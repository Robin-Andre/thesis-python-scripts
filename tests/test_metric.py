import unittest

import numpy
import sklearn.metrics
import sklearn.feature_selection
from pandas.testing import assert_series_equal
import pandas
import numpy as np

import metrics.data
import metrics.traveldistance as td
import metrics.metric as metric
import visualization as plot


class MyTestCase(unittest.TestCase):

    #TODO make test
    def nontest_traveltime(self):
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        t = metrics.traveltime.TravelTime(raw_data)
        print(t._data_frame)
        t.draw()
    #TODO make test
    def nontest_traveldistance(self):
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        t = metrics.traveldistance.TravelDistance(raw_data)
        print(t.data_frame)
        t.draw()
    #TODO make test
    def nontest_something(self):

        numpy_data = np.array([[1, 4, 0],  # -XXX------
                               [0, 5, 0],  # XXXXX-----
                               [2, 8, 1],  # --XXXXXX--
                               [2, 7, 1]   # --XXXXX---
                               ])
        df = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]), columns=["tripBegin", "tripEnd", "tripMode"])
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        t = metrics.trafficdemand.TrafficDemand.from_raw_data(df)
        print(t._data_frame)
        t.draw()
        t.print()
        t.write("dump\\lolfile")

    # TODO make test
    def nontest_full_write(self):
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        dat = metrics.data.Data(raw_data)
        dat.write()

    # TODO make test
    def nontest_full_read(self):
        numpy_data = np.array([[1, 4, 0, 5, 1],  # -XXX------
                               [0, 5, 0, 5, 1],  # XXXXX-----
                               [2, 8, 1, 5, 1],  # --XXXXXX--
                               [2, 7, 1, 5, 1]   # --XXXXX---
                               ])
        df = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]), columns=["tripBegin", "tripEnd", "tripMode", "durationTrip", "distanceInKm"])
        data = metrics.data.Data(df)

        data.load()
        data.print()
        data.write()
        data.load()
        data.print()

    def test_for_modal_split(self):
        data = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        td_modal_split = metric.aggregate(data.travel_distance._data_frame, np.inf, "distanceInKm")
        td_modal_split = td_modal_split / td_modal_split.sum()
        tt_modal_split = data.get_modal_split()
        self.assertTrue(np.array_equal(td_modal_split.values, tt_modal_split.values))
        self.assertEqual(tt_modal_split["amount"].sum(), 1)

    def test_float_diff_function(self):
        numpy_data = np.array([[1, 0, 4],
                               [2, 0, 1],
                               [5, 0, 2],
                               [6, 0, 2]
                               ])
        df1 = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]), columns=["distanceInKm", "tripMode", "amount"])
        td1 = metrics.traveldistance.TravelDistance()
        td1.data_frame = df1
        numpy_data = np.array([[1, 0, 3],
                               [2, 0, 2],
                               [5, 0, 1],
                               [6, 0, 3]
                               ])
        df2 = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]),
                               columns=["distanceInKm", "tripMode", "amount"])
        td2 = metrics.traveldistance.TravelDistance()
        td2.data_frame = df2
        index = pandas.MultiIndex.from_product([[0], [1, 2, 5, 6]], names=["tripMode", "distanceInKm"])

        expected_result = pandas.Series([0, 0, 0, 0], index=index, name="diff")

        result = td.TravelDistance.difference_t(td1, td2, lambda x, y: 0)
        self.assertIsNone(assert_series_equal(result, expected_result, check_dtype=False))

        result = td.TravelDistance.difference_t(td1, td2, lambda x, y: abs(x - y))
        expected_result = pandas.Series([1, 1, 1, 1], index=index, name="diff")
        self.assertIsNone(assert_series_equal(result, expected_result, check_dtype=False))

        result = td.TravelDistance.difference_t(td1, td2, lambda x, y: x - y)
        expected_result = pandas.Series([1, -1, 1, -1], index=index, name="diff")
        self.assertIsNone(assert_series_equal(result, expected_result, check_dtype=False))

        result = td.TravelDistance.difference_t(td1, td2, lambda x, y: np.sqrt(np.abs(x - y)))
        expected_result = pandas.Series([1.0, 1.0, 1.0, 1.0], index=index, name="diff")
        self.assertIsNone(assert_series_equal(result, expected_result, check_dtype=False))
        #TODO fix or delete
        #result = td.difference(td1, td2, lambda x, y: np.sqrt(np.abs(x - y)), resolution=5)


