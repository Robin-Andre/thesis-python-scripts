import unittest

import pandas.testing
from matplotlib import pyplot as plt

from metrics.data import Data


class MyTestCase(unittest.TestCase):
    def test_initial(self):
        data = Data()
        data.load("resources/workday_individual/results/")
        x = data.traffic_demand
        y = x.aggregate_time(1)
        self.assertIsNone(pandas.testing.assert_frame_equal(x._data_frame, y._data_frame))

    def test_second(self):
        data = Data()
        data.load("resources/workday_individual/results/")
        x = data.traffic_demand
        y = x.aggregate_time(5)
        print(y)

    def test_subtraction(self):
        data = Data()
        data.load("resources/workday_individual/results/")
        x = data.traffic_demand
        y = x.sub_all(x)
        z = x.sub_none(x)
        w = x - x
        self.assertFalse(y["active_trips"].any(axis=None))
        self.assertFalse(z["active_trips"].any(axis=None))
        self.assertFalse(w["active_trips"].any(axis=None))
        self.assertEqual(len(y.columns), 2)
        self.assertEqual(len(z.columns), 2)
        self.assertEqual(len(w.columns), 2)

    def test_draw_all_together(self):
        data = Data()
        data.load("resources/example_config_load/results/")
        data2 = Data()
        data2.load("resources/example_config_load2/results/")
        data.traffic_demand.draw(reference=data2.traffic_demand)
        x = data.traffic_demand
        y = data2.traffic_demand
        z = x.sub_all(y)
        q = x.sub_none(y)
        w = x - y
        x = x.aggregate_time(240)
        y = y.aggregate_time(240)
        z_1 = x.sub_all(y)
        q_1 = x.sub_none(y)
        w_1 = x - y


        for temp in [q, q_1, z, z_1, w, w_1]:
            temp = temp.set_index("time")
            temp.plot()
        plt.show()
        return

        x = x.set_index("time")
        x.plot()
        y = y.set_index("time")
        y.plot()
        plt.show()
        print(x)

if __name__ == '__main__':
    unittest.main()
