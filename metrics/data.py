import copy
import logging
import math
import time
from operator import __sub__
from pathlib import Path

import numpy
import pandas
import scipy

import evaluation
import visualization
from configurations.parameter import Parameter, ActivityGroup
from metrics.metric import aggregate
from metrics.trafficdemand import TrafficDemand
from metrics.travelcost import TravelCost
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
            self.travel_costs = None
            return

        self.traffic_demand = TrafficDemand.from_raw_data(raw_data)
        self.travel_time = TravelTime.from_raw_data(raw_data)
        self.travel_distance = TravelDistance.from_raw_data(raw_data)
        self.zone_destination = ZoneDestinationTraffic.from_raw_data(raw_data)
        self.travel_costs = TravelCost.from_raw_data(raw_data)

    def __eq__(self, other):
        return self.traffic_demand._data_frame.equals(other.traffic_demand._data_frame)\
               and self.travel_time._data_frame.equals(other.travel_time._data_frame) \
               and self.travel_distance._data_frame.equals(other.travel_distance._data_frame) \
               and self.zone_destination._data_frame.equals(other.zone_destination._data_frame) \
               and self.travel_costs._data_frame.equals(other.travel_costs._data_frame)

    def empty(self):
        return all(v is None for v in [self.traffic_demand, self.travel_time, self.travel_distance])

    def write(self, path="dump\\"):
        self.safe_write(self.traffic_demand, path + "Demand.csv")
        self.safe_write(self.travel_time, path + "Time.csv")
        self.safe_write(self.travel_distance, path + "Distance.csv")
        self.safe_write(self.zone_destination, path + "ZoneDestination.csv")
        self.safe_write(self.travel_costs, path + "TravelCosts.csv")

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
        self.travel_costs = self.safe_load(TravelCost, path + "ZoneDestination.csv")

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
        self.travel_costs.print()

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


    def draw_with_title(self, reference=None, group="tripMode", title=""):
        if reference is not None:
            x = self.traffic_demand.draw(reference=reference.traffic_demand, group=group, title=title)
            y = self.travel_time.draw(reference=reference.travel_time, group=group, suptitle=title)
            z = self.travel_distance.draw(reference=reference.travel_distance, group=group, suptitle=title)
        else:
            x = self.traffic_demand.draw(group=group, title=title)
            y = self.travel_time.draw(group=group, suptitle=title)
            z = self.travel_distance.draw(group=group, suptitle=title)
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

    def _modsplit_help(self, df, mode_list=[0, 1, 2, 3, 4], divide=True):
        x = df.groupby("tripMode").sum()["count"].to_frame()
        x = x.reindex(mode_list, fill_value=0)
        if divide:
            x = x / x.sum()
        return x

    def get_modal_split_by_param(self, param, mode_list=[0, 1, 2, 3, 4], use_counts_instead=False):
        df = self.travel_time.get_data_frame()
        requirements_without_trip_mode = copy.deepcopy(param.requirements)
        assert set(param.requirements.keys()).issubset(set(self.columns())), "Underlying data lacks columns required for the parameter"
        del requirements_without_trip_mode["tripMode"]

        if len(requirements_without_trip_mode) > 0: # If a parameter does not work on a subset we don't need to build the subset
            df = df.loc[(df[list(requirements_without_trip_mode)] == pandas.Series(requirements_without_trip_mode)).all(axis=1)]
        ret = self._modsplit_help(df, mode_list, divide=(not use_counts_instead))
        return ret.loc[param.requirements["tripMode"], "count"]

    def _get_modal_split(self, specific_mode_num=None, mode_list=[0, 1, 2, 3, 4]):
        ret = self._modsplit_help(self.travel_time.get_data_frame(), mode_list)
        if specific_mode_num is not None:
            assert specific_mode_num in mode_list
            return ret.loc[specific_mode_num, "count"]
        else:
            return ret

    def get_grouped_modal_split(self, column_names=None, mode_list=[0, 1, 2, 3, 4], divide=True):
        if column_names is None or column_names == [] or len(column_names) > 1:
            return self._get_modal_split()

        assert "tripMode" not in column_names
        df = self.travel_time.get_data_frame()
        temp = df.groupby(column_names)
        s_list = []

        test = df.groupby(column_names + ["tripMode"]).sum()["count"].to_frame()
        element_list = list(set(df[column_names[0]]))
        index = pandas.MultiIndex.from_product([element_list, mode_list], names=[column_names[0], "tripMode"])
        crossboi = pandas.DataFrame(index=index).reset_index()
        test = test.reset_index()
        test = test.merge(crossboi, how="outer")
        test = test.fillna(0)
        test = test.set_index(column_names[0])




        looo = list(range(len(column_names)))
        test1 = test.groupby(level=looo).sum()["count"].to_frame()
        test1.rename(columns={"count": 'max'}, inplace=True)
        test2 = test.join(test1)
        test2["split"] = test2["count"] / test2["max"]
        test2 = test2.sort_values(by=[column_names[0], "tripMode"], ascending = [True, True])

        if divide:
            return test2["split"].to_frame()
        else:
            return test2["count"].to_frame()
        for key, group in temp:
            ret = self._modsplit_help(group, mode_list, divide).squeeze()
            if type(key) is tuple:
                ret.name = ",".join([str(x)[:4] for x in key])
            else:
                ret.name = key
            s_list.append(ret)
        df = pandas.concat(s_list, axis=1, keys=[s.name for s in s_list])
        return df

    def get_grouped_modal_count(self, column_names=None, mode_list=[0, 1, 2, 3, 4]):
        return self.get_grouped_modal_split(column_names, mode_list, divide=False)

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




