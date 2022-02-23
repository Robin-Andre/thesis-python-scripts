import unittest

import pandas.testing
from matplotlib import pyplot as plt

import evaluation
import visualization
from configurations.parameter import Parameter
from metrics.data import Data
import calibration


def drop_mode(dataframe, mode):
    return dataframe[dataframe["tripMode"] != mode]


class MyTestCase(unittest.TestCase):

    def test_modal_split_returns_all_modes(self):
        data = Data()
        data.load("resources/example_config_load/results/")
        self.assertEqual(data.travel_distance._data_frame["tripMode"].unique().tolist(), [0, 1, 2, 3, 4])
        self.assertEqual(data.travel_time._data_frame["tripMode"].unique().tolist(), [0, 1, 2, 3, 4])
        data.travel_distance._data_frame = drop_mode(data.travel_distance._data_frame, 1)
        data.travel_time._data_frame = drop_mode(data.travel_time._data_frame, 1)
        self.assertEqual(data.travel_distance._data_frame["tripMode"].unique().tolist(), [0, 2, 3, 4])
        self.assertEqual(data.travel_time._data_frame["tripMode"].unique().tolist(), [0, 2, 3, 4])
        self.assertEqual(data.get_modal_spliteeee(1), 0)
        self.assertEqual(data._get_modal_split()["count"].sum(), 1)
        self.assertEqual(data._get_modal_split().index.values.tolist(), [0, 1, 2, 3, 4])

    def test_modal_split_works_with_incomplete_list(self):
        data = Data()
        data.load("resources/example_config_load/results/")
        modal_split = data._get_modal_split(mode_list=[0, 2, 3, 4])
        self.assertEqual(modal_split["count"].sum(), 1)
        self.assertEqual(modal_split.index.values.tolist(), [0, 2, 3, 4])

    def test_incomplete_approximations_returns_full_list(self):
        data = Data()
        data.load("resources/example_config_load/results/")
        data.travel_distance._data_frame = drop_mode(data.travel_distance._data_frame, 1)
        data.travel_time._data_frame = drop_mode(data.travel_time._data_frame, 1)
        self.assertEqual(len(data.travel_distance.approximations()), 6)
        self.assertEqual(data.travel_distance.approximations()[2], [1, (0, 0, 0), 0])

    def test_get_grouped_modal_split(self):
        data = Data()
        data.load("resources/even_more_detailed_individual/results/")
        x = data.get_grouped_modal_split(["age"])
        y = data.get_grouped_modal_split(["age", "age"])
        self.assertTrue(x.eq(y.values).all().all())

    def test_modal_split_is_sum_of_group(self):
        data = Data()
        data.load("resources/even_more_detailed_individual/results/")
        dt = data.travel_time.get_data_frame()
        x = dt.groupby("tripMode").sum()["count"].to_frame()
        x = x / x.sum()
        self.assertIsNone(pandas.testing.assert_frame_equal(x, data._get_modal_split()))

    def test_extracting_default_modal_split_from_detailed_data(self):
        data = Data()
        data.load("resources/even_more_detailed_individual/results/")
        dt = data.travel_time.get_data_frame()
        x = dt.groupby("tripMode").sum()["count"].to_frame()
        x = x / x.sum()
        y = data.get_grouped_modal_split([])
        self.assertIsNone(pandas.testing.assert_frame_equal(x, y))
        self.assertIsNone(pandas.testing.assert_frame_equal(x, data.get_grouped_modal_split()))

    def test_extracting_data_with_higher_specification(self):
        data = Data()
        data.load("resources/even_more_detailed_individual/results/")
        x = data.get_grouped_modal_split(["age", "gender"])
        p = Parameter("female_on_asc_bike")
        self.assertAlmostEqual(data.get_modal_split_by_param(p), 0.1749315)

        p = Parameter("age_18_29_on_asc_bike")
        self.assertAlmostEqual(data.get_modal_split_by_param(p), 0.25136341)

        p = Parameter("asc_car_d_mu")
        self.assertAlmostEqual(data.get_modal_split_by_param(p), 0.5052792)

    @unittest.skip("Visual test/Graphic analysis")
    def test_draw(self):
        data = Data()
        data.load("resources/even_more_detailed_individual/results/")
        a, b, c, = data.draw()
        a.show()
        b.show()
        c.show()


if __name__ == '__main__':
    unittest.main()
