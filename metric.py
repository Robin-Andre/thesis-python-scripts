import logging

import numpy
import numpy as np
import pandas
import scipy
from matplotlib import pyplot as plt

import evaluation
import metric
import visualization

default_path = "output/calibration/throwaway/"


def get_all_existing_modes(data_frame):
    """
    Outsourced method to get all existing modes in a dataframe to easily change representative of all modes

    :param data_frame: data frame with a tripMode column
    :return: a list with all mode identifiers of the dataframe and -1 as temporary placeholder for all modes
    """
    return np.insert(data_frame.tripMode.unique(), 0, -1)


class Metric:

    def __init__(self):
        self.data_frame = None

    def read_from_raw_data(self, raw_data):
        pass

    @classmethod
    def from_file(cls, file_path):
        obj = cls()
        obj.data_frame = pandas.read_csv(file_path)
        return obj

    @classmethod
    def from_raw_data(cls, raw_data):
        obj = cls()
        obj.read_from_raw_data(raw_data)
        return obj

    def get_data_frame(self):
        return self.data_frame.copy()

    def draw(self, resolution=1):
        pass

    def verify(self):
        return True

    def print(self):
        print(self.data_frame)

    def write(self, path):
        self.data_frame.to_csv(path, index=False)


class TrafficDemand(Metric):

    def read_from_raw_data(self, raw_data):
        temp = raw_data[["tripBegin", "tripEnd", "tripMode"]].groupby("tripMode")
        temp = temp.apply(lambda x: evaluation.create_plot_data(x)).reset_index()
        assert temp["level_1"].equals(temp["time"])  # TODO figure out where the "level_1" comes from
        temp = temp.drop(columns=["level_1"])
        self.data_frame = temp

    def draw(self, resolution=1):
        temp = self.data_frame[self.data_frame["time"] % resolution == 0]
        visualization.draw(temp, visualization.aggregate_traffic_modal)

    def verify(self):
        pass

    @classmethod
    def difference(cls, data1, data2, function, resolution=1, normalize=False):
        return difference(data1, data2, function, resolution=resolution, normalize=normalize)


class TravelTime(Metric):
    def read_from_raw_data(self, raw_data):
        self.data_frame = evaluation.create_travel_time_data(raw_data)

    def draw(self, resolution=1):
        print(visualization.draw_travel_time(self.data_frame))

    def draw_distribution(self, mode=-1):
        distribution = get_distribution(self.data_frame, "durationTrip", group=mode)
        pdf, _, _ = metric.get_fit_and_error_from_dataframe(self.data_frame, "durationTrip", mode)
        visualization.draw_distribution(distribution, mode, pdf)

    def draw_all_distributions(self):
        x, y, z = [], [], []
        for i in get_all_existing_modes(self.data_frame):
            distribution = get_distribution(self.data_frame, "durationTrip", group=i, quantile=0.99)
            pdf, _, _ = metric.get_fit_and_error_from_dataframe(self.data_frame, "durationTrip", i, quantile=0.99)
            x.append(distribution)
            y.append(i)
            z.append(pdf)
        visualization.draw_all_distributions(x, y, z)

    def difference(self, metric, resolution=1):
        pass

    def verify(self):
        pass

    def approximations(self):
        approxis = []
        for i in get_all_existing_modes(self.data_frame):
            _, data, error = metric.get_fit_and_error_from_dataframe(self.data_frame, "durationTrip", i)
            approxis.append([i, data, error])
        return approxis

    @classmethod
    def difference(cls, data1, data2, function, resolution=1, normalize=False):
        return difference(data1, data2, function, resolution=resolution, aggregate_string="durationTrip",
                          normalize=normalize)


class TravelDistance(Metric):
    def read_from_raw_data(self, raw_data):
        self.data_frame = evaluation.create_travel_distance_data(raw_data)

    def draw(self, resolution=1):
        print(visualization.draw_travel_distance(self.data_frame, bin_size=resolution))

    def verify(self):
        pass

    def draw_distribution(self, mode=-1):
        distribution = get_distribution(self.data_frame, "distanceInKm", group=mode)
        pdf, _, _ = metric.get_fit_and_error_from_dataframe(self.data_frame, "distanceInKm", mode)
        visualization.draw_distribution(distribution, mode, pdf)

    def draw_all_distributions(self):
        x, y, z = [], [], []
        for i in get_all_existing_modes(self.data_frame):
            distribution = get_distribution(self.data_frame, "distanceInKm", group=i, quantile=0.99)
            pdf, _, _ = metric.get_fit_and_error_from_dataframe(self.data_frame, "distanceInKm", i, quantile=0.99)
            x.append(distribution)
            y.append(i)
            z.append(pdf)
        visualization.draw_all_distributions(x, y, z)

    def approximations(self):
        approxis = []
        for i in get_all_existing_modes(self.data_frame):
            _, data, error = metric.get_fit_and_error_from_dataframe(self.data_frame, "distanceInKm", i)
            approxis.append([i, data, error])
        return approxis
    @classmethod
    def difference(cls, data1, data2, function, resolution=1, normalize=False):
        return difference(data1, data2, function, resolution=resolution, aggregate_string="distanceInKm",
                          normalize=normalize)


