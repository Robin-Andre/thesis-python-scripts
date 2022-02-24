import copy

import numpy
import pandas

import visualization
from configurations.parameter import Parameter
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
        self.traffic_demand.write(path + "Demand.csv")
        self.travel_time.write(path + "Time.csv")
        self.travel_distance.write(path + "Distance.csv")
        self.zone_destination.write(path + "ZoneDestination.csv")

    def load(self, path="dump\\"):
        self.traffic_demand = TrafficDemand.from_file(path + "Demand.csv")
        self.travel_time = TravelTime.from_file(path + "Time.csv")
        self.travel_distance = TravelDistance.from_file(path + "Distance.csv")
        self.zone_destination = ZoneDestinationTraffic.from_file(path + "ZoneDestination.csv")

    def print(self):
        self.traffic_demand.print()
        self.travel_time.print()
        self.travel_distance.print()
        self.zone_destination.print()

    def columns(self):
        cols = list(self.travel_time.get_data_frame().columns.values)
        cols.remove("durationTrip")
        cols.remove("count")
        return set(cols)

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


def sse(original, comparison, string):
    x = original - comparison
    result = x[string] ** 2
    return -result.sum()


class Comparison:

    def __init__(self, input_data, comparison_data):
        x = copy.deepcopy(input_data)
        x.reduce(["tripMode"])
        y = copy.deepcopy(comparison_data)
        y.reduce(["tripMode"])
        self.modal_split = sse(x._get_modal_split(), y._get_modal_split(), "count")
        self.travel_time = sse(x.travel_time.get_data_frame(), y.travel_time.get_data_frame(), "count")
        self.travel_demand = sse(x.traffic_demand, y.traffic_demand, "active_trips")

    def __str__(self):
        return ", ".join([str(x) for x in [self.modal_split, self.travel_time, self.travel_demand]])



