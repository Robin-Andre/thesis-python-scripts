import os
import unittest
from pathlib import Path

import pandas
import mobitopp_execution as simulation
import metric
import yamlloader


class MyTestCase(unittest.TestCase):

    # TODO this should be in main, not a unit test
    #def test_calibration_folder_exists(self):
    #    cal_dir = cwd + "calibration/"
    #    self.assertTrue(os.path.exists(cal_dir))
    #    self.assertTrue(os.path.isdir(cal_dir))

    def test_existing_yaml_file_can_be_loaded(self):
        yaml_path = Path("resources/example_config_load/launch.yaml")
        yaml = yamlloader.YAML(yaml_path)
        self.assertEqual(yaml.name, "launch.yaml")

    def test_non_existing_yaml_file_cannot_be_loaded(self):
        yaml_path = Path("fakefake")
        assert not yaml_path.exists()
        with self.assertRaises(FileNotFoundError):
            yaml = yamlloader.YAML(yaml_path)
            self.assertIsNone(yaml)

    def test_locate_configs(self):
        # TODO either remove or make global
        mobitopp_cwd = "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/"
        yaml = yamlloader.YAML(Path(mobitopp_cwd + "config/rastatt/short-term-module-100p.yaml"))
        self.assertIsNotNone(yaml)
        configs = yaml.find_calibration_configs(mobitopp_cwd)
        self.assertEqual(len(configs), 6)

    def test_read_write_is_invariant(self):
        mobitopp_cwd = "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/"
        path = Path(mobitopp_cwd + "config/rastatt/short-term-module-100p.yaml")
        yaml = yamlloader.YAML(path)
        original_text = yaml.data
        self.assertEqual(yaml.path, path)
        yaml.write()
        yaml2 = yamlloader.YAML(path)
        self.assertEqual(original_text, yaml2.data)


if __name__ == '__main__':
    unittest.main()
