import copy
import logging
import math
from operator import __sub__
from pathlib import Path

import numpy
import pandas

import visualization
from configurations.parameter import Parameter, ActivityGroup
from metrics.metric import aggregate
from metrics.trafficdemand import TrafficDemand
from metrics.traveldistance import TravelDistance
from metrics.traveltime import TravelTime
from metrics.zone_destination_traffic import ZoneDestinationTraffic


class Data:
    def __init__(self, raw_data=None):
        if raw_data is None:
            self.traffic_demand = None
            self.travel_time = None
            self.travel_distance = None
            self.zone_destination = None
            return

        self.traffic_demand = TrafficDemand.from_raw_data(raw_data)
        self.travel_time = TravelTime.from_raw_data(raw_data)
        self.travel_distance = TravelDistance.from_raw_data(raw_data)
        self.zone_destination = ZoneDestinationTraffic.from_raw_data(raw_data)

    def __eq__(self, other):
        return self.traffic_demand._data_frame.equals(other.traffic_demand._data_frame)\
               and self.travel_time._data_frame.equals(other.travel_time._data_frame) \
               and self.travel_distance._data_frame.equals(other.travel_distance._data_frame) \
               and self.zone_destination._data_frame.equals(other.zone_destination._data_frame)

    def empty(self):
        return all(v is None for v in [self.traffic_demand, self.travel_time, self.travel_distance])

    def write(self, path="dump\\"):
        self.safe_write(self.traffic_demand, path + "Demand.csv")
        self.safe_write(self.travel_time, path + "Time.csv")
        self.safe_write(self.travel_distance, path + "Distance.csv")
        self.safe_write(self.zone_destination, path + "ZoneDestination.csv")

    def safe_write(self, write_object, path):
        if write_object is None:
            logging.warning(f" Cannot write data for {path}: Object is None")
        else:
            write_object.write(path)

    def load(self, path="dump\\"):
        self.traffic_demand = self.safe_load(TrafficDemand, path + "Demand.csv")
        self.travel_time = self.safe_load(TravelTime, path + "Time.csv")
        self.travel_distance = self.safe_load(TravelDistance, path + "Distance.csv")
        self.zone_destination = self.safe_load(ZoneDestinationTraffic, path + "ZoneDestination.csv")

    def safe_load(self, load_object_class, path):
        if not Path(path).exists():
            logging.warning(f" Cannot load from {path}: File does not exist.")
        else:
            return load_object_class.from_file(path)

    def print(self):
        self.traffic_demand.print()
        self.travel_time.print()
        self.travel_distance.print()
        self.zone_destination.print()

    def columns(self):
        return self.travel_time.columns()

    def reduce(self, keep_list):
        self.traffic_demand.reduce(keep_list)
        self.travel_time.reduce(keep_list)
        self.travel_distance.reduce(keep_list)

    def draw(self, reference=None, group="tripMode"):
        if reference is not None:
            x = self.traffic_demand.draw(reference=reference.traffic_demand, group=group)
            y = self.travel_time.draw(reference=reference.travel_time, group=group)
            z = self.travel_distance.draw(reference=reference.travel_distance, group=group)
        else:
            x = self.traffic_demand.draw(group=group)
            y = self.travel_time.draw(group=group)
            z = self.travel_distance.draw(group=group)
        return x, y, z

    def draw_smooth(self, reference=None):
        if reference is not None:
            x = self.traffic_demand.draw_smooth(reference.traffic_demand)
            y = self.travel_time.smoothen(3).draw(reference.travel_time.smoothen(3))
            z = self.travel_distance.smoothen(3).draw(reference.travel_distance.smoothen(3))
        else:
            x = self.traffic_demand.draw_smooth()
            y = self.travel_time.smoothen(3).draw()
            z = self.travel_distance.smoothen(3).draw()
        return x, y, z

        return x, y, z

    def draw_modal_split(self, reference=None):
        if reference is None:
            visualization.draw_modal_split(self)
        else:
            visualization.draw_modal_split([self, reference])

    def draw_distributions(self):
        self.travel_time.draw_all_distributions()
        self.travel_distance.draw_all_distributions()

    def get_modal_spliteeee(self, p):
        if type(p) is Parameter:
            assert len(p.requirements) == 1
            return self._get_modal_split(specific_mode_num=p.requirements["tripMode"])
        elif type(p) is int:
            return self._get_modal_split(specific_mode_num=p)

    def _modsplit_help(self, df, mode_list=[0, 1, 2, 3, 4]):
        x = df.groupby("tripMode").sum()["count"].to_frame()
        x = x.reindex(mode_list, fill_value=0)
        x = x / x.sum()
        return x

    def get_modal_split_by_param(self, param, mode_list=[0, 1, 2, 3, 4]):
        df = self.travel_time.get_data_frame()
        requirements_without_trip_mode = copy.deepcopy(param.requirements)
        assert set(param.requirements.keys()).issubset(set(self.columns())), "Underlying data lacks columns required for the parameter"
        del requirements_without_trip_mode["tripMode"]

        if len(requirements_without_trip_mode) > 0: # If a parameter does not work on a subset we don't need to build the subset
            df = df.loc[(df[list(requirements_without_trip_mode)] == pandas.Series(requirements_without_trip_mode)).all(axis=1)]
        ret = self._modsplit_help(df, mode_list)
        return ret.loc[param.requirements["tripMode"], "count"]

    def _get_modal_split(self, specific_mode_num=None, mode_list=[0, 1, 2, 3, 4]):
        ret = self._modsplit_help(self.travel_time.get_data_frame(), mode_list)
        if specific_mode_num is not None:
            assert specific_mode_num in mode_list
            return ret.loc[specific_mode_num, "count"]
        else:
            return ret

    def get_grouped_modal_split(self, column_names=None, mode_list=[0, 1, 2, 3, 4]):
        if column_names is None or column_names == []:
            return self._get_modal_split()
        assert "tripMode" not in column_names
        df = self.travel_time.get_data_frame()
        temp = df.groupby(column_names)
        s_list = []
        for key, group in temp:
            ret = self._modsplit_help(group, mode_list).squeeze()
            if type(key) is tuple:
                ret.name = ",".join([str(x)[:1] for x in key])
            else:
                ret.name = key
            s_list.append(ret)
        df = pandas.concat(s_list, axis=1, keys=[s.name for s in s_list])
        return df

    def get_modal_split_based_by_time(self, precision, mode_list=[0, 1, 2, 3, 4]):
        agg = aggregate(self.travel_time.get_data_frame(), precision, "durationTrip")
        maximum = agg.index.get_level_values(1).max()
        # modal split
        idx = pandas.MultiIndex.from_product([mode_list, list(range(1, maximum + 1))], names=['tripMode', 'durationTrip'])
        agg = agg.reindex(idx, fill_value=0)

        y = agg.groupby(level=1).sum()
        t = agg.join(y,  lsuffix='', rsuffix='_full')
        t["modal_split"] = t["count"] / t["count_full"]
        t = t.fillna(0)
        return t["modal_split"]


