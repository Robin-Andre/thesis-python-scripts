
import unittest

import pandas.testing
from matplotlib import pyplot as plt

import visualization
from calibration import tuning
from calibration.evolutionary.individual import Individual

from calibration.evolutionary.population import Population

from configurations.observations import ModalSplitObservation, TimeModeObservation


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.x = Individual(21, ["asc_car_d_mu", "female_on_asc_bike"])
        self.x.load("resources/detailed_individual")

        self.x_d = Individual(22, [])
        self.x_d.load("resources/even_more_detailed_individual")


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
        d = self.x.data.get_grouped_modal_split(["gender"])
        d_c = self.x_d.data.get_grouped_modal_split(["gender"])
        self.assertIsNone(pandas.testing.assert_frame_equal(d_c, d))

    def test_precision_does_not_influence_observations(self):
        p_list = ["asc_car_d_mu", "female_on_asc_bike", "b_tt_car_d_mu"]
        for p_name in p_list:
            p = self.x_d[p_name]
            o1 = p.observer._helper(self.x, self.x.data, p)
            o2 = p.observer._helper(self.x_d, self.x_d.data, p)
            self.assertEqual(o1, o2)

    def test_column_specification(self):
        self.assertEqual(self.x.data.columns(), {"gender", "tripMode"})
        self.assertEqual(self.x_d.data.columns(), {"gender", "age", "tripMode"})

    def test_subset_selection(self):
        self.assertAlmostEqual(self.x_d.data.get_modal_split_by_param(self.x_d["age_0_17_on_asc_bike"]), 0.395593489479)

    def test_subset_selection_invalid(self):
        self.assertRaises(AssertionError, self.x.data.get_modal_split_by_param, self.x_d["age_0_17_on_asc_bike"])

    def test_reduction_results_are_same(self):

        t1 = self.x_d.data.get_grouped_modal_split()
        self.assertEqual(self.x_d.data.columns(), {"gender", "age", "tripMode"})
        self.x_d.reduce(["gender", "tripMode"])
        self.assertEqual(self.x_d.data.columns(), {"gender", "tripMode"})
        t2 = self.x_d.data.get_grouped_modal_split()
        self.x_d.reduce(["tripMode"])
        self.assertEqual(self.x_d.data.columns(), {"tripMode"})
        t3 = self.x_d.data.get_grouped_modal_split()
        pandas.testing.assert_frame_equal(t1, t2)
        pandas.testing.assert_frame_equal(t2, t3)

    def test_bad_observation_function_is_caught(self):
        self.assertRaises(AssertionError, TimeModeObservation, lambda x: x / 2, lambda x: 3 * x)

    def test_access_dict_by_name_or_parameter_object(self):
        self.x.load("resources/test_population/individual_0")
        self.x_d.load("resources/compare_individual")
        p = self.x["asc_car_d_mu"]

        p2 = self.x_d[p]
        self.assertNotEqual(p2.value, p.value)
        p.set(13)
        self.assertEqual(p.value, 13)
        self.assertNotEqual(p2.value, 13)

    def test_copy(self):
        self.x["asc_car_d_mu"].set(9)
        y = self.x.copy()
        self.assertEqual(y["asc_car_d_mu"].value, 9)
        y["asc_car_d_mu"].set(2)
        self.assertEqual(self.x["asc_car_d_mu"].value, 9)

    def test_change_value(self):
        self.x["asc_car_d_mu"].set(34)
        self.assertEqual(self.x["asc_car_d_mu"].value, 34)

    def test_error_calculation(self):
        for v in self.x.errors(self.x.data).values():
            self.assertAlmostEqual(v, 0)

    def test_individual_parameter_extraction(self):
        r = Individual(9, ["shift_carav_on_logsum_drive", "b_mode_bef_ped", "b_arbwo_car_p"])
        r.run()
        self.assertEqual(r.data.columns(), {"tripMode", "previousMode", "eachAdultHasCar", "workday"})
        self.assertEqual(r.requirements, {"tripMode", "previousMode", "eachAdultHasCar", "workday"})


if __name__ == '__main__':
    unittest.main()
