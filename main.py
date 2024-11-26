import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from icecream import ic
import numpy as np

# print(plt.style.available)  # stílus keresésre, ha kell


def clear_console() -> None:  # konzol tisztítása
    os.system("cls" if os.name == "nt" else "clear")


def main() -> None:
    clear_console()
    diagramok = {1: diagramSS, 2: diagramOA}  # Választható diagramok
    plt.tight_layout()

    while True:
        try:
            statisztika_szama = int(
                input(
                    """
                    ==============================================
                        0. Kilépés
                        
                        1. Átlagkereset foglalkozás szerint - Teljes munkaidő (bruttó)
                        2. A népesség gazdasági aktivitása korcsoportok szerint
                    ==============================================
                    
                    Válasszon egy diagramot: """
                )
            )
            if statisztika_szama == 0:
                break

            if statisztika_szama in diagramok:  # Kiválasztott diagram futtatása
                clear_console()
                diagramok[statisztika_szama]()
            else:
                clear_console()
                print("Nem megfelelő számot adott meg!")
        except ValueError:
            clear_console()
            print("Érvénytelen karakter. Kérem számot adjon meg!")


def integer_formazo(x: int, pos) -> str:  # integer formázó
    return "{:0,d}".format(int(x))


def lista_darabolas(bemeneti_lista: list, darab_meret: int) -> list:  # lista daraboló
    visszatero_lista = []
    for i in range(0, len(bemeneti_lista), darab_meret):
        visszatero_lista.append(bemeneti_lista[i : i + darab_meret])
    return visszatero_lista


def diagramSS() -> None:
    plt.style.use("seaborn-v0_8-dark")
    plt.suptitle("Átlagkereset foglalkozás szerint - Teljes munkaidő (bruttó)")

    alap_param = {"xlabel": "Év", "ylabel": "Kereset"}
    csv_adatok = pd.read_csv(
        "import/stadat-mun0208-20.1.1.52-hu_tisztitott.csv", encoding="UTF-8"
    )
    fejlec_adatok = list(csv_adatok)[2:]  # fejléc összeállítása
    darabolt_listak = lista_darabolas(csv_adatok, 10)  # adatok feldarabolása

    while True:
        try:
            print(
                f"""
                    **********************************************
                        0. Vissza a főmenübe
                        
                        Összesen {len(darabolt_listak)} lista áll rendelkezésre.
                    **********************************************
                """
            )
            alszam = int(
                input(
                    """
                    Válassza ki a megjelenítendő listát: """
                )
            )

            if alszam == 0:
                clear_console()
                break
            elif alszam > 0 and alszam <= len(
                darabolt_listak
            ):  # kiválasztott tábla paraméterezése
                clear_console()
                uj_param = {
                    **alap_param,
                    "adat": darabolt_listak[alszam - 1].reset_index(drop=True),
                    "fejlec_adatok": fejlec_adatok,
                    "title": str(alszam) + ". táblázat",
                }
                diagramSS_kirajzolo(uj_param)
            else:
                clear_console()
                print("Nem megfelelő számot adott meg!")

        except ValueError:
            clear_console()
            print("Érvénytelen karakter. Kérem számot adjon meg!")


def diagramSS_kirajzolo(parameter) -> None:  # kiválasztott tábla rajzolása
    for i in range(len(parameter["adat"])):
        plt.plot(
            parameter["fejlec_adatok"],
            list(parameter["adat"].iloc[i][2:]),
            label=str(parameter["adat"]["FEOR"][i])
            + " - "
            + str(parameter["adat"]["Foglalkozás megnevezése"][i]),
            linewidth=3,
            marker="o",
        )

    plt.xlabel(parameter["xlabel"])
    plt.ylabel(parameter["ylabel"])

    plt.title(parameter["title"])
    plt.ticklabel_format(style="plain", axis="y")
    plt.gca().yaxis.set_major_formatter(FuncFormatter(integer_formazo))
    plt.grid(color="green", linestyle="--", linewidth=0.5)
    plt.legend()

    plt.show()


