import unittest

import numpy
from pandas.testing import assert_series_equal
import pandas
import numpy as np

import metrics.data
import metrics.traveldistance as td
import metrics.metric as metric



class MyTestCase(unittest.TestCase):

    def test_for_modal_split(self):
        data = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        td_modal_split = metric.aggregate(data.travel_distance._data_frame, np.inf, "distanceInKm")
        td_modal_split = td_modal_split / td_modal_split.sum()
        tt_modal_split = data._get_modal_split()
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


if __name__ == '__main__':
    unittest.main()
