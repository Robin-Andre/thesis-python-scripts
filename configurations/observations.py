import logging
import math
from abc import ABC, abstractmethod

import numpy
import numpy as np
import scipy.optimize
from matplotlib import pyplot as plt


class Observation(ABC):
    def __init__(self, function=lambda x: x, function_inverse=lambda x: x):
        self.f = function
        self.f_inverse = function_inverse

    def observe(self, ind_1, target_data, parameter):
        return 0

    def observe_detailed(self, ind_1, ind_2, target_data, parameter):
        return 0

    def error(self, ind_1, target_data, parameter):
        return 0


def expected_b_tt_func(x, L, k):
    return L / (1 * np.exp(k * x))


def b_tt_exp(x):
    return -math.exp(x)

def b_tt_exp_inverse(y):
    return math.log(-y)


class CostObservation(Observation):
    pass


class ElasticityObservation(Observation):
    """
    The elasticity parameters are cursed, trying to optimize them will only result in tears and broken bones.
    If anyone reads this and does unironically attempt to implement an observation for elasticity parameters:
    Godspeed
    """
    pass


class TimeModeObservation(Observation):

    def __init__(self, function=lambda x: -math.exp(x), inverse_function=lambda x: math.log(-x)):
        """
        The time observation is relevant for parameters that have variable utility based on travel time.
        This incorporates mainly the b_tt-* parameters. Since the impact of these parameters is calculated differently
        a function can be passed along to capture the underlying utility calculation that might be variable.
        """
        self.f = function
        self.f_inverse = inverse_function
        self.verify_functions()

    def verify_functions(self):
        epsilon = 0.0001

        for x in [-20, -10, -1, -0.01, 0, 0.01, 10, 20]:
            assert abs(self.f_inverse(self.f(x)) - x) < epsilon

    def _interpolate(self, x_1, y_1, x_2, y_2, y_target):
        assert y_1 != y_2
        a = (y_target - y_1) / (y_2 - y_1)
        return a * (x_2 - x_1) + x_1

    def _generate_quantiles(self, frame):
        # TODO this is dangerous, there is no guarantee that durationTrip is the last element of th index
        assert frame.index.names[-1] == "durationTrip"
        quants = [.1, .2, .3, .4, .5, .6, .7, .8, .9, .99, .999]
        cumulated_values = frame["count"].cumsum()
        quantile_vals = cumulated_values.quantile(quants)

        x = [(numpy.abs(cumulated_values - i)).argmin() for i in quantile_vals]

        x_1_index = [numpy.where(cumulated_values < i)[0][-1] for i in quantile_vals]
        x_2_index = [i + 1 for i in x_1_index]

        t_1 = cumulated_values.take(x_1_index)
        t_2 = cumulated_values.take(x_2_index)

        y_1 = t_1.values
        y_2 = t_2.values

        x_1 = t_1.index.get_level_values(-1).values
        x_2 = t_2.index.get_level_values(-1).values

        y_target = quantile_vals.values
        assert len(x_1) == len(x_2) == len(y_1) == len(y_2) == len(quants)
        better_results = [self._interpolate(a, b, c, d, e) for a, b, c, d, e in zip(x_1, y_1, x_2, y_2, y_target)]
        print(f"Better Interpolation: {better_results}")
        q = cumulated_values.index.values[x]
        return better_results
        #return [split_tuples[-1] for split_tuples in q] OLD RETURN WITH FIXED VALUEs


    def _generate_function_estimate(self, target, observation):
        lsuffix = "_target"

        temp = target.join(observation, how="left", lsuffix=lsuffix, rsuffix="_observation")
        temp = temp.fillna(0)

        drop_threshold = 0.005
        sum_count = temp["count" + lsuffix].sum()
        data = temp[temp["count" + lsuffix] >= sum_count * drop_threshold]

        filtered_data = data.copy()
        filtered_data.loc[:, "relative_values"] = filtered_data["count_observation"] / filtered_data["count" + lsuffix]

        vals = filtered_data["relative_values"].values
        ind = filtered_data.index.get_level_values("durationTrip").values
        popt, pcov = scipy.optimize.curve_fit(expected_b_tt_func, list(ind), list(vals))

        #plt.plot(ind, expected_b_tt_func(ind, *popt))
        #plt.plot(ind, vals)
        #plt.show()
        #plt.close(fig)
        print(popt)
        return tuple(popt)

    def _get_data_subset(self, dataframe, parameter):
        requirements = list(parameter.requirements.keys())
        temp = dataframe.groupby(requirements + ["durationTrip"]).sum()["count"].to_frame()
        for k, v in parameter.requirements.items():
            temp = temp.iloc[temp.index.get_level_values(k) == parameter.requirements[k]]
        return temp

    def _helper(self, ind_1, target_data, parameter):
        assert parameter.requirements.keys().__contains__("tripMode")

        wololo = self._get_data_subset(ind_1.data.travel_time.get_data_frame(), parameter)
        target_wololo = self._get_data_subset(target_data.travel_time.get_data_frame(), parameter)
        #x = self._generate_quantiles(wololo)
        #y = self._generate_quantiles(target_wololo)

        #print(x)
        #print(y)
        #print([a_i - b_i for a_i, b_i in zip(x, y)])
        #print(sum([a_i - b_i for a_i, b_i in zip(x, y)]))

        estimate = self._generate_function_estimate(target_wololo, wololo)
        #print(estimate)
        return estimate

    def _other_error_method(self, ind_1, target_data, parameter):
        x = self._get_data_subset(ind_1.data.travel_time.get_data_frame(), parameter)
        y = self._get_data_subset(target_data.travel_time.get_data_frame(), parameter)

        a = self._generate_quantiles(x)
        b = self._generate_quantiles(y)
        #print(f"Param {parameter}")
        print([a_i - b_i for a_i, b_i in zip(a, b)])
        z = sum([a_i - b_i for a_i, b_i in zip(a, b)])
        print(z)
        return z

    def error(self, ind_1, target_data, parameter):
        z = self._other_error_method(ind_1, target_data, parameter)
        alpha = 0.01
        return z * alpha
        #return alpha * self._helper(ind_1, target_data, parameter)[1]

    def observe(self, ind_1, target_data, parameter):
        #popt = self._helper(ind_1, target_data, parameter)
        error = self.error(ind_1, target_data, parameter)
        # A positive value for popt[1] means that the time preference component has too much impact
        # In order to reduce it the -exp(x) function needs to return a smaller value (for all except b_tt_ped_mu)
        # So counterintuitively b_tt-* needs to be decreased to reduce the negative impact. For this reason
        # it is recommended to attach an inverse function to the specific parameter to gain a linear impact on the
        # time component.

        alpha = -0.1

        x_1 = ind_1[parameter].value  # x == -0.5
        y_1 = self.f(x_1)
        y_new = y_1 + alpha * error

        #print(f"Debug{x_1} {y_1} {y_new} {error}")

        x_new = self.f_inverse(y_new)
        #print(f"{x_1} {y_1}|  {y_new}")
        #print(f"Suggested Value simple: {x_new}")
        return x_new

    def guess(self, x_1, y_1, x_2, y_2):
        #print(f"The values are {x_1}, {y_1}  {x_2}, {y_2}")
        # Calculate m * x + c for a linear approximation
        m = (y_2 - y_1) / (x_2 - x_1)
        c = y_1 - m * x_1

        # This is a special case for the quantile approximation, since it is easily possible to generate two identical
        # y_1 == y_2
        if m == 0 or abs(y_2 - y_1) < 0.001:
            print(f"Special case has entered the chat")
            # if y is positive that means that the b_tt value is too large and smaller travels should be preferred
            step = -0.1 * numpy.sign(y_1)
            x_new = x_1 + step
        else:
            assert m != 0
            # Calculate the where the approximation would be zero
            x_new = -c / m
            epsilon = 0.001
            assert abs(y_1 - m * x_1 - c) < epsilon
            assert abs(y_2 - m * x_2 - c) < epsilon
        #print(f"New x before inverse: {x_new}")
        if x_new >= 0:
            x_new = -0.0000001
        return self.f_inverse(x_new)

    def observe_detailed(self, ind_1, ind_2, target_data, parameter):
        #popt1 = self._helper(ind_1, target_data, parameter)
        #popt2 = self._helper(ind_2, target_data, parameter)
        error_1 = self.error(ind_1, target_data, parameter)
        error_2 = self.error(ind_2, target_data, parameter)
        #print(f"Errors: {error_1}  {error_2}")
        x_1 = ind_1[parameter].value
        y_1 = self.f(x_1)

        x_2 = ind_2[parameter].value
        y_2 = self.f(x_2)

        new_x = self.guess(y_1, error_1, y_2, error_2)
        #print(f"Suggested Value: {new_x}")
        return new_x


