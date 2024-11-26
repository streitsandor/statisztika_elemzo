import sys
import pandas as pd
import matplotlib.pyplot as plt
from icecream import ic
import seaborn as sns
import numpy as np

# print(plt.style.available) # stílus keresésre, ha kell


def main():
    diagramok = {1: diagram1, 2: diagram2, 3: oaMain}  # Választható diagramok
    plt.style.use("fivethirtyeight")
    plt.tight_layout()

    while True:
        try:
            statisztika_szama = int(
                input(
                    """
                    ==============================================
                    1. Fejlesztők fizetése életkor szerint
                    2. Placeholder
                    3. A népesség gazdasági aktivitása korcsoportok szerint
                    ==============================================
                    
                    Válasszon egy diagramot: """
                )
            )
            if statisztika_szama == 0:
                break

            if statisztika_szama in diagramok:  # Kiválasztott diagram futtatása
                diagramok[statisztika_szama]()
            else:
                print("Nem megfelelő számot adott meg! (1-4)")
        except ValueError:
            print("Érvénytelen karakter. Kérem számot adjon meg! (1-4)")


def diagram1():
    kereset1 = pd.read_csv("import/prog.csv", encoding="UTF-8")
    plt.plot(kereset1.age, kereset1.value1)
    plt.plot(kereset1.age, kereset1.value2, label="JavaScript")
    plt.plot(
        kereset1.age, kereset1.value3, color="#444444", linestyle="--", label="All Devs"
    )

    plt.xlabel("Age")
    plt.ylabel("Money")

    plt.title("Fõbb kereseti adatok - Életkor szerint")
    plt.legend()
    plt.show()

def diagram2():
    print("Placeholder!")
    # kereset2 = pd.read_csv("import/kereset2_2.csv", encoding="ISO-8859-1")
    # kereset2.plot()

    # plt.title("Placeholder title!")
    # plt.legend()
    # plt.show()

#START---OA-------------------------------------------------------------------------------------------
def oaMain() -> None:
    df1 = pd.read_excel(r'import/mun0005.xlsx')
    df2 = pd.read_excel(r'import/nep0004.xlsx')

    df1InspectedColumnName = ['Korcsoport, éves','Foglalkoztatási ráta, %, '] # ezekre az oszlopokra van szükségünk az első DataFrameből
    df1InspectedAgeGroups = ['65–69','70–74'] # ezeket az életkorokat fogjuk vizsgálni évenkénti bontásban, összesítve

    df2InspectedColumnName = ['Év, január 1.','Korösszetétel: 65– éves, %'] # ezt az oszlopot fogjuk vizsgálni a második DataFrameből

    df1MainTitle = getDataFrameTitle(df1) # a statisztkia adatok főcíme
    df2MainTitle = getDataFrameTitle(df2) # a statisztkia adatok főcíme

    # ebben a DatFrame-ben az oszlopok a dátumok, amik a diagram "X" tengelyének értékeit adják
    df1 = setRow2ColumnHeader(df1,0) # az első sor legyen a DataFrame oszlopneve. A kiválasztott indexű sor előtt levő összes sort törli! (technkailag: "shift up" művelet)
    df1 = getSelectedColumns(df1,df1InspectedColumnName) # csak az adott oszlopokat tartjuk meg
    df1 = getSelectedRows(df1, list(range(2, 14))) # csak az adott sorokat tartjuk meg
    df1.columns = cleanColumnNames(df1.columns,df1InspectedColumnName[1],'') # csak az évszámokat tartjuk meg az oszlopnevekben
    df1RetiredPeople = getRowsSum(df1,df1InspectedColumnName[0],df1InspectedAgeGroups,'retired') # a 65 és felettiek összesítése a táblázatból, ezt fogjuk ezután használni
    makePlotDiagram(df1RetiredPeople.columns[1:],df1RetiredPeople.iloc[0, 1:],'Év','Foglalkoztatási ráta, %, ','Férfiak és Nők',df1MainTitle,df1RetiredPeople.columns[1:])

    # ebben a DatFrame-ben az index tratalmazza a dátumokat, amik a diagram "X" tengelyének értékeit adják
    df2 = setRow2ColumnHeader(df2,0)
    df2.columns = cleanColumnNames(df2.columns,'\n',' ') # kitakrítjuk a sortörést az oszlopnevekből
    df2 = getSelectedColumns(df2,df2InspectedColumnName) # csak az adott oszlopokat tartjuk meg
    df2 = getSelectedRows(df2, list(range(11, 26))) # csak az adott sorokat tartjuk meg, 2009-2023, mivel a foglalkoztatottsági táblázat is ezen időszakra van
    df2 = df2.set_index('Év, január 1.')
    df2.index = df2.index.astype(int)
    makePlotDiagram(df2.index,df2['Korösszetétel: 65– éves, %'],'Év','65 év felettiek aránya %-ban','',df2MainTitle,df2.index)

    mergedDataFrame = getMergedDataFrame(df1RetiredPeople.T[1:],df2,['Foglalkoztatási ráta, 65-74 éves, %','Korösszetétel: 65– éves, %'])
    makeRegressionDiagram(mergedDataFrame,'Foglalkoztatási ráta, 65-74 éves, %','Korösszetétel: 65– éves, %')

