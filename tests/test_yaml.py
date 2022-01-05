import unittest
from pathlib import Path

import configurations.configloader
import yamlloader
from configurations import SPECS
import mobitopp_execution as simulation

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
        yaml = yamlloader.YAML(Path(SPECS.CWD + "config/rastatt/short-term-module-100p.yaml"))
        self.assertIsNotNone(yaml)
        configs = yaml.find_calibration_configs(SPECS.CWD)
        self.assertEqual(len(configs), 6)

    def test_read_write_is_invariant(self):

        path = Path(SPECS.CWD + "config/rastatt/short-term-module-100p.yaml")
        yaml = yamlloader.YAML(path)
        original_text = yaml.data
        self.assertEqual(yaml.path, path)
        yaml.write()
        yaml2 = yamlloader.YAML(path)
        self.assertEqual(original_text, yaml2.data)

    def test_get_mode_config(self):
        yaml = simulation.default_yaml()
        c = yaml.mode_config()
        self.assertEqual(type(c), configurations.configloader.ModeChoiceConfig)
        d = yaml.destination_config()
        self.assertEqual(type(d), configurations.configloader.DestinationChoiceConfig)

if __name__ == '__main__':
    unittest.main()