# START---OA-------------------------------------------------------------------------------------------
def diagramOA() -> None:
    plt.style.use("fivethirtyeight")

    df1 = pd.read_excel(r"import/mun0005.xlsx")
    df2 = pd.read_excel(r"import/nep0004.xlsx")

    df1InspectedColumnName = [
        "Korcsoport, éves",
        "Foglalkoztatási ráta, %, ",
    ]  # ezekre az oszlopokra van szükségünk az első DataFrameből
    df1InspectedAgeGroups = [
        "65–69",
        "70–74",
    ]  # ezeket az életkorokat fogjuk vizsgálni évenkénti bontásban, összesítve

    df2InspectedColumnName = [
        "Év, január 1.",
        "Korösszetétel: 65– éves, %",
    ]  # ezt az oszlopot fogjuk vizsgálni a második DataFrameből

    df1MainTitle = getDataFrameTitle(df1)  # a statisztkia adatok főcíme
    df2MainTitle = getDataFrameTitle(df2)  # a statisztkia adatok főcíme

    # ebben a DatFrame-ben az oszlopok a dátumok, amik a diagram "X" tengelyének értékeit adják
    df1 = setRow2ColumnHeader(
        df1, 0
    )  # az első sor legyen a DataFrame oszlopneve. A kiválasztott indexű sor előtt levő összes sort törli! (technkailag: "shift up" művelet)
    df1 = getSelectedColumns(
        df1, df1InspectedColumnName
    )  # csak az adott oszlopokat tartjuk meg
    df1 = getSelectedRows(df1, list(range(2, 14)))  # csak az adott sorokat tartjuk meg
    df1.columns = cleanColumnNames(
        df1.columns, df1InspectedColumnName[1], ""
    )  # csak az évszámokat tartjuk meg az oszlopnevekben
    df1RetiredPeople = getRowsSum(
        df1, df1InspectedColumnName[0], df1InspectedAgeGroups, "retired"
    )  # a 65 és felettiek összesítése a táblázatból, ezt fogjuk ezután használni
    makePlotDiagram(
        df1RetiredPeople.columns[1:],
        df1RetiredPeople.iloc[0, 1:],
        "Év",
        "Foglalkoztatási ráta, %, ",
        "Férfiak és Nők",
        df1MainTitle,
        df1RetiredPeople.columns[1:],
    )

    # ebben a DatFrame-ben az index tratalmazza a dátumokat, amik a diagram "X" tengelyének értékeit adják
    df2 = setRow2ColumnHeader(df2, 0)
    df2.columns = cleanColumnNames(
        df2.columns, "\n", " "
    )  # kitakrítjuk a sortörést az oszlopnevekből
    df2 = getSelectedColumns(
        df2, df2InspectedColumnName
    )  # csak az adott oszlopokat tartjuk meg
    df2 = getSelectedRows(
        df2, list(range(11, 26))
    )  # csak az adott sorokat tartjuk meg, 2009-2023, mivel a foglalkoztatottsági táblázat is ezen időszakra van
    df2 = df2.set_index("Év, január 1.")
    df2.index = df2.index.astype(int)
    makePlotDiagram(
        df2.index,
        df2["Korösszetétel: 65– éves, %"],
        "Év",
        "65 év felettiek aránya %-ban",
        "",
        df2MainTitle,
        df2.index,
    )

    mergedDataFrame = getMergedDataFrame(
        df1RetiredPeople.T[1:],
        df2,
        ["Foglalkoztatási ráta, 65-74 éves, %", "Korösszetétel: 65– éves, %"],
    )
    makeRegressionDiagram(
        mergedDataFrame,
        "Foglalkoztatási ráta, 65-74 éves, %",
        "Korösszetétel: 65– éves, %",
    )


