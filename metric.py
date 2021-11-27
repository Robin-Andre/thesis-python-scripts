import logging
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

    def draw(self, resolution=1):
        pass

    def difference(self, metric, resolution=1):
        pass

    def verify(self):
        return True

    def print(self):
        print(self.data_frame)

    def write(self, path):
        self.data_frame.to_csv(path, index=False)

    def read(self, path):
        pass


class TrafficDemand(Metric):

    def read_from_raw_data(self, raw_data):
        temp = raw_data[["tripBegin", "tripEnd", "tripMode"]].groupby("tripMode")
        temp = temp.apply(lambda x: evaluation.create_plot_data(x)).reset_index()
        assert temp["level_1"].equals(temp["time"])  # TODO figure out where the "level_1" comes from
        temp = temp.drop(columns=["level_1"])
        self.data_frame = temp

    def draw(self, resolution=1):
        visualization.draw(self.data_frame, visualization.aggregate_traffic_modal)
        pass

    def difference(self, metric, resolution=1):
        pass

    def verify(self):
        pass


class TravelTime(Metric):
    def read_from_raw_data(self, raw_data):
        self.data_frame = evaluation.create_travel_time_data(raw_data)

    def draw(self, resolution=1):
        print(visualization.draw_travel_time(self.data_frame))

    def difference(self, metric, resolution=1):
        pass

    def verify(self):
        pass


class TravelDistance(Metric):
    def read_from_raw_data(self, raw_data):
        self.data_frame = evaluation.create_travel_distance_data(raw_data)

    def draw(self, resolution=1):
        print(visualization.draw_travel_distance(self.data_frame))

    def difference(self, metric, resolution=1):
        pass

    def verify(self):
        pass


class Data:
    def __init__(self, raw_data):
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
