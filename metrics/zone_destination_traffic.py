import pandas

import evaluation
import visualization
from metrics import metric
from metrics.metric import Metric

def subtract(df_self, df_other, keep_list=["activityType"]):

    x = df_self.groupby(["sourceZone", "targetZone"] + keep_list).sum()
    y = df_other.groupby(["sourceZone", "targetZone"] + keep_list).sum()
    q = x.join(y, how="outer", lsuffix='_original', rsuffix='_comparison')
    q = q.fillna(0)
    q["traffic"] = q["traffic_original"] - q["traffic_comparison"]
    #q = q.drop(columns=["count_original", "count_comparison"])
    return q


class ZoneDestinationTraffic(Metric):

    def __sub__(self, other):
        return subtract(self.get_data_frame(), other.get_data_frame())

    def sub_none(self, other):
        return subtract(self.get_data_frame(), other.get_data_frame(), [])

    def sub_all(self, other):
        intersection = list(self.columns() & other.columns())
        return subtract(self.get_data_frame(), other.get_data_frame(), intersection)

    def columns(self):
        cols = list(self._data_frame.index.names)
        cols.remove("sourceZone")
        cols.remove("targetZone")
        return set(cols)

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
