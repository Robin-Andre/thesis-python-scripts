import numpy
import pandas
from matplotlib import pyplot as plt
from matplotlib.ticker import MaxNLocator

import visualization
from configurations import SPECS

def plot_all_from_df(df):
    steps = [5, 5, 3, 5, 4, 5, 5, 5, 5, 5, 5, 5, 5, 4, 3, 6, 5, 5, 4, 5, 5, 5, 2, 5, 5, 5, 5, 5, 5]
    x = numpy.cumsum(steps)[:-1]
    x_2 = numpy.cumsum(steps)[1:]

    df.iloc[:, x[-2]:x_2[-2]].plot()
    plt.show()

def plot_main_asc_params(df, ax=None):
    temp = df.iloc[:, :5]
    print(temp.columns)
    temp = temp.iloc[:, [4, 0, 1, 3, 2]]
    assert temp.columns[1] == "asc_car_d_mu"
    temp.columns = ["$\\alpha^{bike}$", "$\\alpha^{car}$", "$\\alpha^{pass}$", "$\\alpha^{ped}$", "$\\alpha^{pub}$"]
    show = False
    if ax is None:
        fig, ax = plt.subplots()
        show = True
    temp.plot(ax=ax, color=visualization.color_modes(None, get_all=True))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if show:
        fig.show()

def plot_main_beta_params(df, ax=None):
    temp = df.iloc[:, 5:10]
    print(temp.columns)
    temp = temp.iloc[:, [3, 1, 0, 4, 2]]
    print(temp.columns)
    assert temp.columns[0] == "b_tt_bike_mu"
    temp.columns = ["$\\beta^{bike}$", "$\\beta^{car}$", "$\\beta^{pass}$", "$\\beta^{ped}$", "$\\beta^{pub}$"]
    show = False
    if ax is None:
        fig, ax = plt.subplots()
        show = True
    temp.plot(ax=ax, color=visualization.color_modes(None, get_all=True))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if show:
        fig.show()

def plot_subset_car_age(df, ax=None):
    temp = df.loc[:, ["asc_car_d_mu", "female_on_asc_car_d", "student_on_asc_car_d", "pkw_1_on_asc_car_d", "inc_high_on_asc_car_d", "age_70_100_on_b_tt_car_d"]]
    temp.columns = ["Name", "Fem", "Student", "Pkw_1", "Rich Bois", "OLDGOATS"]
    show = False
    if ax is None:
        fig, ax = plt.subplots()
        show = True
    temp.plot(ax=ax)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    if show:
        fig.show()
def main():
    path = SPECS.EXP_PATH + r"\MyAlgorithmFullMode\csv\FixedQuantilesTarget101_Algo43parameter_list.csv"
    df = pandas.read_csv(path)

    path = SPECS.EXP_PATH + r"\MyAlgorithmFullTwoPassesNewSetWithTargetSeed\csv\ImprovedDetailPasses100_Algo42parameter_list.csv"
    df2 = pandas.read_csv(path)
    plot_all_from_df(df2)
    print(list(df2.columns))
    return
    df2.iloc[:, :5].plot()
    df2.iloc[:, 5:10].plot()
    plt.show()
    return
    df.plot()
    df.iloc[:, 5:10].plot()
    df.iloc[:, 10:15].plot()

    plt.show()
    print(df)
    print(df.columns)


if __name__ == "__main__":
    main()