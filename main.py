import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from icecream import ic

# print(plt.style.available)  # stílus keresésre, ha kell


def clear_console() -> None:  # konzol tisztítása
    os.system("cls" if os.name == "nt" else "clear")


def main() -> None:
    clear_console()
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
                clear_console()
                diagramok[statisztika_szama]()
            else:
                clear_console()
                print("Nem megfelelő számot adott meg!")
        except ValueError:
            clear_console()
            print("Érvénytelen karakter. Kérem számot adjon meg!")


def integer_formazo(x, pos) -> str:  # integer formázó
    return "{:0,d}".format(int(x))


def lista_darabolas(bemeneti_lista, darab_meret) -> list:  # lista daraboló
    visszatero_lista = []
    for i in range(0, len(bemeneti_lista), darab_meret):
        visszatero_lista.append(bemeneti_lista[i : i + darab_meret])
    return visszatero_lista


def diagram1() -> None:
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
                diagram1_kirajzolo(uj_param)
            else:
                clear_console()
                print("Nem megfelelő számot adott meg!")

        except ValueError:
            clear_console()
            print("Érvénytelen karakter. Kérem számot adjon meg!")


def diagram1_kirajzolo(parameter) -> None:  # kiválasztott tábla rajzolása
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
