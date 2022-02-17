import unittest

from calibration.evolutionary.individual import Individual
from configurations.observations import ModalSplitObservation, TimeModeObservation


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.x = Individual(21, [])
        self.y = Individual(13, [])
        self.z = Individual("number", [])
        self.x.load("resources/test_population/individual_0")
        self.y.load("resources/compare_individual")
        self.z.load("resources/test_population/individual_1")

    def test_modal_split_parameter_observation(self):

        parameter = self.x["asc_car_d_mu"]

        print(self.y[parameter])
        print(self.x[parameter])
        print(self.z[parameter])
        self.assertEqual(type(parameter.observer), ModalSplitObservation)
        self.y.data._get_modal_split().loc[parameter.requirements["tripMode"], "count"]
        print(parameter.observe(self.x, self.y.data))
        print(parameter.observe_detailed(self.x, self.z, self.y.data))

    def test_travel_time_parameter_observation(self):
        parameter = self.x["b_tt_car_d_mu"]
        self.assertEqual(type(parameter.observer), TimeModeObservation)
        print(f"x: {parameter}")
        print(f"y: {self.y['b_tt_car_d_mu']}")

        print(parameter.observe(self.x, self.y.data))
        print(parameter.observe(self.z, self.y.data))
        print(parameter.observe(self.y, self.x.data))
        print(parameter.observe_detailed(self.x, self.z, self.y.data))

    def test_b_tt_ped_gets_different_treatment(self):
        parameter = self.x["b_tt_ped"]

        print(parameter.value)
        print(self.y["b_tt_ped"].value)

        self.assertGreater(parameter.observe(self.x, self.y.data), parameter.value)

    def test_observation_function_guess(self):
        o = TimeModeObservation()
        print(o.guess(-1, -0.5, 1, -1.5))
        print(o.guess(-1, -0.368, 1, -2.718))


if __name__ == '__main__':
    unittest.main()
