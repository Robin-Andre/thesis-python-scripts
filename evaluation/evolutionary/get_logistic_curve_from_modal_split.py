import math
import random

import pandas
from matplotlib import pyplot as plt
import numpy as np

from calibration.evolutionary.population import Population
from configurations import SPECS
import mobitopp_execution as simulation
import scipy.optimize


def log_func(x, k, x_0, L):
    return L / (1 + np.exp(-k * (x - x_0)))

# x = (ln((L / y) - 1) / -k) + x_0
def inv_log_func(y,  k, x_0, L):
    return (math.log((L / y) - 1) / -k) + x_0


def put_sig(x):
    return log_func(x, 0.4985368, 2.46005609, 0.99986215)


def put_logit(y):
    return inv_log_func(y, 0.4985368, 2.46005609, 0.99986215)


def test_sigmoid(x, k, x_0):
    return log_func(x, k, x_0, 1)

def test_put_logit(y, k, x_0):
    return inv_log_func(y, k, x_0, 1)

def default_sigmoid(x, limit=1):
    return log_func(x, 0.5, 2.5, limit)


def default_logit(y, limit=1):
    return inv_log_func(y, 0.5, 2.5, limit)


def car_sigmoid(x):
    return default_sigmoid(x, limit=0.67)


def car_logit(x):
    return default_logit(x, limit=0.67)


def bike_sigmoid(x):
    return default_sigmoid(x, limit=0.75)


def bike_logit(x):
    return default_logit(x, limit=0.75)

def f(x):
    return default_sigmoid(x)


# Inverse f^-1(x) == g(y)
def g(y, mode_num=-1):
    return mode_logit(y, mode_num)

def mode_logit(y, mode_num):
    if mode_num == 0:
        return bike_logit(y)
    elif mode_num == 1:
        return car_logit(y)
    else:
        return default_logit(y)


def mode_sigmoid(x, mode_num):
    if mode_num == 0:
        return bike_sigmoid(x)
    elif mode_num == 1:
        return car_sigmoid(x)
    else:
        return default_sigmoid(x)

def remove_count(string):
    return int(string[5:])




def main():
    modes = ["asc_bike_mu", "asc_car_d_mu", "asc_car_p_mu", "asc_ped_mu", "asc_put_mu"]
    full_modes = [x + "othernullmethod.csv" for x in modes]
    for i, x in enumerate(full_modes):
        data = pandas.read_csv(SPECS.EXP_PATH + x)
        data = data.T
        data.drop(index=["tripMode", "count"], inplace=True)
        data.index = data.index.map(remove_count)
        #print(data)
        data.plot()
        plt.title(x)
        x = data.index
        plt.plot(x, default_sigmoid(x), "--")
        #plt.plot(x, log_func(x, 0.4985368, 2.46005609, 0.99986215))
        y = data[i]
        test = scipy.optimize.curve_fit(log_func, x, y)
        print(test)
        plt.show()
        print(put_sig(0))
        print(put_logit(0.2))
        print(put_sig(-0.3203244832543435))


def main2():

    random.seed(42)

    p = Population()
    _, data = simulation.load("../../tests/resources/compare_individual")
    p.set_target(data)
    ind = p.random_individual(make_basic=True)
    a, b, c = ind.draw(data)
    ind.data.draw_modal_split(data)
    #a.show()
    b.show()
    c.show()
    print(f"Current x : {ind['asc_put_mu']} current y : {ind.data.get_modal_split().loc[4, 'count']}")
    print("----------")
    print(f"Ideal x : {put_logit(ind.data.get_modal_split().loc[4, 'count'])}")
    offset = ind['asc_put_mu'].value - put_logit(ind.data.get_modal_split().loc[4, 'count'])
    print(f"Target x: {put_logit(0.2)}")
    print(f"Offset : {offset}")
    print("----------")
    ind["asc_put_mu"].set(put_logit(0.2) + offset)
    print(ind["asc_put_mu"].value)
    ind.run()
    a,b,c = ind.draw(data)
    ind.data.draw_modal_split(data)
    #a.show()
    b.show()
    c.show()
    print(ind["asc_put_mu"])
    print(ind.data.get_modal_split().loc[4, "count"])
    print("------------")
    ind["asc_put_mu"].set(ind["asc_put_mu"].value + put_logit(0.2) - put_logit(0.2104805715133657))
    ind.run()
    a,b,c = ind.draw(data)
    ind.data.draw_modal_split(data)
    #a.show()
    b.show()
    c.show()
    print(ind["asc_put_mu"])
    print(ind.data.get_modal_split().loc[4, "count"])
    print("------------")
    print(put_logit(0.2) - put_logit(0.2104805715133657))


