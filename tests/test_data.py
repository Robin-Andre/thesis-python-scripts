import unittest

import pandas.testing
from matplotlib import pyplot as plt

import evaluation
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

    def test_draw(self):
        data = Data()
        data.load("resources/example_config_load/results/")
        data2 = Data()
        data2.load("resources/example_config_load2/results/")
        a, b, c = data.draw(reference=data2)
        a.show()
        b.show()
        c.show()
        a, b, c = data.draw_smooth(reference=data2)
        a.show()
        b.show()
        c.show()


    def test_better_modal_split(self):
        data = Data()
        data.load("resources/example_config_load/results/")
        x = data.get_modal_split_based_by_time(1)
        y = x.unstack(level=1).T
        y.plot()
        plt.show()

    def test_new_data_write(self):
        data = Data(evaluation.default_test_merge())
        x = data.traffic_demand
        data.write("temp")
        data.reduce(["tripMode"])
        data.write("temp2")


if __name__ == '__main__':
    unittest.main()
