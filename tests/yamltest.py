import os
import unittest
from pathlib import Path

import pandas
import mobitopp_execution as simulation
import metric
import yamlloader

# TODO fix this path to be able to deal with all locations of the scripts
cwd = "../../mobitopp-example-rastatt/"

class MyTestCase(unittest.TestCase):


    def test_calibration_folder_exists(self):
        cal_dir = cwd + "calibration/"
        self.assertTrue(os.path.exists(cal_dir))
        self.assertTrue(os.path.isdir(cal_dir))

    def test_yaml_file_is_existing(self):
        yaml_file = "config/rastatt/short-term-module-100p.yaml"
        yaml = yamlloader.YAML(cwd, yaml_file)
        self.assertEqual(len(yaml.configs), 6)
        print(yaml.data)


    def test_yaml_file_is_not_existing(self):
        pass


    def test_full_ex(self):
        yaml_file = "config/rastatt/short-term-module-100p.yaml"
        yaml = yamlloader.YAML(cwd, yaml_file)
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        data = metric.Data(raw_data)
        simulation.save(yaml, data, "dump")


if __name__ == '__main__':
    unittest.main()
