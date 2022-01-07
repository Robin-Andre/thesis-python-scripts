import evaluation
import visualization
from metrics import metric
from metrics.metric import Metric, get_distribution, get_all_existing_modes, get_approximations, difference


class TravelDistance(Metric):
    def read_from_raw_data(self, raw_data):
        self._data_frame = evaluation.create_travel_distance_data(raw_data)

    def draw(self):
        return self.draw_all_distributions()
        #print(visualization.draw_travel_distance(self._data_frame))

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

    def approximations(self):
        return get_approximations(self._data_frame, "distanceInKm")

    @classmethod
    def difference_t(cls, data1, data2, function, resolution=1, normalize=False):
        return difference(data1, data2, function, resolution=resolution, aggregate_string="distanceInKm",
                          normalize=normalize)
