import re
import yaml
from copy import copy, deepcopy


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

    def write(self):
        output = yaml.dump(self.data)
        output = re.sub("dataSource:", "dataSource: !file", output)
        #print(output)
        with open(self.path, "w") as file:
            file.write(output)

    def reset(self):
        print(self.original)
        self.data = deepcopy(self.original)
        self.write()
