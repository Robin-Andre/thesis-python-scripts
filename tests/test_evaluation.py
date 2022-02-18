import time
import unittest
import numpy as np
import pandas

import evaluation
import visualization

import visualization as plot
from metrics.trafficdemand import TrafficDemand


class MyTestCase(unittest.TestCase):

    def nontest_temporary(self):
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        temp_df = evaluation.create_plot_data(raw_data)
        temp_df["identifier"] = "LOL"
        plot.draw(temp_df, plot.aggregate_traffic_two_sets)
        print(temp_df)

    def test_travel_time_data(self):
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        temp_df = evaluation.create_plot_data(raw_data)
        print(temp_df)

    def test_distance_extraction(self):
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        data_frame = evaluation.create_travel_distance_data(raw_data)
        self.assertEqual(list(data_frame.columns.values), ["distanceInKm", "tripMode", "amount"])

    def test_distance_and_activity_extraction(self):
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        data_frame = evaluation.create_travel_distance_with_activity_type(raw_data)
        self.assertEqual(list(data_frame.columns.values), ["distanceInKm", "tripMode", "activityType", "amount"])

    def test_household_extraction(self):
        raw_data_household = pandas.read_csv("resources/household.csv", sep=";")
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        x = raw_data.merge(raw_data_household, how="left", left_on="householdOid", right_on="householdId")
        self.assertEqual(len(x), len(raw_data))


if __name__ == '__main__':
    unittest.main()
