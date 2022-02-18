
import unittest

import pandas.testing
from matplotlib import pyplot as plt

import visualization
from calibration import tuning
from calibration.evolutionary.individual import Individual

from calibration.evolutionary.population import Population

from configurations.observations import ModalSplitObservation, TimeModeObservation


class MyTestCase(unittest.TestCase):

    def test_load(self):
        x = Individual(0, [])
        try:
            x.load("resources/test_population/individual_0")
        except FileNotFoundError:
            self.fail("Test did not load the individual!")

        self.assertAlmostEqual(x["asc_car_d_mu"].value, 5.352656054767767)
        self.assertAlmostEqual(x["asc_put_sig"].value, -1.5723)
        self.assertAlmostEqual(x["b_tt_car_d_mu"].value, -0.8685707430564293)
        self.assertEqual(x.yaml.get_fraction_of_population(), 0.02)

    def test_tuning_effect_subset_parameter(self):
        x_d = Individual(22, [])
        x = Individual(223123123, [])
        x.load("resources/detailed_individual")
        x_d.load("resources/even_more_detailed_individual")
        d_c = x.data.get_grouped_modal_split(["gender"])
        d = x_d.data.get_grouped_modal_split(["gender"])
        self.assertIsNone(pandas.testing.assert_frame_equal(d_c, d))

    def test_precision_does_not_influence_observations(self):
        p_list = ["asc_car_d_mu", "female_on_asc_bike", "b_tt_car_d_mu"]
        x = Individual(21, p_list)
        x_d = Individual(22, p_list)
        x.load("resources/detailed_individual")
        x_d.load("resources/even_more_detailed_individual")
        for p_name in p_list:
            p = x_d[p_name]
            o1 = p.observer._helper(x, x.data, p)
            o2 = p.observer._helper(x_d, x_d.data, p)
            self.assertEqual(o1, o2)

    def test_column_specification(self):
        x = Individual(21, [])
        x_d = Individual(22, [])
        x.load("resources/detailed_individual")
        x_d.load("resources/even_more_detailed_individual")

        self.assertEqual(x.data.columns().sort(), ["gender", "tripMode"].sort())
        self.assertEqual(x_d.data.columns().sort(), ["gender", "age", "tripMode"].sort())

    def test_subset_selection(self):
        x_d = Individual(22, [])
        x_d.load("resources/even_more_detailed_individual")
        self.assertAlmostEqual(x_d.data.get_modal_split_by_param(x_d["age_0_17_on_asc_bike"]), 0.395593489479)

    def test_subset_selection_invalid(self):
        x_d = Individual(22, [])
        x_d.load("resources/detailed_individual")
        self.assertRaises(AssertionError, x_d.data.get_modal_split_by_param, x_d["age_0_17_on_asc_bike"])

    def test_bad_observation_function_is_caught(self):
        self.assertRaises(AssertionError, TimeModeObservation, lambda x: x / 2, lambda x: 3 * x)

    def test_access_dict_by_name_or_parameter_object(self):
        x = Individual(21, [])
        y = Individual(13, [])
        x.load("resources/test_population/individual_0")
        y.load("resources/compare_individual")
        p = x["asc_car_d_mu"]

        p2 = y[p]
        self.assertNotEqual(p2.value, p.value)
        p.set(13)
        self.assertEqual(p.value, 13)
        self.assertNotEqual(p2.value, 13)

    def test_copy(self):
        x = Individual(21, [])
        x["asc_car_d_mu"].set(9)
        y = x.copy()
        self.assertEqual(y["asc_car_d_mu"].value, 9)
        y["asc_car_d_mu"].set(2)
        self.assertEqual(x["asc_car_d_mu"].value, 9)

    def test_change_value(self):
        x = Individual(9001, [])
        x["asc_car_d_mu"].set(34)
        self.assertEqual(x["asc_car_d_mu"].value, 34)


if __name__ == '__main__':
    unittest.main()
