import unittest
from pathlib import Path

from configurations.enums.activitygroup import ActivityGroup as Activity
from configurations.enums.mode import Mode
from configurations.enums.agegroup import AgeGroup as Age
from configurations.enums.economicalgroup import EconomicalGroup as Economics

from configurations import configloader

from configurations.parameter import Parameter, Employment


class MyTestCase(unittest.TestCase):
    def test_something(self):
        mc_c = configloader.ModeChoiceConfig(Path("resources/example_config_load/configs/mode_choice_main_parameters.txt"))
        temp = mc_c.entries.keys()
        for key in temp:
            p = Parameter(key)
            print([x[0] for x in p.requirements])
            if key in mc_c.get_main_parameters(active_mode_numerical=[0, 1, 2, 3, 4, 7, 9001, 9002, 9003]):
                self.assertEqual(len(p.requirements), 1)
            else:
                self.assertGreater(len(p.requirements), 1)

    def helper(self, parameter_name, expected_factors):
        p = Parameter(parameter_name)
        self.assertEqual([x[0] for x in p.requirements], expected_factors)

    def detailed_helper(self, parameter_name, expected_factors):
        self.assertEqual(Parameter(parameter_name).requirements, expected_factors)

    def test_something_else(self):
        mc_d = configloader.DestinationChoiceConfig(Path("resources/example_config_load/configs/destination_choice_utility_calculation_parameters.txt"))
        temp = mc_d.entries.keys()
        for key in temp:
            p = Parameter(key)
            print(p)

            if key in mc_d.get_main_parameters(active_mode_numerical=[0, 1, 2, 3, 4, 7, 9001, 9002, 9003]):
                self.assertEqual(len(p.requirements), 1)
            else:
                self.assertGreater(len(p.requirements), 1)


    def test_random_parameters(self):
        self.helper("asc_car_d", ["tripMode"])
        self.detailed_helper("asc_car_d", [("tripMode", Mode.DRIVER)])
        self.detailed_helper("csmit_on_asc_bike", [("tripMode", Mode.BIKE), ("HasCSMembershipNotImplemented", True)])
        self.detailed_helper("b_dienst_car_p", [("tripMode", Mode.PASSENGER), ("activityType", Activity.BUSINESS)])
        self.detailed_helper("shift_age_56_on_logsum_attr", [("age", Age.FROM_50_TO_69)])
        self.detailed_helper("shift_age_78_on_logsum_drive_fix ", [("age", Age.FROM_70_TO_120)])
        self.detailed_helper("shift_age_1_on_logsum_drive_fix", [("age", Age.FROM_0_TO_17)])
        self.detailed_helper("shift_uml_on_logsum_pt", [("isUmlandNotImplemented", True)])
        self.detailed_helper("shift_purp_on_logsum_attr", [])
        self.detailed_helper("b_home_car_p", [("tripMode", Mode.PASSENGER), ("activityType", Activity.HOME)])
        self.detailed_helper("shift_home_on_logsum_pt_fix", [("employment", Employment.HOME)])
        self.detailed_helper("shift_high_inc_on_logsum_pt", [("economicalStatus", Economics.RICH)])

    def test_power_config(self):
        conf = configloader.Config(Path("resources/example_config_load/configs/destination_choice_parameters_LEISURE.txt"))
        for key in conf.entries.keys():
            p = Parameter(key)
            print(p)
        self.helper("shift_age_78_on_logsum_attr", ["age"])



if __name__ == '__main__':
    unittest.main()
