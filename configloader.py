import re


class Config:

    def __init__(self, cwd, path):
        f = open(cwd + path, "r")
        self.text = f.read()
        self.cwd = cwd
        self.path = path
        self.name = path.split("/")[-1]
        f.close()

    def get_parameter_list(self):
        parameters = []
        splits = self.text.split("\n")
        for line in splits:
            name = line.split("=")[0].strip()
            parameters.append(name)
        return parameters

    def get_parameter_tuples(self):
        parameters = []
        splits = self.text.split("\n")
        for line in splits:
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

    def set_parameter(self, parameter_name, new_value, absolute=False):
        if parameter_name.strip() == "":
            print("Danger: Called Parameter with whitespace only.")
            return
        regex = "(" + parameter_name + "\\s+=)(.*)(\n)"
        search = re.search(regex, self.text)
        if search:
            old_value = search.group(2).strip()
            # TODO evil eval
            temp = 0
            if absolute: temp = eval(old_value)
            diff = new_value - temp
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

    def set_path(self, new_path):
        self.path = new_path

    def write(self):
        write_config_file(self.text, self.cwd + self.path)


def write_config_file(text, path):
    #print(path)
    with open(path, "w") as file:
        file.write(text)

