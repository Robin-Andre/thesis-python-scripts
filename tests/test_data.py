import unittest

from metrics.data import Data


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
        self.assertEqual()




if __name__ == '__main__':
    unittest.main()
