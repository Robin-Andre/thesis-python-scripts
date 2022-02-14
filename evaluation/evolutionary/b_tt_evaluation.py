import math

import numpy as np
import pandas
import scipy.optimize
from matplotlib import pyplot as plt

from configurations import SPECS
from configurations.parameter import Parameter

def remove_count(string):
    if string == "target":
        return 0
    elif string.__contains__("count") and len(string) >= 6:
        return int(string[5:]) + 1
    else:
        return string


def __next_helper(x, full_mode, IDString):
    data = pandas.read_csv(SPECS.EXP_PATH + "b_tt_csvs/" + full_mode)
    data = data.rename(remove_count, axis=1)

    # Remove irrelevant values
    data = data[data["tripMode"] == Parameter(x).requirements["tripMode"]]

    # Drop Data which is too small to be relevant
    drop_threshold = 0.005
    sum = data[0].sum()
    data = data[data[0] >= sum * drop_threshold]
    data = data.set_index(["Unnamed: 0", "tripMode", IDString])



    data = data.fillna(0)

    data = data.drop(["count"], axis=1)



    data_r = data.div(data[0], axis=0)
    data_r = data_r.reset_index()
    data_r = data_r[data_r["tripMode"] == Parameter(x).requirements["tripMode"]]
    data_r = data_r.set_index(["Unnamed: 0", "tripMode", IDString])
    return data_r


def __helper(modes, appendix, IDString):
    for i, x in enumerate(modes):
        full_mode = x + appendix
        data_r = __next_helper(x, full_mode, IDString)
        data_r.plot()
        t = data_r.T
        t = t.sort_index()
        t.plot(legend=None)
    plt.show()


def main():
    modes = ["b_tt_car_d_mu", "b_tt_car_p_mu", "b_tt_put_mu", "b_tt_bike_mu"]
    appendix = "time.csv"
    id_string = "durationTrip"
    __helper(modes, appendix, id_string)


def main2():
    modes = ["b_tt_car_d_mu", "b_tt_car_p_mu", "b_tt_put_mu", "b_tt_bike_mu"]
    appendix = "dist.csv"
    id_string = "distanceInKm"
    __helper(modes, appendix, id_string)


def mainfull():
    modes = ["b_tt_car_d_mu", "b_tt_car_p_mu", "b_tt_put_mu", "b_tt_bike_mu"]
    appendix = "FullPopdist.csv"
    id_string = "distanceInKm"
    __helper(modes, appendix, id_string)
    __helper(modes, "FullPoptime.csv", "durationTrip")


def mainfull2():
    modes = ["b_tt_car_d_mu", "b_tt_car_p_mu", "b_tt_put_mu", "b_tt_bike_mu"]
    appendix = "FullPopbonusdist.csv"
    id_string = "distanceInKm"
    __helper(modes, appendix, id_string)
    __helper(modes, "FullPopbonustime.csv", "durationTrip")


def eval_broken_btt():
    __helper(["b_tt_car_d_mu"], "SmallBrokenAsctime.csv", "durationTrip")

def expected_b_tt_func(x, L, k):
    return L / (1 * np.exp(k * (x)))


def plot_inverse_exponential():
    xvals = list(range(100))
    alpha = 0.02
    yvals = [expected_b_tt_func(x, alpha) for x in xvals]
    print(yvals)
    plt.plot(xvals, yvals)
    plt.show()


def __approximator(mode, fullmode, IDString):
    data = __next_helper(mode, fullmode, IDString)
    popt_list = []
    for i in data.columns.values:
        #fig, ax = plt.subplots()
        if i == 0:
            break
        vals = data[i].values
        ind = data.index.get_level_values(IDString).values

        popt, pcov = scipy.optimize.curve_fit(expected_b_tt_func, list(ind), list(vals))

        popt_list.append(popt[1])
        #ax.plot(ind, expected_b_tt_func(ind, *popt))
        #ax.plot(ind, vals)
        #fig.show()
    print(popt_list)
    print(list(range(len(popt_list))))
    plt.plot(list(range(len(popt_list))), popt_list)
    plt.show()

def approximate_one_data():

    IDString = "durationTrip"
    __approximator("b_tt_car_d_mu", "b_tt_car_d_muSmallBrokenAsctime.csv", IDString)


def approx_weirdness():
    IDString = "durationTrip"
    for i in [-2, -1, 0, 1, 2]:
        __approximator("b_tt_car_d_mu", "b_tt_car_d_muWeird"+str(i)+"time.csv", IDString)


def approx_full():
    IDString = "durationTrip"

    __approximator("b_tt_car_d_mu", "b_tt_car_d_mutime.csv", IDString)


if __name__ == "__main__":
    #mainfull2()
    #eval_broken_btt()
    approx_full()
    #approximate_one_data()
    #approx_weirdness()
    #plot_inverse_exponential()
    #main()