def g(y, mode_num=-1):
    return mode_logit(y, mode_num)


def mode_logit(y, mode_num):
    if mode_num == 0:
        return bike_logit(y)
    elif mode_num == 1:
        return car_logit(y)
    else:
        return default_logit(y)


def default_logit(y, limit=1):
    return inv_log_func(y, 0.5, 2.5, limit)


def inv_log_func(y,  k, x_0, L):
    return (math.log((L / y) - 1) / -k) + x_0


def car_logit(x):
    return default_logit(x, limit=0.67)


def bike_logit(x):
    return default_logit(x, limit=0.75)


class ModalSplitObservation(Observation):

    def _helper(self, ind_1, target_data, parameter):
        assert parameter.requirements.keys().__contains__("tripMode")
        mode_num = parameter.requirements["tripMode"]

        y_1 = ind_1.data.get_modal_split_by_param(parameter)
        y_target = target_data.get_modal_split_by_param(parameter)
        x_1 = ind_1[parameter.name].value

        return x_1, y_1, y_target, mode_num

    # This function suggests, for a lack of information, the estimated value from the sigmoid transformation as a new
    def observe(self, ind_1, target_data, parameter):
        x_1, y_1, y_target, mode_num = self._helper(ind_1, target_data, parameter)
        x_new = g(y_target, mode_num) + x_1 - g(y_1, mode_num)
        return x_new

    def error(self, ind_1, target_data, parameter):
        x_1, y_1, y_target, mode_num = self._helper(ind_1, target_data, parameter)
        #print(f"Targets and stuff and so {x_1} {y_1} {y_target} {parameter.name}")
        return y_1 - y_target

    def observe_detailed(self, ind_1, ind_2, target_data, parameter):
        x_1, y_1, y_target, mode_num = self._helper(ind_1, target_data, parameter)
        x_2 = ind_2[parameter.name].value
        y_2 = ind_2.data.get_modal_split_by_param(parameter)

        z = g(y_target)
        z_1 = g(y_1)
        z_2 = g(y_2)
        #print(f"All the observed ladies: {x_1} {y_1} {y_target} {z} {z_1} {z_2}")

        if abs(z_2 - z_1) < 0.000001:
            logging.warning("Careful, low value ")
            a = 0.5
        else:
            a = (z - z_1) / (z_2 - z_1)  # a is the linear scale factor based on the normalized parameters
        x_new = a * (x_2 - x_1) + x_1
        return x_new

