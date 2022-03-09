from matplotlib import pyplot as plt

import evaluation
import visualization
from metrics import metric
from metrics.metric import Metric, get_distribution, get_all_existing_modes, get_approximations, difference


def subtract(df_self, df_other, keep_list=["tripMode"]):
    x = metric.reduce(df_self, keep_list, "durationTrip", "count")
    x = x.set_index(keep_list + ["durationTrip"])
    y = metric.reduce(df_other, keep_list, "durationTrip", "count")
    y = y.set_index(keep_list + ["durationTrip"])
    q = x.join(y, how="outer", lsuffix='_original', rsuffix='_comparison')
    q = q.fillna(0)
    q["count"] = q["count_original"] - q["count_comparison"]
    #q = q.drop(columns=["count_original", "count_comparison"])
    return q


class TravelTime(Metric):
    def __sub__(self, other):
        return subtract(self.get_data_frame(), other.get_data_frame())

    def sub_all(self, other):
        intersection = list(self.columns() & other.columns())
        return subtract(self.get_data_frame(), other.get_data_frame(), intersection)

    def sub_none(self, other):
        return subtract(self.get_data_frame(), other.get_data_frame(), [])

    def columns(self):
        cols = list(self._data_frame.columns.values)
        cols.remove("durationTrip")
        cols.remove("count")
        return set(cols)

    def smoothen(self, smoothness_in_minutes):
        ret = TravelTime()
        ret._data_frame = super().smoothen(smoothness_in_minutes, "count")
        return ret

    def read_from_raw_data(self, raw_data):
        self._data_frame = evaluation.create_travel_time_data_new(raw_data)

    def draw(self, group="tripMode", reference=None):
        temp = metric.reduce(self._data_frame, [group], "durationTrip", "count")
        temp2 = None
        if reference is not None:
            temp2 = metric.reduce(reference._data_frame, [group], "durationTrip", "count")
        return visualization.generic_plot(temp, group, "count", "durationTrip", reference_df=temp2)

    def reduce(self, keeper_list):
        self._data_frame = metric.reduce(self._data_frame, keeper_list, "durationTrip", "count")

    def draw_distribution(self, mode=-1):
        distribution, pdf = self.get_distribution_and_pdf(mode)
        visualization.draw_distribution(distribution, mode, pdf)

    def get_distribution_and_pdf(self, mode):
        distribution = get_distribution(self._data_frame, "durationTrip", group=mode)
        pdf, _, _ = metric.get_fit_and_error_from_dataframe(self._data_frame, "durationTrip", mode)
        return distribution, pdf

    def pdf(self, mode):
        distribution = get_distribution(self._data_frame, "durationTrip", group=mode)
        return distribution

    def cdf(self, mode):
        temp = self.pdf(mode)
        temp["x"] = temp["count"].cumsum()
        return temp["x"]

    def draw_all_distributions(self):
        x, y, z = [], [], []
        for i in get_all_existing_modes(self._data_frame):
            distribution, pdf = self.get_distribution_and_pdf(i)
            x.append(distribution)
            y.append(i)
            z.append(pdf)
        return visualization.draw_all_distributions(x, y, z)

    def approximations(self):
        return get_approximations(self._data_frame, "durationTrip")

    def get_mode_specific_data(self, mode_number):
        return super().get_mode_specific_data(mode_number, "durationTrip")

    @classmethod
    def difference_t(cls, data1, data2, function, resolution=1, normalize=False):
        return difference(data1, data2, function, resolution=resolution, aggregate_string="durationTrip",
                          normalize=normalize)
