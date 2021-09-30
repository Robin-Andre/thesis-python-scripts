import re


class Config:

    def __init__(self, path):
        f = open(path, "r")
        self.text = f.read()
        self.path = path
        f.close()

    def get_parameter_list(self):
        parameters = []
        for line in self.text:
            name = line.split("=")[0].strip()
            # TODO evil eval
            value = eval(line.split("=")[1])
            parameters.append(tuple([name, value]))
        return parameters

    def get_parameter(self, parameter_name):
        splits = self.text.split("\n")
        for line in splits:
            if line.__contains__(parameter_name):
                # TODO maybe not all configs have an equal sign
                return eval(line.split("=")[1])
        print("Parameter [" + parameter_name + "] not found")

    def set_parameter(self, parameter_name, new_value_absolute):
        regex = "(" + parameter_name + "\\s+=)(.*)(\n)"
        search = re.search(regex, self.text)
        if search:
            old_value = search.group(2).strip()
            # TODO evil eval
            diff = new_value_absolute - eval(old_value)
            if diff == 0:
                print("No change performed")
                return
            operator = "+" if diff > 0 else ""
            self.text = re.sub(regex, "\\1\\2 " + operator + str(diff) + "\\3", self.text)
            return
        print("Parameter[" + parameter_name + "] not found")
        return

    def override_parameter(self, parameter_name, parameter_value_absolute):
        # This method overrides a line in a config
        regex = "(" + parameter_name + "\\s+=)(.*)(\n)"
        search = re.search(regex, self.text)
        if search:
            self.text = re.sub(regex, "\\1 " + str(parameter_value_absolute) + "\\3", self.text)
            return
        print("Parameter[" + parameter_name + "] not found")
        return

    def print(self):
        print(self.text)


def find_relevant_config_files(path):
    f = open(path, "r")
    filenames = []
    for line in f:
        if line.__contains__("shared"):
            print(line.split()[1])
            filenames.append(line.split()[1])
    return filenames


def write_configuration_file(parameters):
    print(parameters)
