import pandas
from matplotlib import pyplot as plt

from configurations import SPECS


def plot(df, name):
    temp = df[[name]]
    temp = temp.reset_index()
    ax = plt.subplot()
    for val in list(set(temp["metric"])):
        x = temp[temp["metric"] == val]
        ax.plot(range(0, 50), 50 * [0],  "--", color="black")
        ax.plot(x["iteration"], x[name], label=val)
        ax.legend()
    plt.show()

def main():
    data = pandas.read_csv(SPECS.EXP_PATH + "MetricExperiment.csv", sep=";")
    agg = data.groupby(["metric", "iteration"]).mean()
    print(data)

    plot(agg, "best_metric_modal")
    plot(agg, "best_metric_time")
    plot(agg, "best_metric_demand")
    #temp.plot(x="iteration", y="best_metric_modal")
    plt.show()

if __name__ == "__main__":
    main()
