import unittest

import pandas

import evaluation
import visualization
from metrics.data import Data
from metrics.traveldistance import TravelDistance


class MyTestCase(unittest.TestCase):
    def test_subtraction_from_self_is_zero(self):
        data = Data()
        data.load("resources/example_config_load/results/")
        travel_distance = data.travel_distance
        expected = travel_distance.get_data_frame()
        test = travel_distance - travel_distance
        self.assertTrue(all(test.get_data_frame()["count"]) == 0)
        pandas.testing.assert_frame_equal(expected, travel_distance.get_data_frame())

    @unittest.skip("Visual test/Graphic analysis")
    def test_draw_without_bonus_shenanigans(self):
        data = Data()
        data.load("resources/example_config_load/results/")
        travel_distance = data.travel_distance
        visualization.draw_travel_distance_without_modes(travel_distance.get_data_frame(), reference=travel_distance.get_data_frame())


if __name__ == '__main__':
    unittest.main()
