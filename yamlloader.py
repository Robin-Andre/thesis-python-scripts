import re
import yaml
from copy import deepcopy
import configloader


class V2Loader(yaml.SafeLoader):
    def let_v2_through(self, node):
        return self.construct_mapping(node)


V2Loader.add_constructor(
    u'!file',
    V2Loader.let_v2_through)


class YAML:

    def __init__(self, cwd, yaml_file_path):
        # TODO figure out if multiple yamls can be used
        with open(cwd + yaml_file_path) as file:
            self.data = yaml.load(file, Loader=V2Loader)
            self.original = deepcopy(self.data)
            self.path = cwd + yaml_file_path
            self.name = yaml_file_path
        self.configs = None

    def __str__(self):
        return self.data

    def __repr__(self):
        return [item.name for item in self.configs]

    def set_configs(self, configs):
        self.configs = configs

    def find_config(self, cwd, dict_entry1, dict_entry2):
        return configloader.Config(cwd, self.data[dict_entry1][dict_entry2])

    # TODO maybe remove
    def set_config_to_calibration(self, config, dict_entry1, dict_entry2):
        config.set_path("calibration/" + config.name)
        self.data[dict_entry1][dict_entry2] = config.path
        config.write()

    # TODO this is hardcoded where the relevant configs are
    # TODO remove this from this class
    def find_configs(self, cwd):
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
