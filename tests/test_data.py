import unittest

import pandas.testing

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
        self.assertEqual(data.get_modal_split().iloc[1]["amount"], 0)
        self.assertEqual(data.get_modal_split()["amount"].sum(), 1)
        self.assertEqual(data.get_modal_split().index.values.tolist(), [0, 1, 2, 3, 4])

    def test_modal_split_works_with_incomplete_list(self):
        data = Data()
        data.load("resources/example_config_load/results/")
        modal_split = data.get_modal_split([0, 2, 3, 4])
        self.assertEqual(modal_split["amount"].sum(), 1)
        self.assertEqual(modal_split.index.values.tolist(), [0, 2, 3, 4])

    def test_incomplete_approximations_returns_full_list(self):
        data = Data()
        data.load("resources/example_config_load/results/")
        data.travel_distance._data_frame = drop_mode(data.travel_distance._data_frame, 1)
        data.travel_time._data_frame = drop_mode(data.travel_time._data_frame, 1)
        self.assertEqual(len(data.travel_distance.approximations()), 6)
        self.assertEqual(data.travel_distance.approximations()[2], [1, (0, 0, 0), 0])

    def test_subtraction(self):
        data = Data()
        data.load("resources/example_config_load/results/")
        traffic_demand = data.traffic_demand
        expected = traffic_demand.get_data_frame()
        test = traffic_demand - traffic_demand
        print(test.get_data_frame())
        self.assertTrue(all(test.get_data_frame()["active_trips"]) == 0)
        pandas.testing.assert_frame_equal(expected, traffic_demand.get_data_frame())

    def test_smoothen(self):
        data = Data()
        data.load("resources/example_config_load/results/")
        traffic_demand = data.traffic_demand
        traffic_demand._data_frame[traffic_demand._data_frame.tripMode != 1] = 0

        self.assertEqual(traffic_demand._data_frame.iloc[10208]["active_trips"], 5) # The first entry for cars at time 1
        x = traffic_demand.smoothen(2)
        print(x)
        self.assertTrue((x._data_frame[x._data_frame["tripMode"] != 1]["active_trips"] == 0).all())

        self.assertEqual(x._data_frame.iloc[10207]["active_trips"], 0)
        self.assertEqual(x._data_frame.iloc[10208]["active_trips"], 2.5)
        self.assertEqual(x._data_frame.iloc[10209]["active_trips"], 6.5)

        x = traffic_demand.smoothen(3)
        self.assertEqual(x._data_frame.iloc[10207]["active_trips"], 2.5)
        self.assertEqual(x._data_frame.iloc[10208]["active_trips"], 13 / 3)

    def test_smoothen_maintains_same_structure(self):
        data = Data()
        data.load("resources/example_config_load/results/")
        traffic_demand = data.traffic_demand
        x = traffic_demand.smoothen(1)
        pandas.testing.assert_frame_equal(traffic_demand.get_data_frame(), x.get_data_frame())

    #TODO make this a test or remove
    def test_get_neural_data(self):
        data = Data()
        data.load("resources/example_config_load/results/")
        calibration.neural_network_data_generator.get_neural_training_data(data)

    def test_draw(self):
        data = Data()
        data.load("resources/example_config_load/results/")
        a, b, c = data.draw()
        a.show()
        b.show()
        c.show()



if __name__ == '__main__':
    unittest.main()