def help_difference_builder(original, comparison, method, string):
    diff = original - comparison
    return method(diff[string], diff[string + "_original"], diff[string + "_comparison"])


def help_difference_builder_all(original, comparison, method, string):
    diff = original.sub_all(comparison)
    return method(diff[string], diff[string + "_original"], diff[string + "_comparison"])


def help_difference_builder_none(original, comparison, method, string):
    diff = original.sub_none(comparison)
    return method(diff[string], diff[string + "_original"], diff[string + "_comparison"])


def help_modal_split(original, comparison, method, string):
    diff = original - comparison
    return method(diff.squeeze(), original.squeeze(), comparison.squeeze())


def sse(original, comparison, string):
    x = original - comparison
    result = x[string] ** 2
    return -result.sum()


def root_mean_squared_error(diff, original=None, comparison=None):
    return math.sqrt(sum_squared_error(diff, original, comparison) / diff.size)


def sum_squared_percent_error(diff, original=None, comparison=None):
    frac = diff / comparison
    frac.replace(numpy.inf, numpy.NaN, inplace=True)
    frac.dropna(inplace=True)

    return (frac ** 2).sum()


def mean_average_error(diff, original=None, comparison=None):
    return diff.sum() / diff.size


def mean_absolute_error(diff, original=None, comparison=None):
    return numpy.abs(diff).sum() / diff.size


def sum_squared_error(diff, original=None, comparison=None):
    x = diff ** 2
    y = x.sum()

    return y


def mean_sum_squared_error(diff, original=None, comparison=None):
    return (diff ** 2).sum() / diff.size


def theils_inequality(diff, original=None, comparison=None):
    nominator = (diff ** 2).sum() / diff.size
    denominator1 = (original ** 2).sum() / original.size
    denominator2 = (comparison ** 2).sum() / comparison.size

    result = math.sqrt(nominator) / (math.sqrt(denominator1) + math.sqrt(denominator2))
    return result


def super_sse(original, comparison, string):
    if original is None or comparison is None:
        logging.warning(" Cannot calculate zone difference as one df is None")
        return None
    original_df = original.get_data_frame()
    comparison_df = comparison.get_data_frame()
    x = original_df - comparison_df
    result = x[string] ** 2
    temp = "activityType"
    business = result.loc[result.index.get_level_values(temp) == ActivityGroup.BUSINESS.value]  # Business
    shopping = result.loc[result.index.get_level_values(temp) == ActivityGroup.SHOPPING.value]  # Shopping
    service = result.loc[result.index.get_level_values(temp) == ActivityGroup.SERVICE.value]  # Service#
    rest = result.loc[(result.index.get_level_values(temp) != ActivityGroup.BUSINESS.value) &
                      (result.index.get_level_values(temp) != ActivityGroup.SHOPPING.value) &
                      (result.index.get_level_values(temp) != ActivityGroup.SERVICE.value)]
    return -business.sum(), -shopping.sum(), -service.sum(), -rest.sum()


