import math

import numpy
import numpy as np
import pandas
import scipy
from scipy import stats

default_path = "output/calibration/throwaway/"


def get_all_existing_modes(data_frame):
    """
    Outsourced method to get all existing modes in a dataframe to easily change representative of all modes

    :param data_frame: data frame with a tripMode column
    :return: a list with all mode identifiers of the dataframe and -1 as temporary placeholder for all modes
    """
    return np.insert(data_frame.tripMode.unique(), 0, -1)


def roll_trips(df, rolling_minutes, string):
    df[string] = df[string].rolling(rolling_minutes, center=True, min_periods=1).mean()
    return df


class Metric:

    def __init__(self):
        self._data_frame = None

    def smoothen(self, smoothness_in_minutes, string):
        return self._data_frame.groupby(["tripMode"]).apply(lambda x: roll_trips(x, smoothness_in_minutes, string))

    def _sub(self, other, string):
        temp = self._data_frame.set_index(["tripMode", string])
        temp2 = other._data_frame.set_index(["tripMode", string])
        return temp.sub(temp2, fill_value=0).reset_index()

    def get_mode_specific_data(self, mode_number, string):
        """
        Returns a series of data based on the specific mode
        :param mode_number:
        :return:
        """
        temp = self._data_frame.copy()
        if mode_number == -1:
            temp = temp.groupby([string]).sum()
        else:
            temp = temp[temp["tripMode"] == mode_number]
            temp = temp.set_index(string)
        temp = temp.drop(columns=["tripMode"])  # Trip mode is no longer required and should therefore not be passed
        return temp.squeeze()

    def read_from_raw_data(self, raw_data):
        pass

    @classmethod
    def from_file(cls, file_path):
        obj = cls()
        obj._data_frame = pandas.read_csv(file_path)
        return obj

    @classmethod
    def from_raw_data(cls, raw_data):
        obj = cls()
        obj.read_from_raw_data(raw_data)
        return obj

    def get_data_frame(self):
        return self._data_frame.copy()

    def draw(self, resolution=1):
        pass

    def print(self):
        print(self._data_frame)

    def write(self, path):
        self._data_frame.to_csv(path, index=False)


def get_approximations(dataframe, string, required_modes=[-1, 0, 1, 2, 3, 4]):
    approxis = []
    for i in required_modes:
        if i in get_all_existing_modes(dataframe):
            _, data, error = get_fit_and_error_from_dataframe(dataframe, string, i)
            approxis.append([i, data, error])
        else:
            approxis.append([i, (0, 0, 0), 0])
    # If the dataset does not contain a required mode it needs to be artificially added
    return approxis


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
def fit_distribution_to_data_frame(data_frame, distribution_name="gamma"):
    """
    This method returns the parameters of fitting a probability distribution to the underlying data. Since fitting a
    curve in scipy turns out to be significantly more unreliable than fitting a sample to a distribution this method
    creates an artificial sample by repeating the data points based on their occurrences rather than using the
    probability directly
    :param data_frame: a data frame holding the count (amount) of occurrences
    :param distribution_name: The name of the distribution used for fitting (default: gamma)
    :return: the parameters required to reassemble the best fit of the chosen distribution
    """
    temp = data_frame.copy()

    # TODO this rounding is not really explained and expected
    # Reduces the sample size by integer division of the rounding value (large simulations contain
    # unreasonably large sample sizes)
    # TODO fix and test this 
    if temp["amount"].sum() > 0:
        rounding = pow(10, max(math.ceil(math.log10(temp["amount"].sum()) - 4), 0))
    else:
        return [0, 0, 0]

    temp["amount"] = temp["amount"] // rounding
    temp_ys = temp["amount"].values
    assert any(temp_ys > 0)
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

    result = fit_distribution_to_data_frame(counts, distribution_name=dist_name)
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
