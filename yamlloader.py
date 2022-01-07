import re
from pathlib import Path

import yaml
from copy import deepcopy
from configurations import configloader, SPECS


class V2Loader(yaml.SafeLoader):
    def let_v2_through(self, node):
        return self.construct_mapping(node)


V2Loader.add_constructor(
    u'!file',
    V2Loader.let_v2_through)

#TODO make one liner class method for reading in yaml
class YAML:

    def __init__(self, yaml_file_path):
        # TODO figure out if multiple yamls can be used
        with open(yaml_file_path) as file:
            self.data = yaml.load(file, Loader=V2Loader)
            self.original = deepcopy(self.data)
            self.path = yaml_file_path
            self.name = yaml_file_path.name
        self.configs = None

    def __str__(self):
        return self.data

    def __repr__(self):
        return [item.name for item in self.configs]

    def set_configs(self, configs):
        self.configs = configs

    def mode_config(self):
        for config in self.configs:
            if config.name == "mode_choice_main_parameters.txt":
                return config
        return None

    def destination_config(self):
        for config in self.configs:
            if config.name == "destination_choice_utility_calculation_parameters.txt":
                return config
        return None

    # TODO mobitopp might not be at the same location
    def find_config(self, cwd, dict_entry1, dict_entry2):
        path = Path(cwd + self.data[dict_entry1][dict_entry2])
        if dict_entry1 == "modeChoice":
            return configloader.ModeChoiceConfig(path)
        if dict_entry1 == "destinationChoice" and dict_entry2 == "base":
            return configloader.DestinationChoiceConfig(path)
        return configloader.Config(path)

    def set_config_to_calibration(self):
        for config in self.configs:
            config.set_path(SPECS.CWD + "calibration/" + config.name)
            config.write()

    def set_fraction_of_population(self, target):
        self.data["fractionOfPopulation"] = target

    def get_fraction_of_population(self):
        return self.data["fractionOfPopulation"]

    def set_seed(self, seed):
        self.data["seed"] = seed

    def get_seed(self):
        return self.data["seed"]

    # TODO this is hardcoded where the relevant configs are
    def find_calibration_configs(self, cwd):
        configs = []
        # Find all configs from destinationChoice
        for key in self.data["destinationChoice"]:
            configs.append(self.find_config(cwd, "destinationChoice", key))
        configs.append(self.find_config(cwd, "modeChoice", "main"))
        return configs

    def write_path(self, path):
        output = yaml.dump(self.data)
        output = re.sub("dataSource:", "dataSource: !file", output)
        with open(path, "w+") as file:
            file.write(output)

    def write(self):
        self.write_path(self.path)

    def reset(self):
        print("Restoring Original")
        self.data = deepcopy(self.original)
        self.write()
