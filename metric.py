import logging

import numpy
import pandas

import evaluation
import visualization

default_path = "output/calibration/throwaway/"


class Metric:

    def __init__(self):
        self.data_frame = None

    def read_from_raw_data(self, raw_data):
        pass

    @classmethod
    def from_file(cls, file_path):
        obj = cls()
        obj.data_frame = pandas.read_csv(file_path)
        return obj

    @classmethod
    def from_raw_data(cls, raw_data):
        obj = cls()
        obj.read_from_raw_data(raw_data)
        return obj

    def get_data_frame(self):
        return self.data_frame.copy()

    def draw(self, resolution=1):
        pass

    def verify(self):
        return True

    def print(self):
        print(self.data_frame)

    def write(self, path):
        self.data_frame.to_csv(path, index=False)


class TrafficDemand(Metric):

    def read_from_raw_data(self, raw_data):
        temp = raw_data[["tripBegin", "tripEnd", "tripMode"]].groupby("tripMode")
        temp = temp.apply(lambda x: evaluation.create_plot_data(x)).reset_index()
        assert temp["level_1"].equals(temp["time"])  # TODO figure out where the "level_1" comes from
        temp = temp.drop(columns=["level_1"])
        self.data_frame = temp

    def draw(self, resolution=1):
        temp = self.data_frame[self.data_frame["time"] % resolution == 0]
        visualization.draw(temp, visualization.aggregate_traffic_modal)

    def verify(self):
        pass

    @classmethod
    def difference(cls, data1, data2, function, resolution=1, normalize=False):
        return difference(data1, data2, function, resolution=resolution, normalize=normalize)


class TravelTime(Metric):
    def read_from_raw_data(self, raw_data):
        self.data_frame = evaluation.create_travel_time_data(raw_data)

    def draw(self, resolution=1):
        print(visualization.draw_travel_time(self.data_frame))

    def difference(self, metric, resolution=1):
        pass

    def verify(self):
        pass

    @classmethod
    def difference(cls, data1, data2, function, resolution=1, normalize=False):
        return difference(data1, data2, function, resolution=resolution, aggregate_string="durationTrip",
                          normalize=normalize)


class TravelDistance(Metric):
    def read_from_raw_data(self, raw_data):
        self.data_frame = evaluation.create_travel_distance_data(raw_data)

    def draw(self, resolution=1):
        print(visualization.draw_travel_distance(self.data_frame, bin_size=resolution))

    def verify(self):
        pass

    @classmethod
    def difference(cls, data1, data2, function, resolution=1, normalize=False):
        return difference(data1, data2, function, resolution=resolution, aggregate_string="distanceInKm",
                          normalize=normalize)


class Data:
    def __init__(self, raw_data=None):
        if raw_data is None:
            self.traffic_demand = None
            self.travel_time = None
            self.travel_distance = None
            return

        self.traffic_demand = TrafficDemand.from_raw_data(raw_data)
        self.travel_time = TravelTime.from_raw_data(raw_data)
        self.travel_distance = TravelDistance.from_raw_data(raw_data)

    def write(self, path="dump\\"):
        self.traffic_demand.write(path + "Demand.csv")
        self.travel_time.write(path + "Time.csv")
        self.travel_distance.write(path + "Distance.csv")

    def load(self, path="dump\\"):
        self.traffic_demand = TrafficDemand.from_file(path + "Demand.csv")
        self.travel_time = TravelTime.from_file(path + "Time.csv")
        self.travel_distance = TravelDistance.from_file(path + "Distance.csv")

    def print(self):
        self.traffic_demand.print()
        self.travel_time.print()
        self.travel_distance.print()

    def draw(self, resolution=[1, 1, 1]):
        self.traffic_demand.draw(resolution=resolution[0])
        self.travel_time.draw(resolution=resolution[1])
        self.travel_distance.draw(resolution=resolution[2])

    def get_modal_split(self):
        agg = aggregate(self.travel_time.get_data_frame(), numpy.inf, "durationTrip")
        agg = agg.droplevel(1)  # Drops "durationTrip" from index The aggregated information is irrelevant for the
        # modal split
        return agg  / agg.sum()

    def compare(self, other):
        pass



def aggregate(data_frame, resolution, aggregate_string):
    temp = data_frame.copy()
    temp[aggregate_string] = temp[aggregate_string] // resolution
    temp = temp.groupby(["tripMode", aggregate_string]).sum()
    return temp


# distanceInKm tripMode amount
# durationTrip tripMode amount
# tripMode time active_trips
def difference(data_frame1: pandas.DataFrame, data_frame_2, function, resolution=1, aggregate_string="time",
               normalize=False):
    temp = aggregate(data_frame1.data_frame, resolution, aggregate_string)
    temp_metric = aggregate(data_frame_2.data_frame, resolution, aggregate_string)
    if normalize:
        temp = temp / temp.sum()
        temp_metric = temp_metric / temp_metric.sum()
    curcur = pandas.concat([temp, temp_metric], axis=1).fillna(0)
    curcur["diff"] = function(curcur.iloc[:, 0], curcur.iloc[:, 1])
    return curcur["diff"]
