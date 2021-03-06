import unittest
from pathlib import Path

import configurations.parameter
from configurations import configloader


class ConfigTestCase(unittest.TestCase):

    def setUp(self):
        self.config = configloader.Config(Path("resources/example_config_load/configs/mode_choice_main_parameters.txt"))

    def invalid_parameter_name_setting(self, parameter):
        text = self.config._text
        # Some arbitrary value, the override should not write anything regardless
        self.config.override_parameter(parameter, 9001)
        self.assertEqual(text, self.config._text)
        self.config.set_parameter(parameter, 9001)
        self.assertEqual(text, self.config._text)

    def test_empty_parameter_name(self):
        self.invalid_parameter_name_setting("")

    def test_equal_amount_of_parameters(self):
        self.assertEqual(len(self.config.parameters), len(self.config.get_parameter_list()) - 13) # 13 Parameters are missing

    def test_none_parameter_name(self):
        self.invalid_parameter_name_setting(None)

    def test_wrong_parameter_name(self):
        self.invalid_parameter_name_setting("asc_car_d_mU")  # Should be the first parameter in the specified config
        self.invalid_parameter_name_setting("Bonanza")  # Hopefully there will never be a parameter called "Bonanza"

    def test_get_parameter_list(self):
        parameter_list = self.config.get_parameter_list()
        self.assertEqual(len(parameter_list), 228)

    def valid_parameter_target_overwrite(self, parameter, value):
        self.config.override_parameter(parameter, value)
        self.assertEqual(self.config.get_parameter(parameter), value)

    def invalid_parameter_target_setting(self, parameter, value):
        original_config = self.config._text
        with self.assertRaises(AssertionError):
            self.config.override_parameter(parameter, value)
        self.assertEqual(self.config._text, original_config)
        with self.assertRaises(AssertionError):
            self.config.set_parameter(parameter, value)
        self.assertEqual(self.config._text, original_config)

    def test_parameter_override(self):
        parameter_list = self.config.get_parameter_list()
        test_values_valid = [0, -0, 9001, -9001, 0.00001, -0.00001]
        test_values_invalid = [None, "", "Bonanza", "1", "1+1", "   ", "\n", [42, 9001]]
        for parameter in parameter_list:
            for value in test_values_valid:
                self.valid_parameter_target_overwrite(parameter, value)

        for parameter in parameter_list:
            for value in test_values_invalid:
                self.invalid_parameter_target_setting(parameter, value)

    def test_dictionary_overwrite_does_not_change_untouched_lines(self):
        original_config = self.config._text
        original_text_without_two_lines = "\n".join(original_config.split("\n")[2:])
        original_text_two_lines = "\n".join(original_config.split("\n")[:2])
        self.config.parameters["asc_car_d_mu"].set(42)
        self.config.parameters["asc_car_d_sig"].set(9001)
        self.config.update_text()
        self.assertEqual(original_text_without_two_lines, "\n".join(self.config._text.split("\n")[2:]))
        self.assertNotEqual(original_text_two_lines, "\n".join(self.config._text.split("\n")[:2]))

    def test_write_works_properly(self):
        test_path = Path("test.txt")
        assert not test_path.exists()  # The test file should not exist already
        self.config.write_config_file(test_path)
        loaded_config = configloader.Config(test_path)
        self.assertEqual(self.config._text, loaded_config._text)
        test_path.unlink()

    def test_parameter_append(self):
        test_parameter = "asc_car_d_mu"
        original_value = self.config.get_parameter(test_parameter)
        self.config.set_parameter(test_parameter, 20)  # Append as delta
        self.assertEqual(original_value + 20, self.config.get_parameter(test_parameter))
        self.config.set_parameter(test_parameter, 20, absolute=True)  # Append as new target value
        self.assertEqual(self.config.get_parameter(test_parameter), 20)

    def test_config_load_handles_semi_corrupt_files(self):
        test_path = Path("resources/invalid_config.txt")
        config2 = configloader.Config(test_path)
        self.assertEqual(config2.get_parameter("valid_parameter"), 9001)
        self.assertEqual(config2.get_parameter("another_valid_parameter"), 42)

    def test_subclass_config(self):
        mc_c = configloader.ModeChoiceConfig(Path("resources/example_config_load/configs/mode_choice_main_parameters.txt"))
        self.assertEqual(len(mc_c.parameters), 228 - 13) # 13 parameters are missing

    def test_base_config_randomization_does_nothing(self):
        config = configloader.Config(Path("resources/example_config_load/configs/mode_choice_main_parameters.txt"))
        expected_results = config.parameters
        config.randomize_main_parameters()
        self.assertEqual(expected_results, config.parameters)

    def test_get_main_params(self):
        mc_c = configloader.ModeChoiceConfig(Path("resources/example_config_load/configs/mode_choice_main_parameters.txt"))
        print([x for x in mc_c.get_all_parameter_names_on_requirements(["tripMode", "age"])])
        print([x for x in mc_c.get_all_parameter_names_on_requirements(["tripMode", "gender"])])
        print([x for x in mc_c.get_all_parameter_names_on_requirements(["tripMode", "gender", "age"])])
        print([x for x in mc_c.get_all_parameter_names_on_requirements(["tripMode", "cost"])])
        self.assertEqual(mc_c.get_main_parameters_name_only(requested_modes=[]), [])
        self.assertEqual(mc_c.get_main_parameters_name_only(requested_modes=[0]), ["asc_bike_mu", "b_tt_bike_mu"])

    def test_get_options(self):
        mc_c = configloader.ModeChoiceConfig(
            Path("resources/example_config_load/configs/mode_choice_main_parameters.txt"))
        print(mc_c.get_all_requirement_options())

    def test_set_list(self):
        mc_c = configloader.ModeChoiceConfig(
            Path("resources/example_config_load/configs/mode_choice_main_parameters.txt"))
        print([str(x) for x in mc_c.parameters.values()])
        mc_c.set_list([2])
        print([str(x) for x in mc_c.parameters.values()])

if __name__ == '__main__':
    unittest.main()
