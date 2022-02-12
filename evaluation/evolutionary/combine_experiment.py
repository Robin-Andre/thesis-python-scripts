import pandas
from matplotlib import pyplot as plt

from configurations import SPECS


def plot(df, name):
    temp = df[[name]]
    temp = temp.reset_index()
    ax = plt.subplot()
    value = temp["iteration"].max()
    for val in list(set(temp["measure"])):
        x = temp[temp["measure"] == val]
        ax.plot(range(0, value), value * [0],  "--", color="black")  # Plots a zero line for perfect similarity
        ax.plot(x["iteration"], x[name], label=val)
        ax.set_title(name)
        #ax.set_ylim([-2e7, 0])
        ax.legend()
    plt.show()


def main():
    datac = pandas.read_csv(SPECS.EXP_PATH + "Combine.csv", sep=",")
    data = pandas.read_csv(SPECS.EXP_PATH + "Mutate.csv", sep=",")


    param = pandas.read_csv(SPECS.EXP_PATH + "ParameterExperiment.csv", sep=",")
    param = param.groupby(["param_list", "iteration"]).mean()
    param.index.set_names(["measure", "iteration"], inplace=True)
    plot(param, "best_metric_demand")

    base = pandas.read_csv(SPECS.EXP_PATH + "BaselineRandom.csv", sep=",")
    base = base.groupby(["opr", "iteration"]).mean()
    base.index.set_names(["measure", "iteration"], inplace=True)
    aggc = datac.groupby(["opc", "iteration"]).mean()
    agg = data.groupby(["opm", "iteration"]).mean()
    aggc.index.set_names(["measure", "iteration"], inplace=True)
    agg.index.set_names(["measure", "iteration"], inplace=True)
    temp = pandas.concat([aggc, base])
    temp = aggc
    plot(temp, "best_metric_modal")
    plot(temp, "best_metric_time")
    plot(temp, "best_metric_demand")

    temp = pandas.concat([aggc, base])

    plot(temp, "best_metric_modal")
    plot(temp, "best_metric_time")
    plot(temp, "best_metric_demand")
    #temp.plot(x="iteration", y="best_metric_modal")
    plt.show()


if __name__ == "__main__":
    main()
