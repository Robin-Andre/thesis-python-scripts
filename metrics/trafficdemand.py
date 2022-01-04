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
        """
        Returns a series of data based on the specific mode
        :param mode_number:
        :return:
        """
        temp = self._data_frame.copy()
        if mode_number == -1:
            temp = temp.groupby(["time"]).sum()
        else:
            temp = temp[temp["tripMode"] == mode_number]
            temp = temp.set_index("time")
        temp = temp.drop(columns=["tripMode"])  # Trip mode is no longer required and should therefore not be passed
        return temp.squeeze()

    def get_peak(self, interval, mode=-1):
        data = self.get_mode_specific_data(mode)
        data = data[interval[0]:interval[1]]
        return data.idxmax(), data.max()

    def get_week_peaks(self, mode=-1):
        begin = [0, 1440, 2880, 4320, 5760, 7200, 8640]
        end = [1440, 2880, 4320, 5760, 7200, 8640, 10080]
        return [self.get_peak(x, mode) for x in zip(begin, end)]


    def get_activity_specific_data(self, activity_number):
        # TODO implement
        pass



    @classmethod
    def difference_t(cls, data1, data2, function, resolution=1, normalize=False):
        return difference(data1, data2, function, resolution=resolution, aggregate_string="amount", normalize=normalize)
