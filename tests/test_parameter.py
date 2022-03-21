import unittest
from pathlib import Path

from configurations import configloader

from configurations.parameter import Parameter, Employment, Mode, EconomicalGroup as Economics, AgeGroup as Age, \
    ActivityGroup as Activity


class MyTestCase(unittest.TestCase):
    def helper(self, parameter_name, expected_factors):
        p = Parameter(parameter_name)
        self.assertEqual(list(p.requirements.keys()), expected_factors)

    def detailed_helper(self, parameter_name, expected_factors):
        self.assertEqual(Parameter(parameter_name).requirements, expected_factors)

    def test_random_parameters(self):
        self.helper("asc_car_d", ["tripMode"])
        self.detailed_helper("asc_car_d", {"tripMode": 1})
        self.detailed_helper("csmit_on_asc_bike", {"tripMode": 0, "HasCSMembershipNotImplemented": True})
        self.detailed_helper("b_dienst_car_p", {"tripMode": Mode.PASSENGER.value, "activityType": Activity.BUSINESS.value})
        self.detailed_helper("shift_age_56_on_logsum_attr", {"age": [50, 60]})
        self.detailed_helper("shift_age_78_on_logsum_drive_fix ", {"age": [70, 100]})
        self.detailed_helper("shift_age_1_on_logsum_drive_fix", {"age": 0})
        self.detailed_helper("shift_uml_on_logsum_pt", {"isUmlandNotImplemented": True})
        self.detailed_helper("shift_purp_on_logsum_attr", {})
        self.detailed_helper("b_home_car_p", {"tripMode": Mode.PASSENGER.value, "activityType": Activity.HOME.value})
        self.detailed_helper("shift_home_on_logsum_pt_fix", {"employment": Employment.HOME.value})
        self.detailed_helper("shift_high_inc_on_logsum_pt", {"economicalStatus": Economics.RICH.value})
        self.detailed_helper("b_arbwo_bike", {"tripMode": 0, "workday": True})
        self.detailed_helper("shift_carav_on_logsum_drive", {"eachAdultHasCar": True})

    def test_elasticity(self):
        self.detailed_helper("elasticity_parken", {"tripMode": 1, "parking": True})
        self.detailed_helper("elasticity_acc_put", {"tripMode": 4, "access_time": True})

    @unittest.skip("Console print spam")
    def test_detailed_destination_config(self):
        conf = configloader.Config(Path("resources/example_config_load/configs/destination_choice_parameters_LEISURE.txt"))
        for key in conf.parameters.keys():
            print(conf.parameters[key])
        self.helper("shift_age_78_on_logsum_attr", ["age"])





if __name__ == '__main__':
    unittest.main()
