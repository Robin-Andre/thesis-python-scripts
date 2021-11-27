import shutil
import unittest
from pathlib import Path

import pandas

import metric
import mobitopp_execution as simulation
import yamlloader

cwd = "../../mobitopp-example-rastatt/"
test_path = "dump"

class MyTestCase(unittest.TestCase):

    def setUp(self):
        Path(test_path).mkdir(exist_ok=False)

    def tearDown(self):
        path = Path(test_path)
        assert path.exists() and path.is_dir()
        shutil.rmtree(path)

# TODO this test fails due to hardcode
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

    def test_full_save_function(self):
        yaml_file = "config/rastatt/short-term-module-100p.yaml"
        yaml = yamlloader.YAML(cwd, yaml_file)
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        data = metric.Data(raw_data)
        simulation.save(yaml, data, test_path)
        self.assertTrue(Path(test_path).exists())
        self.assertTrue(Path(test_path + "/configs").exists())
        self.assertTrue(Path(test_path + "/results").exists())

    def test_partial_save_function(self):
        yaml_file = "config/rastatt/short-term-module-100p.yaml"
        yaml = yamlloader.YAML(cwd, yaml_file)
        #raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        #data = metric.Data(raw_data)
        simulation.save(yaml, None, test_path)
        self.assertTrue(Path(test_path).exists())
        self.assertTrue(Path(test_path + "/configs").exists())
        self.assertFalse(Path(test_path + "/results").exists())

    def test_valid_load_function(self):
        yaml = simulation.load("resources/example_config_load/")
        self.assertEqual(len(yaml.configs), 6)

    def test_read_write(self):
        yaml = simulation.load("resources/example_config_load/")
        for config in yaml.configs:
            for key in config.entries.keys():
                config.entries[key] = 42
        simulation.save(yaml, None, "dump")
        yaml2 = simulation.load("dump/")

        for config in yaml2.configs:
            for key, value in config.entries.items():
                self.assertEqual(value, 42)


if __name__ == '__main__':
    unittest.main()
