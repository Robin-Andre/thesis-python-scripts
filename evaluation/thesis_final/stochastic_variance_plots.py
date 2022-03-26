import pandas

from configurations import SPECS


def main():
    csv = pandas.read_csv(SPECS.EXP_PATH + "data_random/temp.csv")
    test = csv.mean()
    print(csv)
    print(test)


if __name__ == "__main__":
    main()