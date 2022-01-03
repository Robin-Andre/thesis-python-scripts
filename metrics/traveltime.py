import evaluation
import visualization
from metrics import metric
from metrics.metric import Metric, get_distribution, get_all_existing_modes, get_approximations, difference


class TravelTime(Metric):
    def read_from_raw_data(self, raw_data):
        self._data_frame = evaluation.create_travel_time_data(raw_data)

    def draw(self, resolution=1):
        print(visualization.draw_travel_time(self._data_frame))

    def draw_distribution(self, mode=-1):
        distribution, pdf = self.get_distribution_and_pdf(mode)
        visualization.draw_distribution(distribution, mode, pdf)

    def get_distribution_and_pdf(self, mode):
        distribution = get_distribution(self._data_frame, "durationTrip", group=mode)
        pdf, _, _ = metric.get_fit_and_error_from_dataframe(self._data_frame, "durationTrip", mode)
        return distribution, pdf

    def draw_all_distributions(self):
        x, y, z = [], [], []
        for i in get_all_existing_modes(self._data_frame):
            distribution, pdf = self.get_distribution_and_pdf(i)
            x.append(distribution)
            y.append(i)
            z.append(pdf)
        visualization.draw_all_distributions(x, y, z)

    def approximations(self):
        return get_approximations(self._data_frame, "durationTrip")



    @classmethod
    def difference_t(cls, data1, data2, function, resolution=1, normalize=False):
        return difference(data1, data2, function, resolution=resolution, aggregate_string="durationTrip",
                          normalize=normalize)
