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
        print(test.get_data_frame())
        self.assertTrue(all(test.get_data_frame()["amount"]) == 0)
        pandas.testing.assert_frame_equal(expected, travel_time.get_data_frame())

    def test_subtraction_works(self):
        data = Data()
        data.load("resources/example_config_load/results/")
        data2 = Data()
        data2.load("resources/example_config_load2/results/")
        tt1 = data.travel_time
        tt2 = data2.travel_time

        x = tt1 - tt2
        #x.draw_all_distributions()
        print(tt1 - tt2)



if __name__ == '__main__':
    unittest.main()