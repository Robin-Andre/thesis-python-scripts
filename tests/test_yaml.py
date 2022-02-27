import re
import unittest
from pathlib import Path

import configurations.configloader
import utils.check_parameters_from_gen_files
import yamlloader
from configurations import SPECS
import mobitopp_execution as simulation


def temp(path, compare_keys):
    with open(path, "r") as file:
        text = file.read()
    test = []
    for x in compare_keys:
        l = text.strip().split(x + " ")[1:]
        if l:
            ele = l[0]
            ele = re.split("\n|\t", ele)[0]
            if ele.__contains__("[") and ele.__contains__("]"):
                fin = ele.split("[")[1].split("]")[0]
                test.append("[" + fin + "]")

    return test


class MyTestCase(unittest.TestCase):

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

    def test_util_yaml_checker(self):
        simulation.restore_experimental_configs()
        yaml = simulation.default_yaml()
        utils.check_parameters_from_gen_files.check_yaml(yaml, remove_invalid_parameters=True)
        # Warning there is a parameter "b_ausb_put" which is obviously misspelled in the gen file, once fixed this
        # test will fail so increase the number of expected parameters to 217 (the other 11 parameters are for car
        # sharing which will not be in this model)
        self.assertEqual(len(yaml.mode_config().parameters), 228 - 12 - 1)
        self.assertEqual(len(yaml.destination_config().parameters), 23 - 5 - 5)
        self.assertTrue("elasticity_acc_put" not in yaml.destination_config().parameters.keys())
        self.assertEqual(len(yaml.activity_destination_config("business").parameters), 66 - 7 - 5 - 1) # -1 because maxAttractivity is not part of the tuning process

    #@unittest.skip("Just a print, not a test")
    def test_print_all_params(self):
        yaml = simulation.default_yaml()
        config = yaml.activity_destination_config("leisure")
        print(config)

if __name__ == '__main__':
    unittest.main()
