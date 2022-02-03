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
        return self.traffic_demand._data_frame.equals(other.traffic_demand._data_frame)\
               and self.travel_time._data_frame.equals(other.travel_time._data_frame) \
               and self.travel_distance._data_frame.equals(other.travel_distance._data_frame)

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

    def reduce(self, keep_list):
        self.traffic_demand.reduce(keep_list)
        self.travel_time.reduce(keep_list)
        self.travel_distance.reduce(keep_list)

    def draw(self, reference=None):
        if reference is not None:
            x = self.traffic_demand.draw(reference.traffic_demand)
            y = self.travel_time.draw(reference.travel_time)
            z = self.travel_distance.draw(reference.travel_distance)
        else:
            x = self.traffic_demand.draw()
            y = self.travel_time.draw()
            z = self.travel_distance.draw()
        return x, y, z

    def draw_smooth(self, reference=None):
        if reference is not None:
            x = self.traffic_demand.smoothen(60).draw(reference.traffic_demand.smoothen(60))
            y = self.travel_time.smoothen(3).draw(reference.travel_time.smoothen(3))
            z = self.travel_distance.smoothen(3).draw(reference.travel_distance.smoothen(3))
        else:
            x = self.traffic_demand.smoothen(60).draw()
            y = self.travel_time.smoothen(3).draw()
            z = self.travel_distance.smoothen(3).draw()
        return x, y, z

        return x, y, z


    def draw_distributions(self):
        self.travel_time.draw_all_distributions()
        self.travel_distance.draw_all_distributions()

    def get_modal_split(self, mode_list=[0, 1, 2, 3, 4]):
        agg = aggregate(self.travel_time.get_data_frame(), numpy.inf, "durationTrip")

        agg = agg.droplevel(1)  # Drops "durationTrip" from index The aggregated information is irrelevant for the
        # modal split
        agg = agg.reindex(mode_list, fill_value=0)
        return agg / agg.sum()


def sse(original, comparison, string):
    result = (original - comparison)[string] ** 2
    return -result.sum()


class Comparison:

    def __init__(self, input_data, comparison_data):
        self.modal_split = sse(input_data.get_modal_split(), comparison_data.get_modal_split(), "count")
        self.travel_time = sse(input_data.travel_time.get_data_frame(), comparison_data.travel_time.get_data_frame(), "count")
        self.travel_demand = sse(input_data.traffic_demand, comparison_data.traffic_demand, "active_trips")

    def __str__(self):
        return ", ".join([str(x) for x in [self.modal_split, self.travel_time, self.travel_demand]])