def getMergedDataFrame(sDataFrame1,sDataFrame2,columnNames):
    sDataFrame1.index = sDataFrame1.index.astype(int)
    tempDataFrame = sDataFrame2.join(sDataFrame1, how='inner')
    tempDataFrame.columns = [columnNames[0],columnNames[1]]
    return tempDataFrame

def makePlotDiagram(xAxis,yAxis,xLabel,yLabel,title,suptitle,xticks):
    plt.plot(xAxis,yAxis)
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.suptitle(suptitle)
    plt.title(title)
    if xticks is not None:
        plt.xticks(xticks)
    plt.show()
    return

def makeRegressionDiagram(sDataFrame,xAxis,yAxis) -> None: 
    x = sDataFrame[xAxis].values
    x = np.array(x, dtype=float)

    y = sDataFrame[yAxis].values
    y = np.array(y, dtype=float)

    df = pd.DataFrame({'Array1': x, 'Array2': y})

    plt.figure(figsize=(10, 6))
    sns.regplot(x='Array1', y='Array2', data=df, ci=None, label=xAxis + ' <--> ' + yAxis, line_kws={'color': 'blue'})
    sns.regplot(x='Array2', y='Array1', data=df, ci=None, label=yAxis + ' <--> ' + xAxis, line_kws={'color': 'red'})
    plt.legend()
    plt.title('Lineáris regressziós diagram')
    plt.xlabel(xAxis)
    plt.ylabel(yAxis)
    plt.show()

def getDataFrameTitle(sDataFrame):
    return(sDataFrame.columns[0])

def setRow2ColumnHeader(sDataFrame,index):
    sDataFrame.columns = sDataFrame.iloc[index]
    sDataFrame = sDataFrame.drop(sDataFrame.index[index])
    return sDataFrame

def getSelectedColumns(sDataFrame,columnName):
    return sDataFrame[[col for col in sDataFrame.columns if any(sub in col for sub in columnName)]]


def getSelectedRows(sDataFrame,rows):
    return sDataFrame.loc[rows]

def getPlots2Visualize(df,rows):
    for index, row in df.iterrows():
        if len(rows) > 0:
            plt.plot(row.iloc[1:],label=row.iloc[0])
    return plt.plot

def cleanColumnNames(columns,replaceFrom, replaceTo):
    return columns.str.replace(replaceFrom, replaceTo, regex=True)

def getRowsSum(sDataFrame,columnName,rows,sumRowName):
    rowsToSummarize = sDataFrame[sDataFrame[columnName].isin(rows)] # az összeadandó sorok leválogatása
    summarizedRow = rowsToSummarize.iloc[:, 1:].sum() # a sorok értékeinek összaadása és a kapott eredmény tárolása
    summarizedRow[columnName] = sumRowName # az oszlopnév beállítása
    summarizedRowDf = pd.DataFrame([summarizedRow], columns=sDataFrame.columns) # a sor konvertálása DataFrame-re, és az oszlopok fejléceinek beállítása
    return summarizedRowDf
#STOP---OA-------------------------------------------------------------------------------------------


if __name__ == "__main__":
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