FUNCTIONS = [sum_squared_error, mean_absolute_error, mean_average_error,
             root_mean_squared_error, theils_inequality, sum_squared_percent_error,
             mean_sum_squared_error]


class Comparison:

    def __init__(self, input_data, comparison_data):
        self.metrics = {}
        self.apply_on_all_sub_methods(input_data.travel_time, comparison_data.travel_time, "TravelTime", "count")
        self.apply_on_all_sub_methods(input_data.traffic_demand, comparison_data.traffic_demand, "TrafficDemand", "active_trips")

        self.apply_on_all_sub_methods(input_data.traffic_demand.aggregate_time(5), comparison_data.traffic_demand.aggregate_time(5), "TrafficDemand5min",
                                      "active_trips")
        self.apply_on_all_sub_methods(input_data.traffic_demand.aggregate_time(15), comparison_data.traffic_demand.aggregate_time(15), "TrafficDemand15min",
                                      "active_trips")
        self.apply_on_all_sub_methods(input_data.traffic_demand.aggregate_time(60), comparison_data.traffic_demand.aggregate_time(60), "TrafficDemand60min",
                                      "active_trips")
        self.do_all_modal_splits(input_data, comparison_data)
        #self.apply_on_all_sub_methods(input_data._get_modal_split(), comparison_data._get_modal_split, "ModalSplit", "count")

        if "tripMode" in input_data.columns():
            x = copy.deepcopy(input_data)

            y = copy.deepcopy(comparison_data)
            #self.temp_val = sse(x.travel_time.get_data_frame(), y.travel_time.get_data_frame(), "count")
            x.reduce(["tripMode"])
            y.reduce(["tripMode"])
            self.modal_split = sse(x._get_modal_split(), y._get_modal_split(), "count")
            self.travel_time = sse(x.travel_time.get_data_frame(), y.travel_time.get_data_frame(), "count")
            self.travel_demand = sse(x.traffic_demand, y.traffic_demand, "active_trips")
        else:
            self.modal_split = numpy.inf
            self.travel_time = numpy.inf
            self.travel_demand = numpy.inf
        self.zone_traffic = super_sse(input_data.zone_destination, comparison_data.zone_destination, "traffic")
        if self.zone_traffic is None:
            self.zone_traffic = (numpy.inf, numpy.inf)

        print(self.metrics)


    def do_all_modal_splits(self, input_obj, comparison_obj):
        if len(input_obj.columns()) >= 2:
            x = input_obj.columns()
            x.remove("tripMode")
            for func in FUNCTIONS:
                x = help_modal_split(input_obj.get_grouped_modal_split(), comparison_obj.get_grouped_modal_split(),
                                     func, "EH")
                self.metrics["MODALSPLITVERYDETAILED" + func.__name__] = x

        else:
            for func in FUNCTIONS:
                x = numpy.inf
                self.metrics["MODALSPLITVERYDETAILED" + func.__name__] = x

        for func in FUNCTIONS:
            x = help_modal_split(input_obj.get_grouped_modal_split(), comparison_obj.get_grouped_modal_split(), func, "EH")
            self.metrics["MODALSPLIT" + func.__name__] = x

    def apply_on_all_sub_methods(self, input_obj, comparison_obj, name, string):
        self.apply_all_metrics(input_obj, comparison_obj, name + "TripMode", string)
        self.apply_all_metrics_detailed(input_obj, comparison_obj, name + "All", string)
        self.apply_all_metrics_generic(input_obj, comparison_obj, name , string)

    def __helper(self, input_obj, comparison_obj, name, metric_func, string):
        for func in FUNCTIONS:
            x = metric_func(input_obj, comparison_obj, func, string)
            self.metrics[name + func.__name__] = x

    def apply_all_metrics_detailed(self, input_obj, comparison_obj, name, string):
        self.__helper(input_obj, comparison_obj, name, help_difference_builder_all, string)

    def apply_all_metrics(self, input_obj, comparison_obj, name, string):
        self.__helper(input_obj, comparison_obj, name, help_difference_builder, string)

    def apply_all_metrics_generic(self, input_obj, comparison_obj, name, string):
        self.__helper(input_obj, comparison_obj, name, help_difference_builder_none, string)


    def sum_zones(self):
        return sum(list(self.zone_traffic))

    def __str__(self):
        return ", ".join([str(x) for x in [self.modal_split, self.travel_time, self.travel_demand, self.sum_zones()]])



