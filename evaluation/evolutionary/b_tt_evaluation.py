import math

import pandas
from matplotlib import pyplot as plt

from configurations import SPECS
from configurations.parameter import Parameter


def main():
    modes = ["b_tt_car_d_mu", "b_tt_car_p_mu", "b_tt_put_mu", "b_tt_bike_mu"]

    for i, x in enumerate(modes):
        full_mode = x + "time.csv"
        data = pandas.read_csv(SPECS.EXP_PATH + "b_tt_csvs/" + full_mode)
        data = data.set_index(["Unnamed: 0", "tripMode", "durationTrip"])
        data = data.fillna(0)
        data_r = data.div(data.target, axis=0)
        data_r = data_r.reset_index()
        #data_r = data / data["target"]
        data_r = data_r[data_r["tripMode"] == Parameter(x).requirements["tripMode"]]

        data_r = data_r.set_index(["Unnamed: 0", "tripMode", "durationTrip"])
        #data_r.plot()
        t = data_r.T
        t.plot()
    plt.show()


def main2():
    modes = ["b_tt_car_d_mu", "b_tt_car_p_mu", "b_tt_put_mu", "b_tt_bike_mu"]

    for i, x in enumerate(modes):
        full_mode = x + "dist.csv"
        data = pandas.read_csv(SPECS.EXP_PATH + "b_tt_csvs/" + full_mode)
        data = data.set_index(["Unnamed: 0", "tripMode", "distanceInKm"])
        data = data.fillna(0)
        data_r = data.div(data.target, axis=0)
        data_r = data_r.reset_index()
        #data_r = data / data["target"]
        data_r = data_r[data_r["tripMode"] == Parameter(x).requirements["tripMode"]]

        data_r = data_r.set_index(["Unnamed: 0", "tripMode", "distanceInKm"])
        data_r.plot()
    plt.show()


def plot_inverse_exponential():
    xvals = list(range(100))
    alpha = 0.05
    yvals = [1 / (4 * math.exp(alpha * x) + 1) for x in xvals]
    print(yvals)
    plt.plot(xvals, yvals)
    plt.show()


if __name__ == "__main__":
    plot_inverse_exponential()
    #main()


    #data = data.T
    #data.drop(index=["tripMode", "count"], inplace=True)
    #data.index = data.index.map(remove_count)
    ##print(data)
    #data.plot()
    #plt.title(x)
    #x = data.index
    #plt.plot(x, default_sigmoid(x), "--")
    ##plt.plot(x, log_func(x, 0.4985368, 2.46005609, 0.99986215))
    #y = data[i]
    #test = scipy.optimize.curve_fit(log_func, x, y)
    #print(test)
    #plt.show()
    #print(put_sig(0))
    #print(put_logit(0.2))
    #print(put_sig(-0.3203244832543435))
