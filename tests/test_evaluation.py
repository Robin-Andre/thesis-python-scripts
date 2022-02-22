import time
import unittest
import numpy as np
import pandas

import evaluation
import visualization

import visualization as plot
from metrics.trafficdemand import TrafficDemand


class MyTestCase(unittest.TestCase):

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

    def test_weekday_extraction(self):
        x = evaluation.default_test_merge()
        self.assertTrue("workday" in x)
        self.assertEqual(set(x["workday"]), {"WORKDAY", "WEEKEND"})

    def test_merge_data(self):
        pass


if __name__ == '__main__':
    unittest.main()
