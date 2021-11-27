import time
import unittest

import pandas
import numpy as np
import metric

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


if __name__ == '__main__':
    unittest.main()
