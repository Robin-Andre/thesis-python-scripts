import unittest
from pathlib import Path

from configurations import configloader

from configurations.parameter import Parameter, Employment, Mode, EconomicalGroup as Economics, AgeGroup as Age, \
    ActivityGroup as Activity


class MyTestCase(unittest.TestCase):
    def test_something(self):
        mc_c = configloader.ModeChoiceConfig(Path("resources/example_config_load/configs/mode_choice_main_parameters.txt"))
        temp = mc_c.parameters.keys()
        for key in temp:
            p = Parameter(key)
            print(p)
            #print([x[0] for x in p.requirements])
           # if key in mc_c.get_main_parameters(active_mode_numerical=[0, 1, 2, 3, 4, 7, 9001, 9002, 9003]):
           #     self.assertEqual(len(p.requirements), 1)
            #else:
            #    self.assertGreater(len(p.requirements), 1)

    def helper(self, parameter_name, expected_factors):
        p = Parameter(parameter_name)
        self.assertEqual(list(p.requirements.keys()), expected_factors)

    def detailed_helper(self, parameter_name, expected_factors):
        self.assertEqual(Parameter(parameter_name).requirements, expected_factors)

    def test_something_else(self):
        mc_d = configloader.DestinationChoiceConfig(Path("resources/example_config_load/configs/destination_choice_utility_calculation_parameters.txt"))
        temp = mc_d.parameters.keys()
        for key in temp:
            p = Parameter(key)
            print(p)
            #x = mc_d.get_main_parameters(active_mode_numerical=[0, 1, 2, 3, 4, 7, 9001, 9002, 9003])
            #print(x)
            #if key in mc_d.get_main_parameters(active_mode_numerical=[0, 1, 2, 3, 4, 7, 9001, 9002, 9003]):
            #    self.assertEqual(len(p.requirements), 1)
            #else:
            #    self.assertGreater(len(p.requirements), 1)


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

    def test_detailed_destination_config(self):
        conf = configloader.Config(Path("resources/example_config_load/configs/destination_choice_parameters_LEISURE.txt"))
        for name in conf.parameters:
            print(conf.parameters[name])
        return
        for key in conf.parameters.keys():
            p = Parameter(key)
            print(p)
        self.helper("shift_age_78_on_logsum_attr", ["age"])





if __name__ == '__main__':
    unittest.main()
