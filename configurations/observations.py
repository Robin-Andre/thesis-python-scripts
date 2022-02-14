import math
from abc import ABC, abstractmethod


class Observation(ABC):
    def __init__(self):
        pass

    def observe(self, ind_1, target_data, parameter):
        return 0

    def observe_detailed(self, data_1, data_2, target_data, parameter):
        return 0


class TimeModeObservation(Observation):

    def observe(self, ind_1, target_data, parameter):
        time_df = ind_1.data.travel_time.get_data_frame()
        target_df = target_data.travel_time.get_data_frame()

        assert parameter.requirements.keys().__contains__("tripMode")

        time_df = time_df[time_df["tripMode"] == parameter.requirements["tripMode"]]
        target_df = target_df[target_df["tripMode"] == parameter.requirements["tripMode"]]




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

    def __helper(self, ind_1, target_data, parameter):
        assert parameter.requirements.keys().__contains__("tripMode")
        mode_num = parameter.requirements["tripMode"]

        y_1 = ind_1.data.get_modal_split().loc[mode_num, "count"]
        y_target = target_data.get_modal_split().loc[mode_num, "count"]
        x_1 = ind_1[parameter.name].value

        return x_1, y_1, y_target, mode_num

    # This function suggests, for a lack of information, the estimated value from the sigmoid transformation as a new
    def observe(self, ind_1, target_data, parameter):
        x_1, y_1, y_target, mode_num = self.__helper(ind_1, target_data, parameter)
        return g(y_target, mode_num) + x_1 - g(y_1, mode_num)


    def observe_detailed(self, ind_1, ind_2, target_data, parameter):
        x_1, y_1, y_target, mode_num = self.__helper(ind_1, target_data, parameter)
        x_2 = ind_2[parameter.name].value
        y_2 = ind_2.data.get_modal_split().loc[mode_num, "count"]

        z = g(y_target)
        z_1 = g(y_1)
        z_2 = g(y_2)
        a = (z - z_1) / (z_2 - z_1)  # a is the linear scale factor based on the normalized parameters

        return a * (x_2 - x_1) + x_1

