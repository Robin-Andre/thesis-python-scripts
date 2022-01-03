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



if __name__ == '__main__':
    unittest.main()
