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
        self.assertEqual(type(parameter.observer), ModalSplitObservation)

    def test_travel_time_parameter_observation(self):
        parameter = self.x["b_tt_car_d_mu"]
        self.assertEqual(type(parameter.observer), TimeModeObservation)

    def test_multirequiring_parameter(self):
        parameter = self.x["female_on_asc_car_d"]
        print(self.x.data.columns())
        print(parameter.requirements)

        parameter = self.x["age_0_17_on_asc_ped"]
        print(list(parameter.requirements.keys()))
        print(parameter.observe(self.x, self.y.data))



    def test_b_tt_ped_gets_different_treatment(self):
        parameter = self.x["b_tt_ped"]

        print(parameter.value)
        print(self.y["b_tt_ped"].value)

        self.assertGreater(parameter.observe(self.x, self.y.data), parameter.value)


if __name__ == '__main__':
    unittest.main()
