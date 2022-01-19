import unittest

import pandas

import evaluation
from metrics.data import Data
from metrics.traveldistance import TravelDistance


class MyTestCase(unittest.TestCase):
    def test_subtraction_from_self_is_zero(self):
        data = Data()
        data.load("resources/example_config_load/results/")
        travel_distance = data.travel_distance
        expected = travel_distance.get_data_frame()
        test = travel_distance - travel_distance
        self.assertTrue(all(test.get_data_frame()["amount"]) == 0)
        pandas.testing.assert_frame_equal(expected, travel_distance.get_data_frame())

    def nontest_new_readin(self):
        a = TravelDistance()
        a.read_from_raw_data_new(evaluation.default_test_merge())
        x = a.reduce(["tripMode"])


if __name__ == '__main__':
    unittest.main()
