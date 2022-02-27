import unittest

from metrics.data import Data


class MyTestCase(unittest.TestCase):

    def test_something(self):
        data = Data()
        data.load("resources/test2_population/individual_0/results/")
        zone_demand = data.zone_destination
        zone_demand.draw(reference=zone_demand)


if __name__ == '__main__':
    unittest.main()
