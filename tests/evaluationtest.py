import time
import unittest
import numpy as np
import pandas

import evaluation

import visualization as plot


class MyTestCase(unittest.TestCase):

    def test_temporary(self):
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        temp_df = evaluation.create_plot_data(raw_data)
        temp_df["identifier"] = "LOL"
        plot.draw(temp_df, plot.aggregate_traffic_two_sets)
        print(temp_df)

    def test_travel_time_data(self):
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        start = time.time()
        temp_df = evaluation.create_travel_time_data(raw_data)
        end = time.time()
        print(end - start)
        graph = plot.draw_travel_time(temp_df, bin_size=1)

        print(graph)



    def test_travel_distance_data(self):
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        temp_df = evaluation.create_travel_distance_data(raw_data)
        graph = plot.draw_travel_distance(temp_df, bin_size=5)
        print(graph)

    def test_geo_plot(self):
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        print(raw_data.iloc[0])
        raw_data = raw_data.iloc[0:4]
        evaluation.check_data(raw_data)

    def test_plot_data_rename_pls(self):
        numpy_data = np.array([[1, 4, 0],  # -XXX------
                               [0, 5, 0],  # XXXXX-----
                               [2, 8, 1],  # --XXXXXX--
                               [2, 7, 1]   # --XXXXX---
                               ])
        expected_active_trips = [1, 2, 4, 4, 3, 2, 2, 1]
        df = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]), columns=["tripBegin", "tripEnd", "tripMode"]).groupby("tripMode")
        for key in df.groups:
            print(f"The key is{key}")
        print(df.get_group(1))
        temp_df = df.apply(lambda x: evaluation.create_plot_data(x))
        print(temp_df)
        temp_df = temp_df.droplevel(level=1)  # This is the level I wanna reach
        print(temp_df)
        temp_df = temp_df.groupby("time").sum()
        print(temp_df)

        #self.assertEqual(temp_df.get["active_trips"].tolist(), expected_active_trips)

if __name__ == '__main__':
    unittest.main()
