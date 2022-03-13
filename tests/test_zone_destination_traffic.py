import unittest

from metrics.data import Data


class MyTestCase(unittest.TestCase):
    def test_subtraction_from_self_is_zero(self):
        data = Data()
        data.load("resources/temp/results/")
        zone_demand = data.zone_destination
        expected = zone_demand.get_data_frame()
        test = zone_demand.sub_none(zone_demand)
        self.assertTrue(all(test["traffic"]) == 0)

if __name__ == '__main__':
    unittest.main()
