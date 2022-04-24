import evaluation
import visualization
from metrics import metric
from metrics.metric import Metric, get_distribution, get_all_existing_modes, get_approximations, difference


def subtract(df_self, df_other, keep_list=["tripMode"]):
    x = metric.reduce(df_self, keep_list, "distanceInKm", "count")
    x = x.set_index(keep_list + ["distanceInKm"])
    y = metric.reduce(df_other, keep_list, "distanceInKm", "count")
    y = y.set_index(keep_list + ["distanceInKm"])
    q = x.join(y, how="outer", lsuffix='_original', rsuffix='_comparison')
    q = q.fillna(0)
    q["count"] = q["count_original"] - q["count_comparison"]
    #q = q.drop(columns=["count_original", "count_comparison"])
    return q


class TravelDistance(Metric):

    def __sub__(self, other):
        return subtract(self.get_data_frame(), other.get_data_frame())

    def sub_all(self, other):
        intersection = list(self.columns() & other.columns())
        return subtract(self.get_data_frame(), other.get_data_frame(), intersection)

    def sub_none(self, other):
        return subtract(self.get_data_frame(), other.get_data_frame(), [])

    def columns(self):
        cols = list(self._data_frame.columns.values)
        cols.remove("count")
        cols.remove("distanceInKm")
        return set(cols)

    def smoothen(self, smoothness_in_minutes):
        ret = TravelDistance()
        ret._data_frame = super().smoothen(smoothness_in_minutes, "count")
        return ret

    def read_from_raw_data_old(self, raw_data):
        self._data_frame = evaluation.create_travel_distance_data(raw_data)

    def read_from_raw_data(self, raw_data):
        self._data_frame = evaluation.create_travel_distance_data_new(raw_data)

    def reduce(self, keeper_list):
        self._data_frame = metric.reduce(self._data_frame, keeper_list, "distanceInKm", "count")

    def draw(self, group="tripMode", reference=None, suptitle=None):
        if type(group) is not list:
            listgroup = [group]
        else:
            listgroup = group
        temp = metric.reduce(self._data_frame, listgroup, "distanceInKm", "count")
        temp2 = None
        if reference is not None:
            temp2 = metric.reduce(reference._data_frame, listgroup, "distanceInKm", "count")

        col_seperator="tripMode"
        if "tripMode" not in listgroup:
            col_seperator = None
        return visualization.generic_plot(temp, group, "count", "distanceInKm", reference_df=temp2, color_seperator=col_seperator, sharex=False, suptitle=suptitle)


        #return visualization.draw_travel_distance_without_modes(self, reference)
        #temp = metric.reduce(self._data_frame, [], "distanceInKm", "count")
        #temp2 = None
        #if reference is not None:
        #    temp2 = metric.reduce(reference._data_frame, [], "distanceInKm", "count")
        #return visualization.generic_plot(temp, group, "count", "distanceInKm", reference_df=temp2)


    def get_mode_specific_data(self, mode_number):
        return super().get_mode_specific_data(mode_number, "distanceInKm")

    def draw_distribution(self, mode=-1):
        distribution = get_distribution(self._data_frame, "distanceInKm", group=mode)
        pdf, _, _ = metric.get_fit_and_error_from_dataframe(self._data_frame, "distanceInKm", mode)
        visualization.draw_distribution(distribution, mode, pdf)

    def draw_all_distributions(self):
        x, y, z = [], [], []
        for i in get_all_existing_modes(self._data_frame):
            distribution = get_distribution(self._data_frame, "distanceInKm", group=i, quantile=0.99)
            pdf, _, _ = metric.get_fit_and_error_from_dataframe(self._data_frame, "distanceInKm", i, quantile=0.99)
            x.append(distribution)
            y.append(i)
            z.append(pdf)
        return visualization.draw_all_distributions(x, y, z)

    def pdf(self, mode):
        distribution = get_distribution(self._data_frame, "distanceInKm", group=mode)
        return distribution

    def cdf(self, mode):
        temp = self.pdf(mode)
        temp["x"] = temp["count"].cumsum()
        return temp["x"]


    def approximations(self):
        return get_approximations(self._data_frame, "distanceInKm")

    @classmethod
    def difference_t(cls, data1, data2, function, resolution=1, normalize=False):
        return difference(data1, data2, function, resolution=resolution, aggregate_string="distanceInKm",
                          normalize=normalize)
