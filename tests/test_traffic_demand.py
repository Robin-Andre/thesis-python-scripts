import time
import unittest

import pandas

import evaluation
from metrics import data
from metrics.data import Data
from metrics.trafficdemand import TrafficDemand


class MyTestCase(unittest.TestCase):

    def test_bounds_of_get_data(self):
        dat = data.Data()
        dat.load("resources/example_config_load/results/")
        traffic_demand = dat.traffic_demand
        for i in [0, 1, 2, 3, 4]:
            cur = traffic_demand.get_mode_specific_data(i)
            self.assertLess(cur.index.values.max(), 11000)  # The test data runs for 7 days so 10080 minutes
            self.assertEqual(cur.index.values.min(), 0)

    def test_get_peak(self):
        dat = data.Data()
        dat.load("resources/example_config_load/results/")
        traffic_demand = dat.traffic_demand
        self.assertEqual(traffic_demand.get_peak((0, 1400))[1], 11372)
        self.assertLess(traffic_demand.get_peak((0, 449))[1], 11372)
        self.assertLess(traffic_demand.get_peak((451, 1400))[1], 11372)

    def test_get_peaks(self):
        dat = data.Data()
        dat.load("resources/example_config_load/results/")
        traffic_demand = dat.traffic_demand
        print(traffic_demand.get_week_peaks())

    # TODO wont work as long as it is using outdated test data
    def disabled_test_subtraction(self):
        dat = Data()
        dat.load("resources/example_config_load/results/")
        traffic_demand = dat.traffic_demand
        #expected = traffic_demand.accumulate(["tripMode"])
        test = traffic_demand - traffic_demand
        print(test.get_data_frame())
        self.assertTrue(all(test.get_data_frame()["active_trips"]) == 0)
        #pandas.testing.assert_frame_equal(expected, traffic_demand.get_data_frame())

    def nontest_new_readin_method(self):
        a, b, c = TrafficDemand(), TrafficDemand(), TrafficDemand()
        a.read_from_raw_data_new2(evaluation.default_test_merge())
        b.read_from_raw_data_new(evaluation.default_test_merge())

        c.read_from_raw_data_new(evaluation.default_test_merge())
        c.reduce(["tripMode"])

        x = a.aggregate_delta(["tripMode"])
        y = b.aggregate_delta(["tripMode"])
        z = c.aggregate_delta(["tripMode"])

        pandas.testing.assert_frame_equal(x, y)
        pandas.testing.assert_frame_equal(y, z)

if __name__ == '__main__':
    unittest.main()