########################################################################################################################
    # Testing get_counts() function

    def help_count_function(self, data_array, expected_data_array, expected_indices_array, group=0, resolution=1):
        df = pandas.DataFrame(data=data_array, index=range(data_array.shape[0])
                              , columns=["distanceInKm", "tripMode", "amount"])
        expected_df = pandas.DataFrame(data=expected_data_array, index=expected_indices_array
                                       , columns=["amount"])
        expected_df.index.name = "distanceInKm"
        count = metric.get_counts(df, "distanceInKm", group=group, resolution=resolution)
        self.assertIsNone(pandas.testing.assert_frame_equal(expected_df, count))

    def test_get_count_function_with_resolution(self):
        numpy_data = np.array([[0, 0, 4],
                               [2, 0, 1],
                               [3, 0, 2],
                               [3, 0, 2],
                               [4, 0, 1]
                               ])
        expected_data = np.array([4, 5, 1])
        expected_indices = np.array([0, 2, 4])
        self.help_count_function(numpy_data, expected_data, expected_indices, resolution=2)

    def test_get_count_function_with_grouping_aspect(self):
        # This should group all data into the frame and sum them if they are in the same value
        numpy_data = np.array([[0, 0, 4],
                               [2, 2, 1],
                               [3, 1, 2],
                               [3, 0, 2]
                               ])
        expected_data = np.array([4, 1, 4])
        expected_indices = np.array([0, 2, 3])
        self.help_count_function(numpy_data, expected_data, expected_indices, group=-1)

    def test_get_count_function_with_irrelevant_data(self):
        # Data for 2 and 3 km are for cars (group = 1)
        numpy_data = np.array([[0, 0, 4],
                               [2, 1, 1],
                               [3, 1, 2],
                               [4, 0, 2]
                               ])
        expected_data = np.array([4, 2])
        expected_indices = np.array([0, 4])
        self.help_count_function(numpy_data, expected_data, expected_indices)

    def test_get_count_function_with_data_hole(self):
        # This Data set has no data for 1 km
        numpy_data = np.array([[0, 0, 4],
                               [2, 0, 1],
                               [3, 0, 2],
                               [4, 0, 2]
                               ])
        expected_data = np.array([4, 1, 2, 2])
        expected_indices = np.array([0, 2, 3, 4])
        self.help_count_function(numpy_data, expected_data, expected_indices)

    def test_get_count_function(self):
        numpy_data = np.array([[0, 0, 4],
                               [1, 0, 1],
                               [2, 0, 3],
                               [3, 0, 1],
                               [4, 0, 2]
                               ])
        expected_data = np.array([4, 1, 3, 1, 2])
        expected_indices = np.array([0, 1, 2, 3, 4])
        self.help_count_function(numpy_data, expected_data, expected_indices)

