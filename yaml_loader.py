import re


class YAML:

    def __init__(self, path):
        f = open(path, "r")
        self.text = f.read()
        self.path = path
        f.close()

    def print(self):
        print(self.text)

    def set_seed(self, number):
        assert number >= 0
        self.text = re.sub("seed:.*\n", "seed: " + str(number) + "\n", self.text)

    def get_seed(self):
        for item in self.text.split("\n"):
            if "seed: " in item:
                return item.split(" ")[1].strip()

    def set_pop_percentage(self, floating_number):
        assert 0 <= floating_number <= 1
        self.text = re.sub("fractionOfPopulation:.*\n", "fractionOfPopulation: " + str(floating_number) + "\n", self.text)

    def get_pop_percentage(self):
        for item in self.text.split("\n"):
            if "fractionOfPopulation: " in item:
                return item.split(" ")[1].strip()

    def get_result_folder(self):
        for item in self.text.split("\n"):
            if "resultFolder: " in item:
                return item.split(" ")[1].strip()

    def set_result_folder(self, relative_path):
        self.text = re.sub("resultFolder:.*\n", "resultFolder: " + relative_path + "\n",
                           self.text)

    def activate(self):
        # Loads in the yaml file, TODO find out how to start multiple yamls
        write_yaml_file(self.path, self.text)


def write_yaml_file(path, text):
    f = open(path, "w")
    f.write(text)
    f.close()




