import math
from abc import ABC, abstractmethod
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

    def _helper(self, ind_1, target_data, parameter):
        time_df = ind_1.data.travel_time.get_data_frame()
        target_df = target_data.travel_time.get_data_frame()

        lsuffix = "_target"

        assert parameter.requirements.keys().__contains__("tripMode")

        temp = time_df.groupby(["tripMode", "durationTrip"]).sum()["count"].to_frame()
        temp_target = target_df.groupby(["tripMode", "durationTrip"]).sum()["count"].to_frame()

        wololo = temp.iloc[temp.index.get_level_values("tripMode") == 1]
        target_wololo = temp_target.iloc[temp_target.index.get_level_values("tripMode") == 1]

        temp = target_wololo.join(wololo, how="left", lsuffix=lsuffix, rsuffix="_observation")
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
        return tuple(popt)

    def error(self, ind_1, target_data, parameter):
        return self._helper(ind_1, target_data, parameter)[1]

    def observe(self, ind_1, target_data, parameter):
        popt = self._helper(ind_1, target_data, parameter)
        # A positive value for popt[1] means that the time preference component has too much impact
        # In order to reduce it the -exp(x) function needs to return a smaller value (for all except b_tt_ped_mu)
        # So counterintuitively b_tt-* needs to be decreased to reduce the negative impact. For this reason
        # it is recommended to attach an inverse function to the specific parameter to gain a linear impact on the
        # time component.

        alpha = 1

        x_1 = ind_1[parameter].value  # x == -0.5
        y_1 = self.f(x_1)
        y_new = y_1 + alpha * popt[1]
        x_new = self.f_inverse(y_new)
        print(f"Suggested Value: {x_new}")
        return x_new

    def guess(self, x_1, y_1, x_2, y_2):
        # Calculate m * x + c for a linear approximation
        m = (y_2 - y_1) / (x_2 - x_1)
        c = y_1 - m * x_1

        # Calculate the where the approximation would be zero
        x_new = -c / m
        epsilon = 0.001
        assert abs(y_1 - m * x_1 - c) < epsilon
        assert abs(y_2 - m * x_2 - c) < epsilon
        return self.f_inverse(x_new)

    def observe_detailed(self, ind_1, ind_2, target_data, parameter):
        popt1 = self._helper(ind_1, target_data, parameter)
        popt2 = self._helper(ind_2, target_data, parameter)

        x_1 = ind_1[parameter].value
        y_1 = self.f(x_1)

        x_2 = ind_2[parameter].value
        y_2 = self.f(x_2)

        new_x = self.guess(y_1, popt1[1], y_2, popt2[1])
        print(f"Suggested Value: {new_x}")
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

        y_1 = ind_1.data.get_modal_spliteeee(parameter)
        y_target = target_data.get_modal_spliteeee(parameter)
        x_1 = ind_1[parameter.name].value

        return x_1, y_1, y_target, mode_num

    # This function suggests, for a lack of information, the estimated value from the sigmoid transformation as a new
    def observe(self, ind_1, target_data, parameter):
        x_1, y_1, y_target, mode_num = self._helper(ind_1, target_data, parameter)
        x_new = g(y_target, mode_num) + x_1 - g(y_1, mode_num)
        print(f"Suggested Value: {x_new}")
        return x_new

    def error(self, ind_1, target_data, parameter):
        x_1, y_1, y_target, mode_num = self._helper(ind_1, target_data, parameter)
        return abs(y_1 - y_target)

    def observe_detailed(self, ind_1, ind_2, target_data, parameter):
        x_1, y_1, y_target, mode_num = self._helper(ind_1, target_data, parameter)
        x_2 = ind_2[parameter.name].value
        y_2 = ind_2.data.get_modal_spliteeee(mode_num)

        z = g(y_target)
        z_1 = g(y_1)
        z_2 = g(y_2)
        a = (z - z_1) / (z_2 - z_1)  # a is the linear scale factor based on the normalized parameters
        x_new = a * (x_2 - x_1) + x_1
        print(f"Suggested Value: {x_new}")
        return x_new

