import re
import yaml
from copy import copy, deepcopy
import configloader


class V2Loader(yaml.SafeLoader):
    def let_v2_through(self, node):
        return self.construct_mapping(node)


V2Loader.add_constructor(
    u'!file',
    V2Loader.let_v2_through)


class YAML:

    def __init__(self, yaml_file_path):
        # TODO figure out if multiple yamls can be used
        with open(yaml_file_path) as file:
            self.data = yaml.load(file, Loader=V2Loader)
            self.original = deepcopy(self.data)
            self.path = yaml_file_path

    def find_config(self, cwd, dict_entry1, dict_entry2):
        co = configloader.Config(cwd, self.data[dict_entry1][dict_entry2])
        co.set_path("calibration/" + co.name)
        self.data[dict_entry1][dict_entry2] = co.path
        co.write()
        return co

    # TODO this is hardcoded where the relevant configs are
    def find_configs(self, cwd):
        configs = []
        # Find all configs from destinationChoice
        for key in self.data["destinationChoice"]:
            configs.append(self.find_config(cwd, "destinationChoice", key))
        configs.append(self.find_config(cwd, "modeChoice", "main"))
        return configs

    def write(self):
        output = yaml.dump(self.data)
        output = re.sub("dataSource:", "dataSource: !file", output)
        # print(output)
        with open(self.path, "w") as file:
            file.write(output)

    def reset(self):
        print("Restoring Original")
        self.data = deepcopy(self.original)
        self.write()
