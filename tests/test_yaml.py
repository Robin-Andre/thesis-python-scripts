import re
import unittest
from pathlib import Path

import configurations.configloader
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
            #print(f"Splitting on {x}")
            ele = l[0]
            #print(ele)
            ele = re.split("\n|\t", ele)[0]
            #print(ele)
            if ele.__contains__("[") and ele.__contains__("]"):
                fin = ele.split("[")[1].split("]")[0]
                #print("[" + fin + "]")
                test.append("[" + fin + "]")

    return test


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

# TODO this is not a test but a stub to extract the details for the config and should be removed when finished
    def test_extract_config_prelims(self):
        path_mode1 = Path(SPECS.CWD + "config/choice-models/mode_choice_mixed_logit.gen")
        path_mode2 = Path(SPECS.CWD + "config/choice-models/mode_choice_mixed_logit_mode_preference.gen")
        path_mode3 = Path(SPECS.CWD + "config/choice-models/mode_choice_mixed_logit_time_sensitivity.gen")
        path_dest = Path(SPECS.CWD + "config/choice-models/destination-choice.gen")
        compare_keys = simulation.default_yaml().mode_config().parameters.keys()
        compare_dest_keys = simulation.default_yaml().configs[3].parameters.keys()

        woohoo = []
        for x in [path_mode1, path_mode2, path_mode3]:
            pass
            woohoo.append(temp(x, compare_keys))
        woohoo.append(temp(path_dest, compare_dest_keys))
        z = list(set([x for y in woohoo for x in y]))
        print(sorted(z))
        print("\n".join(z))
        #print(set(woohoo))



if __name__ == '__main__':
    unittest.main()
