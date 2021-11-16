import unittest
import mobitopp_execution as simulation


class MyTestCase(unittest.TestCase):

    def test_config_restoration(self):
        simulation.restore_experimental_configs()
        standard_config_path = "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/"
        original_configs = "config/shared/parameters/"
        calibration_configs = "calibration/"
        configs = ["destination_choice_utility_calculation_parameters.txt",
                   "destination_choice_parameters_SHOPPING.txt",
                   "destination_choice_parameters_SERVICE.txt", "destination_choice_parameters_LEISURE.txt",
                   "destination_choice_parameters_BUSINESS.txt", "mode_choice_main_parameters.txt"]
        for config in configs:
            original_file = open(standard_config_path + original_configs + config, "r")
            calibration_file = open(standard_config_path + calibration_configs + config, "r")
            self.assertEqual(original_file.read(), calibration_file.read())
            original_file.close()
            calibration_file.close()


if __name__ == '__main__':
    unittest.main()
