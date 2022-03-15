import evaluation
from metrics.metric import Metric


class TravelCost(Metric):

    def read_from_raw_data(self, raw_data):
        self._data_frame = evaluation.create_travel_cost_data(raw_data)