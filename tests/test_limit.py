import unittest
from pathlib import Path

from configurations import configloader
from configurations.limits import generate_mode_choice_parameter_bounds, \
    generate_destination_choice_parameter_bounds


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.mc_c = configloader.ModeChoiceConfig(Path("resources/example_config_load/configs/mode_choice_main_parameters.txt"))

        self.mc_d = configloader.DestinationChoiceConfig(Path("resources/example_config_load/configs/destination_choice_utility_calculation_parameters.txt"))


    def test_generate_mode_limit(self):
        for key, param in self.mc_c.parameters.items():
            print(param)
            #print(f"\"{key}\": {generate_mode_choice_parameter_bounds(key)},")

    def test_generate_destination_limit(self):
        for key, param in self.mc_d.parameters.items():
            print(param)
            #print(f"\"{key}\": {generate_destination_choice_parameter_bounds(key)},")

if __name__ == '__main__':
    unittest.main()
