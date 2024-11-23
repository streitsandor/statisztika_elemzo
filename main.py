import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from icecream import ic

os.system("cls" if os.name == "nt" else "clear")  # konzol tisztítása

# print(plt.style.available)  # stílus keresésre, ha kell


def main() -> None:
    diagramok = {1: diagram1, 2: diagram2}  # Választható diagramok
    plt.tight_layout()

    while True:
        try:
            statisztika_szama = int(
                input(
                    """
                    ==============================================
                    0. Kilépés
                    1. Átlagkereset foglalkozás szerint - Teljes munkaidő (bruttó)
                    2. Placeholder
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


def comma_formatter(x, pos) -> str:  # integer formázó
    return "{:0,d}".format(int(x))


def diagram1() -> None:
    plt.style.use("seaborn-v0_8-dark")
    plt.suptitle("Átlagkereset foglalkozás szerint - Teljes munkaidő (bruttó)")

    alap_param = {"xlabel": "Év", "ylabel": "Kereset"}
    csv_adatok = pd.read_csv(
        "import/stadat-mun0208-20.1.1.52-hu_tisztitott.csv", encoding="UTF-8"
    )
    fejlec_adatok = list(csv_adatok)[2:]

    while True:
        try:
            alszam = int(
                input(
                    """
                    
                    **********************************************
                    0. Vissza a főmenübe
                    1. Lista 0-10
                    2. Lista 10-20
                    **********************************************
                    
                    Válasszon egy alszámot: """
                )
            )
            match alszam:
                case 0:
                    break
                case 1:
                    uj_param = {
                        **alap_param,
                        "adat": csv_adatok.iloc[:11],
                        "fejlec_adatok": fejlec_adatok,
                        "title": "0-10",
                    }
                    diagram1_kirajzolo(uj_param)
                case 2:
                    uj_param = {
                        **alap_param,
                        "adat": csv_adatok.iloc[10:21].reset_index(drop=True),
                        "fejlec_adatok": fejlec_adatok,
                        "title": "10-20",
                    }
                    diagram1_kirajzolo(uj_param)
                case _:
                    print("Nem megfelelő alszámot adott meg!")
        except ValueError:
            print("Érvénytelen karakter. Kérem számot adjon meg!")


def diagram1_kirajzolo(parameter) -> None:
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
    plt.gca().yaxis.set_major_formatter(FuncFormatter(comma_formatter))
    plt.grid(color="green", linestyle="--", linewidth=0.5)
    plt.legend()

    plt.show()


def diagram2() -> None:
    print("Placeholder!")
    # kereset2 = pd.read_csv("import/kereset2_2.csv", encoding="ISO-8859-1")
    # kereset2.plot()

    # plt.title("Placeholder title!")
    # plt.legend()
    # plt.show()


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
