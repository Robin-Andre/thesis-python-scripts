import evaluation
from metrics.metric import Metric


class ZoneDestinationTraffic(Metric):

    def __sub__(self, other):
        return self._data_frame.sub(other._data_frame, fill_value=0)
    def read_from_raw_data(self, raw_data):
        self._data_frame = evaluation.create_zone_destination_traffic_data(raw_data)