def help_modal_split(diff, original, comparison, method):

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

    return (frac ** 2).sum().sum()


def mean_average_error(diff, original=None, comparison=None):
    return diff.sum().sum() / diff.size


def mean_absolute_error(diff, original=None, comparison=None):
    return numpy.abs(diff).sum().sum() / diff.size


def sum_squared_error(diff, original=None, comparison=None):
    x = diff ** 2
    y = x.sum()
    z = y.sum()
    return z


def sum_cubed_error(diff, original=None, comparison=None):
    return (numpy.abs(diff) ** 3).sum().sum()


def mean_sum_squared_error(diff, original=None, comparison=None):
    return (diff ** 2).sum().sum()  / diff.size


def theils_inequality(diff, original=None, comparison=None):
    nominator = (diff ** 2).sum().sum()  / diff.size
    denominator1 = (original ** 2).sum().sum()  / original.size
    denominator2 = (comparison ** 2).sum().sum()  / comparison.size

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
             mean_sum_squared_error, sum_cubed_error]


class Comparison:

    def __init__(self, input_data, comparison_data):
        self.mode_metrics = {}
        self.destination_metrics = {}

        self.apply_on_all_sub_methods(input_data.travel_distance, comparison_data.travel_distance, "TravelDistance",
                                      "count", use_dest_dict=True)
        self.apply_on_all_sub_methods(input_data.zone_destination, comparison_data.zone_destination, "ZoneDemand", "traffic", use_dest_dict=True)

        self.apply_on_all_sub_methods(input_data.travel_time, comparison_data.travel_time, "TravelTime", "count")

        self.apply_on_all_sub_methods(input_data.traffic_demand, comparison_data.traffic_demand, "TrafficDemand", "active_trips")

        self.apply_on_all_sub_methods(input_data.traffic_demand.aggregate_time(5), comparison_data.traffic_demand.aggregate_time(5), "TrafficDemand5min",
                                      "active_trips")

        self.apply_on_all_sub_methods(input_data.traffic_demand.aggregate_time(15), comparison_data.traffic_demand.aggregate_time(15), "TrafficDemand15min",
                                      "active_trips")

        self.apply_on_all_sub_methods(input_data.traffic_demand.aggregate_time(60), comparison_data.traffic_demand.aggregate_time(60), "TrafficDemand60min",
                                      "active_trips")

        self.do_all_modal_splits(input_data, comparison_data)

        self.do_all_modal_counts(input_data, comparison_data)
        self.statistic_tests = {}
        self.apply_count_statistic(input_data.travel_time, comparison_data.travel_time, "TravelTime")

        self.apply_count_statistic(input_data.traffic_demand, comparison_data.traffic_demand, "TrafficDemand")

        self.apply_count_statistic(input_data.travel_distance, comparison_data.travel_distance, "TravelDistance")

        self.apply_count_statistic(input_data.zone_destination, comparison_data.zone_destination, "Destinations")

        self.apply_statistic_tests(input_data.travel_time, comparison_data.travel_time, "time")

        self.apply_statistic_tests(input_data.travel_distance, comparison_data.travel_distance, "distance")

        self.modal_split = -self.mode_metrics["ModalSplit_Default_Splits_sum_squared_error"]
        self.travel_time = -self.mode_metrics["TravelTime_Default_sum_squared_error"]
        self.travel_demand = -self.mode_metrics["TrafficDemand_Default_sum_squared_error"]

        self.zone_traffic = super_sse(input_data.zone_destination, comparison_data.zone_destination, "traffic")
        if self.zone_traffic is None:
            self.zone_traffic = (numpy.inf, numpy.inf)

    def __helper2(self, input_obj, comparison_obj, funct, string):

        if len(input_obj.columns()) >= 2:
            cols = list(input_obj.columns())
            cols.remove("tripMode")

            original = funct(input_obj, cols)
            comparison = funct(comparison_obj, cols)

            temp = original.join(comparison, how="outer", lsuffix="or", rsuffix="comp")
            temp = temp.fillna(0)
            temp["diff"] = temp.iloc[:, 0] - temp.iloc[:,1]
            #diff.fillna(0)


            for func in FUNCTIONS:
                x = help_modal_split(temp.iloc[:, 2], temp.iloc[:, 0], temp.iloc[:,1], func)
                self.mode_metrics["ModalSplit_Detailed" + string + func.__name__] = x

        else:
            for func in FUNCTIONS:
                x = numpy.inf
                self.mode_metrics["ModalSplit_Detailed" + string + func.__name__] = x
        original = funct(input_obj)
        comparison = funct(comparison_obj)
        temp = original.join(comparison, how="outer", lsuffix="or", rsuffix="comp")
        temp = temp.fillna(0)
        temp["diff"] = temp.iloc[:, 0] - temp.iloc[:, 1]
        for func in FUNCTIONS:

            x = help_modal_split(temp.iloc[:, 2], temp.iloc[:, 0], temp.iloc[:,1], func)
            self.mode_metrics["ModalSplit_Default" + string + func.__name__] = x

    def do_all_modal_splits(self, input_obj, comparison_obj):
        self.__helper2(input_obj, comparison_obj, Data.get_grouped_modal_split, "_Splits_")

    def do_all_modal_counts(self, input_obj, comparison_obj):
        self.__helper2(input_obj, comparison_obj, Data.get_grouped_modal_count, "_Counts_")

    def apply_statistic_tests(self, input, comparison, name):
        mode_list = {"all": -1, "bike": 0, "car": 1, "passenger":2, "pedestrian": 3, "public_transport": 4}
        tests = {"ks": scipy.stats.kstest, "ttest": scipy.stats.ttest_ind, "ranksums": scipy.stats.ranksums}
        for mode_name, x in mode_list.items():
            inp = input.cdf(x)
            comp = comparison.cdf(x)
            for test_name, test in tests.items():

                if len(inp) == 0 or len(comp) == 0:
                    self.statistic_tests[name + "_" + test_name + "_" + mode_name] = numpy.inf
                else:

                    _, p_value = test(inp, comp)
                    self.statistic_tests[name + "_" + test_name + "_" + mode_name] = p_value

    def apply_count_statistic(self, input, comparison, name):
        tests = {"wilcoxon": scipy.stats.wilcoxon, "ttest": scipy.stats.ttest_rel, "ks": scipy.stats.ks_2samp}
        d_names = ["default", "aggegated_none", "all"]
        if input is None or comparison is None:
            for d_name in d_names:
                for test_name in tests.keys():
                    self.statistic_tests["CountComparisonStatisticTest_" + name + "_" + test_name + "_" + d_name] = numpy.inf
            return

        diff = input - comparison
        diff2 = input.sub_none(comparison)
        diff3 = input.sub_all(comparison)
        for d_name, d in zip(d_names, [diff, diff2, diff3]):
            for test_name, teste in tests.items():
                temp = d[d.columns[2]] == 0
                if temp.all():
                    p_value = 1
                else:
                    x, p_value = teste(d[d.columns[0]], d[d.columns[1]])

                self.statistic_tests["CountComparisonStatisticTest_" + name + "_" + test_name + "_" + d_name] = p_value


    def apply_on_all_sub_methods(self, input_obj, comparison_obj, name, string, use_dest_dict=False):
        self.apply_all_metrics(input_obj, comparison_obj, name + "_All_", string, use_dest_dict)
        self.apply_all_metrics_detailed(input_obj, comparison_obj, name + "_Default_", string, use_dest_dict)
        self.apply_all_metrics_generic(input_obj, comparison_obj, name + "_None_", string, use_dest_dict)

    def __helper(self, input_obj, comparison_obj, name, diff, string, use_dest_dict=False):
        for func in FUNCTIONS:
            if diff is None:
                x = numpy.inf
            else:
                x = func(diff[string], diff[string + "_original"], diff[string + "_comparison"])
                #x = metric_func(input_obj, comparison_obj, func, string)
            if use_dest_dict:
                self.destination_metrics[name + func.__name__] = x
            else:
                self.mode_metrics[name + func.__name__] = x

    def apply_all_metrics_detailed(self, input_obj, comparison_obj, name, string, use_dest_dict):
        if input_obj is None or comparison_obj is None:
            diff = None
        else:
            diff = input_obj - comparison_obj
        self.__helper(input_obj, comparison_obj, name, diff, string, use_dest_dict)

    def apply_all_metrics(self, input_obj, comparison_obj, name, string, use_dest_dict):
        if input_obj is None or comparison_obj is None:
            diff = None
        else:
            diff = input_obj.sub_all(comparison_obj)
        self.__helper(input_obj, comparison_obj, name, diff, string, use_dest_dict)

    def apply_all_metrics_generic(self, input_obj, comparison_obj, name, string, use_dest_dict):
        if input_obj is None or comparison_obj is None:
            diff = None
        else:
            diff = input_obj.sub_none(comparison_obj)
        self.__helper(input_obj, comparison_obj, name, diff, string, use_dest_dict)


    def sum_zones(self):
        return sum(list(self.zone_traffic))

    def mode_vals(self):
        return ", ".join([str(x) for x in list(self.mode_metrics.values())])

    def mode_keys(self, appendix):
        return ", ".join([str(x) + appendix for x in list(self.mode_metrics.keys())])

    def statistic_vals(self):
        return ", ".join([str(x) for x in list(self.statistic_tests.values())])

    def statistic_keys(self, appendix):
        return ", ".join([str(x) + appendix for x in list(self.statistic_tests.keys())])

    def destination_vals(self):
        return ", ".join([str(x) for x in list(self.destination_metrics.values())])

    def destination_keys(self, appendix):
        return ", ".join([str(x) + appendix for x in list(self.destination_metrics.keys())])

    def logger_vals(self):
        return self.mode_vals() + ", " + self.statistic_vals() + ", " + self.destination_vals()

    def logger_keys(self, appendix):
        return self.mode_keys(appendix) + ", " + self.statistic_keys(appendix) + ", " + self.destination_keys(appendix)

    def __str__(self):
        return ", ".join([str(x) for x in [self.modal_split, self.travel_time, self.travel_demand, self.sum_zones()]])



