import pandas
from matplotlib import pyplot as plt

from configurations import SPECS


def plot(df, name):
    temp = df[[name]]
    temp = temp.reset_index()
    ax = plt.subplot()
    value = temp["iteration"].max()
    for val in list(set(temp["opc"])):
        x = temp[temp["opc"] == val]
        ax.plot(range(0, value), value * [0],  "--", color="black") # Plots a zero line for perfect similarity
        ax.plot(x["iteration"], x[name], label=val)
        ax.set_title(name)
        ax.legend()
    plt.show()


def main():
    data = pandas.read_csv(SPECS.EXP_PATH + "Combine.csv", sep=",")
    agg = data.groupby(["opc", "iteration"]).mean()
    print(data)

    plot(agg, "best_metric_modal")
    plot(agg, "best_metric_time")
    plot(agg, "best_metric_demand")
    #temp.plot(x="iteration", y="best_metric_modal")
    plt.show()


if __name__ == "__main__":
    main()
