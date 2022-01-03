import evaluation
import visualization
from metrics.metric import Metric, difference


class TrafficDemand(Metric):

    def read_from_raw_data(self, raw_data):
        temp = raw_data[["tripBegin", "tripEnd", "tripMode"]].groupby("tripMode")
        temp = temp.apply(lambda x: evaluation.create_plot_data(x)).reset_index()
        assert temp["level_1"].equals(temp["time"])  # TODO figure out where the "level_1" comes from
        temp = temp.drop(columns=["level_1"])
        self._data_frame = temp

    def draw(self, resolution=1):
        temp = self._data_frame[self._data_frame["time"] % resolution == 0]
        visualization.draw(temp, visualization.aggregate_traffic_modal)

    def get_mode_specific_data(self, mode_number):
        temp = self._data_frame.copy()
        if mode_number == -1:
            temp = temp.groupby(["time"]).sum()
        else:
            temp = temp[temp["tripMode"] == mode_number]
            temp = temp.set_index("time")
        return temp



    @classmethod
    def difference_t(cls, data1, data2, function, resolution=1, normalize=False):
        return difference(data1, data2, function, resolution=resolution, aggregate_string="amount", normalize=normalize)
