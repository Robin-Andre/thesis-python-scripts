import shutil
import unittest
from pathlib import Path

import pandas

import evaluation
import metrics.data
from configurations import configloader, SPECS
from metrics import metric
import mobitopp_execution as simulation
import yamlloader


cwd = SPECS.CWD

test_path = "dump"


class MyTestCase(unittest.TestCase):

    def setUp(self):
        Path(test_path).mkdir(exist_ok=False)

    def tearDown(self):
        path = Path(test_path)
        assert path.exists() and path.is_dir()
        shutil.rmtree(path)

    def test_config_restoration(self):
        simulation.restore_experimental_configs()
        original_configs = "config/shared/parameters/"
        calibration_configs = "calibration/"
        configs = ["destination_choice_utility_calculation_parameters.txt",
                   "destination_choice_parameters_SHOPPING.txt",
                   "destination_choice_parameters_SERVICE.txt", "destination_choice_parameters_LEISURE.txt",
                   "destination_choice_parameters_BUSINESS.txt", "mode_choice_main_parameters.txt"]
        for config in configs:
            original_file = open(cwd + original_configs + config, "r")
            calibration_file = open(cwd + calibration_configs + config, "r")
            self.assertEqual(original_file.read(), calibration_file.read())
            original_file.close()
            calibration_file.close()

    def test_yaml_restoration(self):
        yaml = simulation.default_yaml()
        # This is just making sure that the yaml is dirty
        yaml.set_fraction_of_population("THIS IS A FAKE VALUE FROM TEST AND SHOULD NEVER BEEN SEEN")
        yaml.write()
        simulation.restore_default_yaml()
        yaml = simulation.default_yaml()
        self.assertEqual(yaml.get_fraction_of_population(), 1)


    def test_full_save_function(self):
        yaml_file = "config/rastatt/short-term-module-100p.yaml"
        yaml = yamlloader.YAML(Path(cwd + yaml_file))
        yaml.set_configs(yaml.find_calibration_configs(cwd))  # TODO remove and change yaml loading
        data = metrics.data.Data(evaluation.default_test_merge())
        simulation.save(yaml, data, test_path)
        self.assertTrue(Path(test_path).exists())
        self.assertTrue(Path(test_path + "/configs").exists())
        self.assertTrue(Path(test_path + "/results").exists())

    def test_partial_save_function(self):
        yaml_file = "config/rastatt/short-term-module-100p.yaml"
        yaml = yamlloader.YAML(Path(cwd + yaml_file))
        yaml.set_configs(yaml.find_calibration_configs(cwd))  # TODO remove and change yaml loading
        simulation.save(yaml, None, test_path)
        self.assertTrue(Path(test_path).exists())
        self.assertTrue(Path(test_path + "/configs").exists())
        self.assertFalse(Path(test_path + "/results").exists())

    def test_valid_load_function(self):
        yaml, _ = simulation.load("resources/example_config_load/")
        self.assertEqual(len(yaml.configs), 6)

    def test_read_write(self):
        yaml, _ = simulation.load("resources/example_config_load/")
        namelist = [x.name for x in yaml.configs]
        dest_configs = ["base", "business", "leisure", "service", "shopping"]
        self.assertTrue(Path(yaml.data["modeChoice"]["main"]).name in namelist)
        for x in dest_configs:
            self.assertTrue(Path(yaml.data["destinationChoice"][x]).name in namelist)


        for config in yaml.configs:
            for key in config.parameters.keys():
                config.parameters[key].set(42)
        simulation.save(yaml, None, "dump")
        yaml2, _ = simulation.load("dump/")

        for config in yaml2.configs:
            for key, parameter in config.parameters.items():
                self.assertEqual(parameter.value, 42)

    def test_execution(self):
        yaml, _ = simulation.load("resources/example_config_load/")
        print(yaml.data)
        yaml.set_fraction_of_population(0.01)
        data = simulation.run_experiment(yaml)
        self.assertIsNotNone(data)
        simulation.save(yaml, data, "resources/temp")
        simulation.restore_experimental_configs()

    def test_clean_directory(self):
        path = Path(cwd + "output/results/calibration/throwaway")
        simulation.clean_directory(path)
        self.assertTrue(path.is_dir())
        self.assertFalse(any(path.iterdir()))

    def test_get_config_from_path(self):
        yaml, _ = simulation.load("resources/example_config_load/")
        self.assertEqual(type(yaml.mode_config()), configloader.ModeChoiceConfig)
        self.assertEqual(type(yaml.destination_config()), configloader.DestinationChoiceConfig)


    def test_plot(self):
        yaml, data = simulation.load("resources/example_config_load")
        simulation.save(yaml, data, test_path)
        simulation.plot(test_path)
        self.assertTrue(Path(test_path + "/plots").exists())
        self.assertTrue(Path(test_path + "/plots/traffic_demand.png").exists())
        self.assertTrue(Path(test_path + "/plots/travel_time.png").exists())
        self.assertTrue(Path(test_path + "/plots/travel_distance.png").exists())


if __name__ == '__main__':
    unittest.main()
