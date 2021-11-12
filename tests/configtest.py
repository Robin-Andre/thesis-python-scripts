import random
import unittest

import configloader

# TODO hardcoded path

cwd = "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/"
file_path = "config/shared/parameters/mode_choice_main_parameters.txt"


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.config = configloader.Config(cwd, file_path)

    def invalid_parameter_name_overwrite(self, parameter):

        text = self.config.text
        # Some arbitrary value, the override should not write anything regardless
        self.config.override_parameter(parameter, 9001)
        self.assertEqual(text, self.config.text)

    def test_empty_parameter_name_overwrite(self):
        self.invalid_parameter_name_overwrite("")

    def test_none_parameter_name_override(self):
        self.invalid_parameter_name_overwrite(None)

    def test_wrong_parameter_name_override(self):
        self.invalid_parameter_name_overwrite("asc_car_d_mU")  # Should be the first parameter in the specified config
        self.invalid_parameter_name_overwrite("Bonanza")  # Hopefully there will never be a parameter called "Bonanza"

    def test_get_parameter_list(self):
        parameter_list = self.config.get_parameter_list()
        self.assertEqual(len(parameter_list), 228)

    def valid_parameter_target_overwrite(self, parameter, value):
        self.config.override_parameter(parameter, value)
        self.assertEqual(self.config.get_parameter(parameter), value)

    def invalid_parameter_target_overwrite(self, parameter, value):
        original_config = self.config.text
        with self.assertRaises(AssertionError):
            self.config.override_parameter(parameter, value)
        self.assertEqual(self.config.text, original_config)

    def test_parameter_override(self):
        parameter_list = self.config.get_parameter_list()
        test_values_valid = [0, -0, 9001, -9001, 0.00001, -0.00001]
        test_values_invalid = [None, "", "Bonanza", "1", "1+1", "   ", "\n", [42, 9001]]
        for parameter in parameter_list:
            for value in test_values_valid:
                self.valid_parameter_target_overwrite(parameter, value)

        for parameter in parameter_list:
            for value in test_values_invalid:
                self.invalid_parameter_target_overwrite(parameter, value)


if __name__ == '__main__':
    unittest.main()
