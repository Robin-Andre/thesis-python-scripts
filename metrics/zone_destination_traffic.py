import pandas

import evaluation
import visualization
from metrics.metric import Metric


class ZoneDestinationTraffic(Metric):

    def __sub__(self, other):
        return self._data_frame.sub(other._data_frame, fill_value=0)

    def read_from_raw_data(self, raw_data):
        self._data_frame = evaluation.create_zone_destination_traffic_data(raw_data)

    def write(self, path):
        self._data_frame.to_csv(path, index=True)

    @classmethod
    def from_file(cls, file_path):
        obj = cls()
        try:
            obj._data_frame = pandas.read_csv(file_path)
        except FileNotFoundError:
            return None
        obj._data_frame = obj._data_frame.set_index(["sourceZone", "targetZone", "activityType"])
        return obj

    def draw(self, reference=None):
        visualization.draw_zone_demand(self, reference)
