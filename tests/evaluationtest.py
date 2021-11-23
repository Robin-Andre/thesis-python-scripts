import time
import unittest

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

        #graph = plot.draw_travel_time2(temp_df, bin_size=5)

        #print(graph)
        #graph = plot.draw_travel_time2(temp_df, bin_size=2)

        #print(graph)
        #graph = plot.draw_travel_time2(temp_df, bin_size=4)

        #print(graph)


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

if __name__ == '__main__':
    unittest.main()
