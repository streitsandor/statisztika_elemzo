import sys
import pandas as pd
import matplotlib.pyplot as plt
from icecream import ic

# print(plt.style.available) # stílus keresésre, ha kell


def main():
    diagramok = {1: diagram1, 2: diagram2}  # Választható diagramok
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