class Data:
    def __init__(self, raw_data=None):
        if raw_data is None:
            self.traffic_demand = None
            self.travel_time = None
            self.travel_distance = None
            return

        self.traffic_demand = TrafficDemand.from_raw_data(raw_data)
        self.travel_time = TravelTime.from_raw_data(raw_data)
        self.travel_distance = TravelDistance.from_raw_data(raw_data)

    def __eq__(self, other):
        return self.traffic_demand.data_frame.equals(other.traffic_demand.data_frame)\
               and self.travel_time.data_frame.equals(other.travel_time.data_frame) \
               and self.travel_distance.data_frame.equals(other.travel_distance.data_frame)

    def empty(self):
        return all(v is None for v in [self.traffic_demand, self.travel_time, self.travel_distance])

    def write(self, path="dump\\"):
        self.traffic_demand.write(path + "Demand.csv")
        self.travel_time.write(path + "Time.csv")
        self.travel_distance.write(path + "Distance.csv")

    def load(self, path="dump\\"):
        self.traffic_demand = TrafficDemand.from_file(path + "Demand.csv")
        self.travel_time = TravelTime.from_file(path + "Time.csv")
        self.travel_distance = TravelDistance.from_file(path + "Distance.csv")

    def print(self):
        self.traffic_demand.print()
        self.travel_time.print()
        self.travel_distance.print()

    def draw(self, resolution=[1, 1, 1]):
        self.traffic_demand.draw(resolution=resolution[0])
        self.travel_time.draw(resolution=resolution[1])
        self.travel_distance.draw(resolution=resolution[2])

    def get_neural_training_data(self):
        test = self.get_modal_split()
        approxis_time = self.travel_time.approximations()
        approxis_distance = self.travel_distance.approximations()
        return test["amount"], approxis_time, approxis_distance

    def draw_distributions(self):
        self.travel_time.draw_all_distributions()
        self.travel_distance.draw_all_distributions()

    def get_modal_split(self):
        agg = aggregate(self.travel_time.get_data_frame(), numpy.inf, "durationTrip")
        agg = agg.droplevel(1)  # Drops "durationTrip" from index The aggregated information is irrelevant for the
        # modal split
        return agg / agg.sum()

    def compare(self, other):
        pass


