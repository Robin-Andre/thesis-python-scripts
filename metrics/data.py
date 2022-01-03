import numpy

from metrics.metric import aggregate
from metrics.trafficdemand import TrafficDemand
from metrics.traveldistance import TravelDistance
from metrics.traveltime import TravelTime


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

    def __eq__(self, other):
        return self.traffic_demand.data_frame.equals(other.traffic_demand.data_frame)\
               and self.travel_time.data_frame.equals(other.travel_time.data_frame) \
               and self.travel_distance.data_frame.equals(other.travel_distance.data_frame)

    def empty(self):
        return all(v is None for v in [self.traffic_demand, self.travel_time, self.travel_distance])

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

    def get_neural_training_data(self):
        test = self.get_modal_split()
        approxis_time = self.travel_time.approximations()
        approxis_distance = self.travel_distance.approximations()
        return test["amount"], approxis_time, approxis_distance

    def draw_distributions(self):
        self.travel_time.draw_all_distributions()
        self.travel_distance.draw_all_distributions()

    def get_modal_split(self):
        agg = aggregate(self.travel_time.get_data_frame(), numpy.inf, "durationTrip")
        agg = agg.droplevel(1)  # Drops "durationTrip" from index The aggregated information is irrelevant for the
        # modal split
        return agg / agg.sum()

    def compare(self, other):
        pass