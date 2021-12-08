import unittest
from pandas.testing import assert_series_equal

import pandas
import numpy as np
import metric
import visualization
from metric import TrafficDemand as trd, TravelDistance as td, TravelTime as tt
import visualization as plot

class MyTestCase(unittest.TestCase):


    def test_traveltime(self):
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        t = metric.TravelTime(raw_data)
        print(t.data_frame)
        t.draw()

    def test_traveldistance(self):
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        t = metric.TravelDistance(raw_data)
        print(t.data_frame)
        t.draw()


    def test_something(self):

        numpy_data = np.array([[1, 4, 0],  # -XXX------
                               [0, 5, 0],  # XXXXX-----
                               [2, 8, 1],  # --XXXXXX--
                               [2, 7, 1]   # --XXXXX---
                               ])
        df = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]), columns=["tripBegin", "tripEnd", "tripMode"])
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        t = metric.TrafficDemand.from_raw_data(df)
        print(t.data_frame)
        t.draw()
        t.print()
        t.write("dump\\lolfile")


    def test_full_write(self):
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        dat = metric.Data(raw_data)
        dat.write()


    def test_full_read(self):
        numpy_data = np.array([[1, 4, 0, 5, 1],  # -XXX------
                               [0, 5, 0, 5, 1],  # XXXXX-----
                               [2, 8, 1, 5, 1],  # --XXXXXX--
                               [2, 7, 1, 5, 1]   # --XXXXX---
                               ])
        df = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]), columns=["tripBegin", "tripEnd", "tripMode", "durationTrip", "distanceInKm"])
        data = metric.Data(df)

        data.load()
        data.print()
        data.write()
        data.load()
        data.print()

    def test_for_meeting(self):
        data = metric.Data()
        data2 = metric.Data()
        data.load("resources/example_config_load/results/")
        data2.load("resources/example_config_load2/results/")
        data.traffic_demand.data_frame["identifier"] = "Target"
        data2.traffic_demand.data_frame["identifier"] = "Uncalibrated"
        data.draw()
        data2.draw()
        plot.draw(pandas.concat([data.traffic_demand.data_frame, data2.traffic_demand.data_frame]), plot.aggregate_traffic_modal_two_sets)

        normalization = data2.traffic_demand.data_frame["active_trips"].sum()
        result = trd.difference(data.traffic_demand, data2.traffic_demand, lambda x, y: abs(x - y), resolution=1)
        print(result.sum() / normalization)
        result = trd.difference(data.traffic_demand, data2.traffic_demand, lambda x, y: x - y, resolution=20)
        print(result.sum() / normalization)
        result = td.difference(data.travel_distance, data2.travel_distance, lambda x, y: abs(x - y))
        result = td.difference(data.travel_distance, data2.travel_distance, lambda x, y: 0, resolution=5)

    def test_for_modal_split(self):
        data = metric.Data()
        data.load("resources/example_config_load/results/")
        td_modal_split = metric.aggregate(data.travel_distance.data_frame, np.inf, "distanceInKm")
        tt_modal_split = metric.aggregate(data.travel_time.data_frame, np.inf, "durationTrip")
        self.assertTrue(np.array_equal(td_modal_split.values, tt_modal_split.values))

    def test_draw_modal_split(self):
        data = metric.Data()
        data.load("resources/example_config_load/results/")
        td_modal_split = metric.aggregate(data.travel_distance.data_frame, np.inf, "distanceInKm")
        td_modal_split["identifier"] = "Test"
        tt_modal_split = metric.aggregate(data.travel_time.data_frame, np.inf, "durationTrip")
        tt_modal_split["identifier"] = "Test2"
        concon = pandas.concat([td_modal_split, tt_modal_split])
        print(concon)
        print(td_modal_split)
        print(visualization.draw_modal_split(concon.reset_index()))

    def test_float_diff_function(self):
        numpy_data = np.array([[1, 0, 4],
                               [2, 0, 1],
                               [5, 0, 2],
                               [6, 0, 2]
                               ])
        df1 = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]), columns=["distanceInKm", "tripMode", "amount"])
        td1 = metric.TravelDistance()
        td1.data_frame = df1
        numpy_data = np.array([[1, 0, 3],
                               [2, 0, 2],
                               [5, 0, 1],
                               [6, 0, 3]
                               ])
        df2 = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]),
                               columns=["distanceInKm", "tripMode", "amount"])
        td2 = metric.TravelDistance()
        td2.data_frame = df2
        index = pandas.MultiIndex.from_product([[0], [1, 2, 5, 6]], names=["tripMode", "distanceInKm"])

        expected_result = pandas.Series([0, 0, 0, 0], index=index, name="diff")
        result = td.difference(td1, td2, lambda x, y: 0)
        self.assertIsNone(assert_series_equal(result, expected_result))

        result = td.difference(td1, td2, lambda x, y: abs(x - y))
        expected_result = pandas.Series([1, 1, 1, 1], index=index, name="diff")
        self.assertIsNone(assert_series_equal(result, expected_result))

        result = td.difference(td1, td2, lambda x, y: x - y)
        expected_result = pandas.Series([1, -1, 1, -1], index=index, name="diff")
        self.assertIsNone(assert_series_equal(result, expected_result))

        result = td.difference(td1, td2, lambda x, y: np.sqrt(np.abs(x - y)))
        expected_result = pandas.Series([1.0, 1.0, 1.0, 1.0], index=index, name="diff")
        self.assertIsNone(assert_series_equal(result, expected_result))

        result = td.difference(td1, td2, lambda x, y: np.sqrt(np.abs(x - y)), resolution=5)
        print(result)

    def test_difference_on_incomplete_data(self):
        numpy_data = np.array([[1, 0, 4],
                               [2, 0, 1],
                               ])
        df1 = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]), columns=["distanceInKm", "tripMode", "amount"])
        td1 = metric.TravelDistance()
        td1.data_frame = df1
        numpy_data = np.array([[1, 0, 3],
                               [3, 0, 2],
                               ])
        df2 = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]),
                               columns=["distanceInKm", "tripMode", "amount"])
        td2 = metric.TravelDistance()
        td2.data_frame = df2
        result = td.difference(td1, td2, lambda x, y: np.abs(x - y))
        print(result)

    def test_normalization(self):
        numpy_data = np.array([[1, 0, 4],
                               [2, 0, 1],
                               [1, 1, 1]
                               ])
        df1 = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]), columns=["distanceInKm", "tripMode", "amount"])
        td1 = metric.TravelDistance()
        td1.data_frame = df1
        numpy_data = np.array([[1, 0, 3],
                               [3, 0, 2],
                               ])
        df2 = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]),
                               columns=["distanceInKm", "tripMode", "amount"])
        td2 = metric.TravelDistance()
        td2.data_frame = df2
        result = td.difference(td1, td2, lambda x, y: np.abs(x - y), normalize=True)
        print(result.describe())
        print(result)
        result = td.difference(td1, td2, lambda x, y: np.abs(x - y), normalize=True)
        res = pandas.concat([result, result], axis=1)
        res = pandas.DataFrame(np.outer(result, result), index=result.index, columns=result.index)
        res = result.to_frame()
        print(res)
        res = res.reset_index()
        print(res)
        rest = pandas.merge(res, res, how="cross")
        print(rest)
        print(result.describe())



if __name__ == '__main__':
    unittest.main()