def get_counts(data_frame, value, group=-1, resolution=1, quantile=1.0):
    """
    This method takes a subset of the dataframe by the group parameter and returns the count of how often
    the values has been observed in the simulation.
    Requires: a dataframe containing a column named "Amount"
    :param data_frame: The Data Frame containing both a column named amount and an observation parameter
    :param value: The name of the observation used to differentiate between travel time and travel distance
    dataframes
    :param group: which trip mode shall be returned (-1 for all trip modes together)
    :param resolution: in case that the precision is too fine a higher resolution aggregates all values between 0 .. x
    into one data point
    :param quantile: cuts off all data exceeding the quantile (useful if there are few far outliers in the data)
    :return: A series containing the counts
    """
    temp = data_frame.copy()
    if group == -1:
        temp = temp.groupby([value]).sum()
    else:
        temp = temp[temp["tripMode"] == group]
        temp = temp.set_index(value)

    temp = temp.reset_index()

    temp[value] = (temp[value] // resolution)
    temp[value] = temp[value] * resolution

    temp = temp.groupby([value]).sum()
    sum_of_all = temp["amount"].sum()
    temp["cumsum"] = temp["amount"].cumsum()
    temp = temp[temp["cumsum"] <= quantile * sum_of_all]
    # Neither the cumulative sum nor trip mode are required to be held
    temp = temp.drop(columns=["tripMode", "cumsum"])
    return temp


def get_distribution(data_frame, value, group=-1, resolution=1, quantile=1.0):
    """
    Returns the probability density distribution of the data frame
    Behaves similar to get_counts but returns probabilities instead
    Required for plotting the data
    :param data_frame:
    :param value:
    :param group:
    :param resolution:
    :param quantile:
    :return:
    """
    temp = get_counts(data_frame, value, group, resolution, quantile)
    temp["amount"] = temp["amount"] / temp["amount"].sum()
    return temp


def aggregate(data_frame, resolution, aggregate_string):
    temp = data_frame.copy()
    temp[aggregate_string] = temp[aggregate_string] // resolution
    temp = temp.groupby(["tripMode", aggregate_string]).sum()
    return temp


# This method returns the values of the fitting to a dataframe it is more reliable to fit to an artificial sample instead
# of fitting to curve in scipy
def fit_distribution_to_data_frame(data_frame, rounding=100, distribution_name="gamma"):
    """
    This method returns the parameters of fitting a probability distribution to the underlying data. Since fitting a
    curve in scipy turns out to be significantly more unreliable than fitting a sample to a distribution this method
    creates an artificial sample by repeating the data points based on their occurrences rather than using the
    probability directly
    :param data_frame: a data frame holding the count (amount) of occurrences
    :param rounding: Reduces the sample size by integer division of the rounding value (large simulations contain
    unreasonably large sample sizes)
    :param distribution_name: The name of the distribution used for fitting (default: gamma)
    :return: the parameters required to reassemble the best fit of the chosen distribution
    """
    temp = data_frame.copy()
    temp["amount"] = temp["amount"] // rounding
    temp_ys = temp["amount"].values
    x = np.arange(len(temp.index))
    y = temp_ys
    all_points = numpy.repeat(x, y)
    dist = getattr(scipy.stats, distribution_name)
    params = dist.fit(all_points)

    return params


def dist_name_to_pdf(params, x, dist_name="gamma"):
    """
    This method returns a discrete number of points from a distribution for measurement and plotting purposes
    :param params: the parameters describing the distribution (args, loc, scale)
    :param x: an array of points at which the probability distribution should be evaluated
    :param dist_name: the distribution name as found in the scipy package
    :return: a list of values for the corresponding x values
    """
    dist = getattr(scipy.stats, dist_name)
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]
    if arg:
        pdf_fitted = dist.pdf(x, *arg, loc=loc, scale=scale)
    else:
        pdf_fitted = dist.pdf(x, loc=loc, scale=scale)
    return pdf_fitted


def get_fit_and_error_from_dataframe(data_frame, aggregation_string, mode_identifier=-1, dist_name="gamma", resolution=1, quantile=1):
    """

    :param data_frame:
    :param aggregation_string:
    :param mode_identifier:
    :param dist_name:
    :param resolution:
    :param quantile:
    :return:
    """
    savess = get_distribution(data_frame, aggregation_string, mode_identifier, resolution=resolution, quantile=quantile)
    counts = get_counts(data_frame, aggregation_string, mode_identifier, resolution=resolution, quantile=quantile)

    result = fit_distribution_to_data_frame(counts, rounding=100, distribution_name=dist_name)
    x = np.arange(len(savess))
    pdf_calc = dist_name_to_pdf(result, x, dist_name=dist_name)
    # TODO fix that an exponential approximation uses arbitrarily high values at 0
    if pdf_calc[0] > 1:
        pdf_calc[0] = 0

    sse = np.sum(np.power(savess["amount"] - pdf_calc, 2.0))
    # TODO plot precision needs to be set externally
    pdf = dist_name_to_pdf(result, np.linspace(0.05, int(savess.index.max()), 10 * int(savess.index.max())), dist_name=dist_name)
    #sse = 0
    return pdf, result, sse

# distanceInKm tripMode amount
# durationTrip tripMode amount
# tripMode time active_trips
def difference(data_frame1: pandas.DataFrame, data_frame_2, function, resolution=1, aggregate_string="time",
               normalize=False):
    temp = aggregate(data_frame1.data_frame, resolution, aggregate_string)
    temp_metric = aggregate(data_frame_2.data_frame, resolution, aggregate_string)
    if normalize:
        temp = temp / temp.sum()
        temp_metric = temp_metric / temp_metric.sum()
    curcur = pandas.concat([temp, temp_metric], axis=1).fillna(0)
    curcur["diff"] = function(curcur.iloc[:, 0], curcur.iloc[:, 1])
    return curcur["diff"]