def getMergedDataFrame(sDataFrame1, sDataFrame2, columnNames):
    sDataFrame1.index = sDataFrame1.index.astype(int)
    tempDataFrame = sDataFrame2.join(sDataFrame1, how="inner")
    tempDataFrame.columns = [columnNames[0], columnNames[1]]
    return tempDataFrame


def makePlotDiagram(xAxis, yAxis, xLabel, yLabel, title, suptitle, xticks):
    plt.plot(xAxis, yAxis)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.suptitle(suptitle)
    plt.title(title)
    if xticks is not None:
        plt.xticks(xticks)
    plt.show()


def makeRegressionDiagram(sDataFrame, xAxis, yAxis) -> None:
    x = sDataFrame[xAxis].values
    x = np.array(x, dtype=float)

    y = sDataFrame[yAxis].values
    y = np.array(y, dtype=float)

    df = pd.DataFrame({"Array1": x, "Array2": y})

    plt.figure(figsize=(10, 6))

    # Fit the linear model for Array1 -> Array2
    coefficients1 = np.polyfit(df["Array1"], df["Array2"], 1)
    polynomial1 = np.poly1d(coefficients1)
    trendline1 = polynomial1(df["Array1"])

    # Fit the linear model for Array2 -> Array1
    coefficients2 = np.polyfit(df["Array2"], df["Array1"], 1)
    polynomial2 = np.poly1d(coefficients2)
    trendline2 = polynomial2(df["Array2"])

    # Plot the data
    plt.scatter(
        df["Array1"],
        df["Array2"],
        edgecolor="black",
        linewidth=1,
        alpha=0.75,
        label=xAxis + " <--> " + yAxis,
    )
    plt.scatter(
        df["Array2"],
        df["Array1"],
        edgecolor="black",
        linewidth=1,
        alpha=0.75,
        label=yAxis + " <--> " + xAxis,
    )

    # Plot the regression lines
    plt.plot(df["Array1"], trendline1, color="blue")
    plt.plot(df["Array2"], trendline2, color="red")

    plt.legend()
    plt.title("Lineáris regressziós diagram")
    plt.xlabel(xAxis)
    plt.ylabel(yAxis)
    plt.show()


def getDataFrameTitle(sDataFrame):
    return sDataFrame.columns[0]


def setRow2ColumnHeader(sDataFrame, index):
    sDataFrame.columns = sDataFrame.iloc[index]
    sDataFrame = sDataFrame.drop(sDataFrame.index[index])
    return sDataFrame


def getSelectedColumns(sDataFrame, columnName):
    return sDataFrame[
        [col for col in sDataFrame.columns if any(sub in col for sub in columnName)]
    ]


def getSelectedRows(sDataFrame, rows):
    return sDataFrame.loc[rows]


def cleanColumnNames(columns, replaceFrom, replaceTo):
    return columns.str.replace(replaceFrom, replaceTo, regex=True)


def getRowsSum(sDataFrame, columnName, rows, sumRowName):
    rowsToSummarize = sDataFrame[
        sDataFrame[columnName].isin(rows)
    ]  # az összeadandó sorok leválogatása
    summarizedRow = rowsToSummarize.iloc[
        :, 1:
    ].sum()  # a sorok értékeinek összaadása és a kapott eredmény tárolása
    summarizedRow[columnName] = sumRowName  # az oszlopnév beállítása
    summarizedRowDf = pd.DataFrame(
        [summarizedRow], columns=sDataFrame.columns
    )  # a sor konvertálása DataFrame-re, és az oszlopok fejléceinek beállítása
    return summarizedRowDf


# STOP---OA-------------------------------------------------------------------------------------------


if __name__ == "__main__":  # program belépő függvénye
    rc = 1
    try:
        main()
        rc = 0
    except FileNotFoundError:
        print("Fájl nem található!")
    except Exception as e:
        ic("Error: %s" % e, file=sys.stderr)
    print("Program futása befejezve.")
    sys.exit(rc)
