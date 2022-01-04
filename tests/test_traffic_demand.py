import unittest


from metrics import data


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




if __name__ == '__main__':
    unittest.main()
