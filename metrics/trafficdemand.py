import math

import numpy
import pandas

import evaluation
import visualization
from metrics.metric import Metric, difference, reduce


def fill_each_group(split_df, agg_list, method="ffill"):
    tmp = split_df.droplevel(agg_list)

    x = tmp.reindex(range(0, max(tmp.index.max(), 10080)), method=method)
    x = x.fillna(0)
    return x


def pad(df, agg_list):
    df = df.set_index(agg_list + ["time"])
    df = df.groupby(agg_list).apply(fill_each_group, agg_list)
    df = df.reset_index()
    return df



def subtract(trafdemand, trafdemand_other, keep_list=["tripMode"]):
    x = trafdemand.accumulate(keep_list)
    x = x.set_index(keep_list + ["time"])
    y = trafdemand_other.accumulate(keep_list)
    y = y.set_index(keep_list + ["time"])
    q = x.join(y, how="outer", lsuffix='_original', rsuffix='_comparison')
    q = q.fillna(method="ffill") # Important to ffill instead of 0
    q["active_trips"] = q["active_trips_original"] - q["active_trips_comparison"]

    #q = q.reset_index()
    return q


class TrafficDemand(Metric):

    def __sub__(self, other):
        return subtract(self, other)

    def sub_all(self, other):
        intersection = list(self.columns() & other.columns())
        return subtract(self, other, intersection)

    def sub_none(self, other):
        return subtract(self, other, [])

    def columns(self):
        cols = list(self._data_frame.columns.values)
        cols.remove("time")
        cols.remove("active_trips_delta")
        return set(cols)

    def columns_list(self):
        cols = list(self._data_frame.columns.values)
        cols.remove("time")
        cols.remove("active_trips_delta")
        return cols

    def smoothen(self, smoothness_in_minutes):
        ret = TrafficDemand()
        ret._data_frame = super().smoothen(smoothness_in_minutes, "active_trips_delta")
        return ret

    def aggregate_time(self, minute_interval):
        ret = TrafficDemand()
        temp = self._data_frame.copy()
        temp["time"] = (numpy.ceil(temp["time"] / minute_interval)).astype(int) * minute_interval
        temp = temp.groupby(self.columns_list() + ["time"]).sum()
        temp = temp.reset_index()
        ret._data_frame = temp
        return ret

    def read_from_raw_data_old(self, raw_data):
        temp = raw_data[["tripBegin", "tripEnd", "tripMode"]].groupby("tripMode")
        temp = temp.apply(lambda x: evaluation.create_plot_data(x)).reset_index()
        assert temp["level_1"].equals(temp["time"])  # TODO figure out where the "level_1" comes from
        temp = temp.drop(columns=["level_1"])
        self._data_frame = temp

    def read_from_raw_data(self, raw_data):
        self._data_frame = evaluation.create_traffic_demand_data(raw_data)

    def read_from_raw_data_new2(self, raw_data):
        self._data_frame = evaluation.create_traffic_demand_data(raw_data, ["tripMode"])

    def aggregate_delta(self, agg_list):
        return evaluation.aggregate_traffic_demand(self._data_frame, agg_list)

    def accumulate_padded(self, acc_list):
        temp = self.accumulate(acc_list)
        return pad(temp, acc_list)

    def accumulate(self, acc_list):
        temp = reduce(self._data_frame, acc_list, "time", "active_trips_delta")
        temp = temp.drop(columns=["active_trips_delta"])
        data = reduce(self._data_frame, acc_list, "time", "active_trips_delta").drop(columns="time")
        if len(acc_list) == 0:
            data["active_trips"] = data.cumsum()
        else:
            data["active_trips"] = data.groupby(acc_list).cumsum()
        data["time"] = temp["time"]
        data = data.drop(columns=["active_trips_delta"])
        return data

    def reduce(self, keep_list):
        assert "time", "active_trips_delta" not in keep_list
        self._data_frame = reduce(self._data_frame, keep_list, "time", "active_trips_delta")

    def draw(self, reference=None, group=["tripMode"]):
        if reference is None:
            return visualization.draw_travel_demand_by_mode(self.accumulate(group), group="tripMode")
        else:
            return visualization.draw_travel_demand_by_mode(self.accumulate(group),
                                                            reference_df=reference.accumulate(group), group="tripMode")

    def draw_smooth(self, reference=None, smoothness_factor=60):
        df1 = self.accumulate_padded(["tripMode"])
        df1["active_trips"] = df1["active_trips"].rolling(smoothness_factor, center=True, min_periods=1).mean()
        if reference is None:
            return visualization.draw_travel_demand_by_mode(df1)
        else:
            df_r = reference.accumulate_padded(["tripMode"])
            df_r["active_trips"] = df_r["active_trips"].rolling(smoothness_factor, center=True, min_periods=1).mean()
            return visualization.draw_travel_demand_by_mode(df1,
                                                            reference_df=df_r)



    def get_mode_specific_data(self, mode_number):
        return super().get_mode_specific_data(mode_number, "time")

    def get_peak(self, interval, mode=-1):
        data = self.get_mode_specific_data(mode)
        data = data[interval[0]:interval[1]]
        return data.idxmax(), data.max()

    def get_week_peaks(self, mode=-1):
        begin = [0, 1440, 2880, 4320, 5760, 7200, 8640]
        end = [1440, 2880, 4320, 5760, 7200, 8640, 10080]
        return [self.get_peak(x, mode) for x in zip(begin, end)]



    @classmethod
    def difference_t(cls, data1, data2, function, resolution=1, normalize=False):
        return difference(data1, data2, function, resolution=resolution, aggregate_string="amount", normalize=normalize)
