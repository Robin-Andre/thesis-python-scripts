import unittest

import pandas

from metrics.data import Data


class MyTestCase(unittest.TestCase):
    def test_subtraction_from_self_is_zero(self):
        data = Data()
        data.load("resources/example_config_load/results/")
        travel_time = data.travel_time
        expected = travel_time.get_data_frame()
        test = travel_time - travel_time
        self.assertTrue(all(test.get_data_frame()["count"]) == 0)
        pandas.testing.assert_frame_equal(expected, travel_time.get_data_frame())

if __name__ == '__main__':
    unittest.main()