def __helper(ind, data):
    for i, param_name in enumerate(["asc_bike_mu", "asc_car_d_mu", "asc_car_p_mu", "asc_ped_mu", "asc_put_mu"]):
        cur_x = ind[param_name].value
        #print(f"Current x : {ind[param_name].value} current y : {ind.data.get_modal_split().loc[i, 'count']}")
        #print(f"Target y : {data.get_modal_split().loc[i, 'count']}")
        #print(mode_logit(ind.data.get_modal_split().loc[i, 'count'], i))
        offset = ind[param_name].value - put_logit(ind.data.get_modal_split().loc[i, 'count'])
        diff = ind.data.get_modal_split().loc[i, 'count'] - data.get_modal_split().loc[i, 'count']
        new_val = mode_logit(data.get_modal_split().loc[i, 'count'], i) + offset
        val = ind[param_name].value
        if diff > 0:
            # In this case the simulation is bigger than the value previously determined
            set_target = min(new_val, val - 0.5)
        else:
            set_target = max(new_val, val + 0.5)
        ind[param_name].set(set_target)
        #print(ind[param_name].value)
        print(f"{param_name} {ind[param_name].value - cur_x}")

    print(ind.data.get_modal_split())
    print(data.get_modal_split())
    ind.run()
    ind.data.draw_modal_split(data)
    a,b,c = ind.draw(data)
    b.show()
    c.show()


def main3():
    random.seed(42)

    p = Population()
    _, data = simulation.load("../../tests/resources/compare_individual")
    p.set_target(data)
    ind = p.random_individual(make_basic=True)
    ind.data.draw_modal_split(data)

    print((ind["asc_put_mu"].value, ind.data.get_modal_split().loc[4, 'count']))
    xvals = [ind["asc_put_mu"].value]
    yvals = [ind.data.get_modal_split().loc[4, 'count']]
    offset = ind['asc_put_mu'].value - put_logit(ind.data.get_modal_split().loc[4, 'count'])
    bounds = [(0, 0), (10, 50)]
    popt = None
    for i in [0.25, 0.5, 0.75]:
        ind["asc_put_mu"].set(put_logit(i) + offset)
        ind.run()
        print((ind["asc_put_mu"].value, ind.data.get_modal_split().loc[4, 'count']))
        xvals.append(ind["asc_put_mu"].value)
        yvals.append(ind.data.get_modal_split().loc[4, 'count'])
        plt.plot(xvals, yvals)
        popt, pcov = scipy.optimize.curve_fit(test_sigmoid, xvals, yvals, bounds=bounds)
        print(popt)
        plt.plot(range(0,50), test_sigmoid(range(0, 50), *popt))
        plt.show()

    for i in [35, 45, 50]:
        ind["asc_put_mu"].set(i)
        ind.run()
        print((ind["asc_put_mu"].value, ind.data.get_modal_split().loc[4, 'count']))
        xvals.append(ind["asc_put_mu"].value)
        yvals.append(ind.data.get_modal_split().loc[4, 'count'])
        plt.plot(xvals, yvals)
        popt, pcov = scipy.optimize.curve_fit(test_sigmoid, xvals, yvals, bounds=bounds)
        print(popt)
        plt.plot(range(0, 50), test_sigmoid(range(0, 50), *popt))
        plt.show()

    ind["asc_put_mu"].set(test_put_logit(0.13, *popt))
    ind.run()
    ind.data.draw_modal_split(data)


    print(xvals)
    print(yvals)
#    print(test)
    exit()


def main4():
    random.seed(42)

    p = Population()
    _, data = simulation.load("../../tests/resources/compare_individual")
    p.set_target(data)
    ind = p.random_individual(make_basic=True)
    for i in range(6):
        __helper(ind, data)


def _help(x_1, y_1, x_2, y_2, y_target):
    # Estimates an x value to approximate the target
    # x is the configuration parameter. y the observation
    z = g(y_target)
    z_1 = g(y_1)
    z_2 = g(y_2)
    a = (z - z_1) / (z_2 - z_1) # a is the linear scale factor based on the normalized parameters

    return a * (x_2 - x_1) + x_1


def _help_only_one(x_1, y_1, y_target, mode_num):
    print(f"{g(y_1, mode_num)} {x_1} {g(y_target, mode_num)}")
    return g(y_target, mode_num) + x_1 - g(y_1, mode_num)


def tune_parameter_without(ind, parameter, target, pair):
    mode_num = parameter.requirements["tripMode"]
    offset = ind[parameter.name].value - put_logit(ind.data.get_modal_split().loc[mode_num, 'count'])
    ind[parameter.name].set(mode_logit(target, mode_num) + offset)