########################################################################################################################
    def test_get_distribution_function(self):
        numpy_data = np.array([[0, 0, 4],
                               [1, 0, 1],
                               [2, 0, 3],
                               [3, 0, 1],
                               [4, 0, 2]
                               ])
        df = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0])
                              , columns=["distanceInKm", "tripMode", "amount"])
        result = metric.get_distribution(df, "distanceInKm")

        self.assertEqual(result["amount"].sum(), 1)

    def test_incomplete_data_set(self):
        data = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        temp = data.travel_distance.get_data_frame()
        temp = temp[temp["tripMode"] != 1]

        data.travel_distance._data_frame = temp
        self.assertTrue(numpy.array_equal(metric.get_all_existing_modes(data.travel_distance._data_frame), np.array([-1, 0, 2, 3, 4])))
        data.travel_distance.approximations()

    # TODO this is not a test
    def nontest_broken_data_set(self):
        data = metrics.data.Data()
        data.load("resources/asc_car_d_sig10/results/")
        data.travel_time.draw_distribution(mode=3)
        #data.draw_distributions()
    # TODO this is not a test
    def nontest_difference_on_incomplete_data(self):
        numpy_data = np.array([[1, 0, 4],
                               [2, 0, 1],
                               ])
        df1 = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]), columns=["distanceInKm", "tripMode", "amount"])
        td1 = metrics.traveldistance.TravelDistance()
        td1.data_frame = df1
        numpy_data = np.array([[1, 0, 3],
                               [3, 0, 2],
                               ])
        df2 = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]),
                               columns=["distanceInKm", "tripMode", "amount"])
        td2 = metrics.traveldistance.TravelDistance()
        td2.data_frame = df2
        result = td.difference(td1, td2, lambda x, y: np.abs(x - y))
        print(result)

    #TODO make test or remove
    def nontest_normalization(self):
        numpy_data = np.array([[1, 0, 4],
                               [2, 0, 1],
                               [1, 1, 1]
                               ])
        df1 = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]), columns=["distanceInKm", "tripMode", "amount"])
        td1 = metrics.traveldistance.TravelDistance()
        td1.data_frame = df1
        numpy_data = np.array([[1, 0, 3],
                               [3, 0, 2],
                               ])
        df2 = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]),
                               columns=["distanceInKm", "tripMode", "amount"])
        td2 = metrics.traveldistance.TravelDistance()
        td2.data_frame = df2
        result = td.difference(td1, td2, lambda x, y: np.abs(x - y), normalize=True)
        print(result.describe())
        print(result)
        result = td.difference(td1, td2, lambda x, y: np.abs(x - y), normalize=True)
        res = pandas.concat([result, result], axis=1)
        res = pandas.DataFrame(np.outer(result, result), index=result.index, columns=result.index)
        res = result.to_frame()
        print(res)
        res = res.reset_index()
        print(res)
        rest = pandas.merge(res, res, how="cross")
        print(rest)
        print(result.describe())

    #TODO make test or move somewhere else
    def nontest_sklearn_mean_squared_error(self):
        data = metrics.data.Data()
        data2 = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        data2.load("resources/example_config_load2/results/")
        modal_split = data.get_modal_split()
        modal_split2 = data2.get_modal_split()
        modal_split = modal_split / modal_split.sum()
        modal_split2 = modal_split2 / modal_split2.sum()
        print(sklearn.metrics.mean_squared_error(modal_split, modal_split2))

        modal_split = data.get_modal_split()
        modal_split2 = data2.get_modal_split()
        modal_split = modal_split * 1000
        modal_split = modal_split / modal_split.sum()
        modal_split2 = modal_split2 / modal_split2.sum()
        print(sklearn.metrics.mean_squared_error(modal_split, modal_split2))

    # TODO not a test
    def nontest_fitting_of_distribution(self):
        data = metrics.data.Data()
        data2 = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        data2.load("resources/example_config_load2/results/")
        temp = data.travel_distance._data_frame
        temp = temp[temp["tripMode"] == 1]
        temp = metric.aggregate(temp, 2, "distanceInKm").reset_index()
        print(temp)
        temp["amount"] = temp["amount"] / temp["amount"].sum()
        print(temp)
        print(plot.draw_travel_distance(temp))
        nmpyaray = temp["amount"].values
        f = Fitter(nmpyaray)
        f.fit()
        print(f.summary())

    #dist_names = [ 'alpha', 'anglit', 'arcsine', 'beta', 'betaprime', 'bradford', 'burr', 'cauchy', 'chi', 'chi2', 'cosine', 'dgamma', 'dweibull', 'erlang', 'expon', 'exponweib', 'exponpow', 'f', 'fatiguelife', 'fisk', 'foldcauchy', 'foldnorm', 'frechet_r', 'frechet_l', 'genlogistic', 'genpareto', 'genexpon', 'genextreme', 'gausshyper', 'gamma', 'gengamma', 'genhalflogistic', 'gilbrat', 'gompertz', 'gumbel_r', 'gumbel_l', 'halfcauchy', 'halflogistic', 'halfnorm', 'hypsecant', 'invgamma', 'invgauss', 'invweibull', 'johnsonsb', 'johnsonsu', 'ksone', 'kstwobign', 'laplace', 'logistic', 'loggamma', 'loglaplace', 'lognorm', 'lomax', 'maxwell', 'mielke', 'nakagami', 'ncx2', 'ncf', 'nct', 'norm', 'pareto', 'pearson3', 'powerlaw', 'powerlognorm', 'powernorm', 'rdist', 'reciprocal', 'rayleigh', 'rice', 'recipinvgauss', 'semicircular', 't', 'triang', 'truncexpon', 'truncnorm', 'tukeylambda', 'uniform', 'vonmises', 'wald', 'weibull_min', 'weibull_max', 'wrapcauchy']


if __name__ == '__main__':
    unittest.main()