def extract_x_y(individual, parameter):
    return individual[parameter.name].value, individual.data.get_modal_split().loc[parameter.requirements["tripMode"], "count"]


def visualize(ind, data):
    #a, b, c = ind.draw(data)
    ind.data.draw_modal_split(data)
    #a.show()
    #b.show()
    # c.show()

def suggestions(ind1, target, ind2=None):
    pass


def tune_parameter(ind, parameter, data):
    assert ind.data is not None
    print(f"Optimizing {parameter.name}")
    x_1, y_1 = extract_x_y(ind, parameter)
    mode_num = parameter.requirements["tripMode"]

    target_y = data.get_modal_split().loc[mode_num, "count"]
    new_val = _help_only_one(x_1, y_1, target_y, mode_num)
    ind[parameter.name].set(new_val)
    ind.run()

    #visualize(ind, data)
    x_2, y_2 = extract_x_y(ind, parameter)
    eps = abs(y_2 - target_y)
    print(f"First Iteration Error: {eps}")

    while eps > 0.0001:
        x_new = _help(x_1, y_1, x_2, y_2, target_y)
        print(f"{x_new}")
        ind[parameter.name].set(x_new)
        ind.run()

        #visualize(ind, data)

        _, y_new = extract_x_y(ind, parameter)
        x_1 = x_2
        y_1 = y_2
        x_2 = x_new
        y_2 = y_new

        eps = abs(y_2 - target_y)
        print(f"Error: {eps} {y_2} target: {target_y}")






def main5():
    random.seed(42)

    p = Population()
    _, data = simulation.load("../../tests/resources/compare_individual")
    p.set_target(data)
    ind = p.random_individual(make_basic=True)

    param_name_list = ["asc_bike_mu", "asc_car_d_mu", "asc_car_p_mu", "asc_ped_mu", "asc_put_mu"]
    flag = True
    for i in range(10):
        diff = ind.data.get_modal_split() - data.get_modal_split()
        print(diff)
        print(diff.idxmin())
        print(diff.idxmax())
        maxe = diff.idxmax()

        if flag:
            print(param_name_list[diff.idxmin()["count"]])
            tune_parameter(ind, ind[param_name_list[diff.idxmin()["count"]]], data)

        else:
            print(param_name_list[diff.idxmax()["count"]])
            tune_parameter(ind, ind[param_name_list[diff.idxmax()["count"]]], data)
        flag = not flag
        visualize(ind, data)
    ind.draw()
    exit()
    visualize(ind, data)
    tune_parameter(ind, ind['asc_put_mu'], data)
    visualize(ind, data)
    tune_parameter(ind, ind['asc_car_d_mu'], data)
    visualize(ind, data)
    tune_parameter(ind, ind['asc_ped_mu'], data)
    visualize(ind, data)
    tune_parameter(ind, ind['asc_bike_mu'], data)
    visualize(ind, data)
    tune_parameter(ind, ind['asc_ped_mu'], data)
    visualize(ind, data)
    tune_parameter(ind, ind['asc_put_mu'], data)
    visualize(ind, data)
    tune_parameter(ind, ind['asc_ped_mu'], data)
    visualize(ind, data)
    tune_parameter(ind, ind['asc_ped_mu'], data)
    visualize(ind, data)
    exit()

    ind.data.draw_modal_split(data)
    a, b, c = ind.draw(data)
    #a.show()
    b.show()
    c.show()
    exit()
    offset = ind['asc_put_mu'].value - put_logit(ind.data.get_modal_split().loc[4, 'count'])
    x_1, y_1 = ind['asc_put_mu'].value, ind.data.get_modal_split().loc[4, 'count']
    print(f"{x_1} {y_1}")
    ind["asc_put_mu"].set(put_logit(0.2) + offset)
    ind.run()
    x_2, y_2 = ind['asc_put_mu'].value, ind.data.get_modal_split().loc[4, 'count']
    y_target = data.get_modal_split().loc[4, 'count']
    a, b, c = ind.draw(data)
    b.show()
    c.show()
    ind.data.draw_modal_split(data)
    ind["asc_put_mu"].set(_help(x_1, y_1, x_2, y_2, y_target))
    ind.run()
    a, b, c = ind.draw(data)
    b.show()
    c.show()
    ind.data.draw_modal_split(data)
    x_3, y_3 = ind['asc_put_mu'].value, ind.data.get_modal_split().loc[4, 'count']

    ind["asc_put_mu"].set(_help(x_2, y_2, x_3, y_3))
    ind.run()
    a, b, c = ind.draw(data)
    b.show()
    c.show()
    ind.data.draw_modal_split(data)
    print(ind['asc_put_mu'].value, ind.data.get_modal_split().loc[4, 'count'])


if __name__ == "__main__":
    main5()
