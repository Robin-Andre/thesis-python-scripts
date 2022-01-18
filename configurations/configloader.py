import re
import random

from configurations.parameter import Mode
from configurations.limits import ModeLimitSimple, DestinationLimitSimple, Limit


class Config:

    def __init__(self, path):
        with open(path, "r") as file:
            self._text = file.read()
            self.path = path
            self.name = path.name
        self.entries = {}
        self.initialize_dictionary()
        self.limit = Limit(self)

    def __str__(self):
        return self._text

    def __repr__(self):
        return f"Data: {self.entries}\nPath: {self.path}\nName: {self.name}\n"

    def get_parameter_list(self):
        parameters = []
        splits = self._text.split("\n")
        for line in splits:
            if line.__contains__("="):
                name = line.split("=")[0].strip()
                parameters.append(name)

        return parameters

    def reset(self):
        with open(self.path, "r") as file:
            self._text = file.read()

        self.initialize_dictionary()
        self.write()

    def get_main_parameters(self, active_mode_numerical=[0, 1, 2, 3, 4]):
        return []

    def randomize_main_parameters(self, active_mode_numerical=[0, 1, 2, 3, 4]):
        params = self.get_main_parameters(active_mode_numerical)
        for param in params:
            a, b = self.limit.limits[param]
            self.entries[param] = random.uniform(a, b)

    def initialize_dictionary(self):
        splits = self._text.split("\n")
        for line in splits:
            if line.__contains__("="):
                name = line.split("=")[0].strip()
                # TODO evil eval
                value = eval(line.split("=")[1])
                self.entries[name] = value
            else:
                pass
                # print(f"Error parsing[{line}] no seperator found", file=sys.stderr)

    def get_parameter(self, parameter_name):
        splits = self._text.split("\n")
        for line in splits:
            if line.__contains__(parameter_name):
                # TODO maybe not all configs have an equal sign
                return eval(line.split("=")[1])
        print("Parameter [" + parameter_name + "] not found")

    def set_parameter(self, parameter_name, new_value, absolute=False):
        assert isinstance(new_value, int) or isinstance(new_value, float)
        if parameter_name is None:
            print("Called with empty parameter: exiting")
            return
        if parameter_name.strip() == "":
            print("Danger: Called Parameter with whitespace only.")
            return
        regex = "(" + parameter_name + "\\s+=)(.*)(\n*)"
        search = re.search(regex, self._text)
        if search:
            old_value = search.group(2).strip()
            # TODO evil eval
            temp = 0
            if absolute:
                temp = eval(old_value)
            diff = new_value - temp
            if diff == 0:
                print("No change performed")
                return
            operator = "+" if diff > 0 else ""
            self._text = re.sub(regex, "\\1\\2 " + operator + str(diff) + "\\3", self._text)
            return
        print("Parameter[" + parameter_name + "] not found")
        return

    def override_parameter(self, parameter_name, parameter_value_absolute):
        assert isinstance(parameter_value_absolute, int) or isinstance(parameter_value_absolute, float)
        if parameter_name is None:
            print("Called with empty parameter: exiting")
            return
        if parameter_name.strip() == "":
            print("Danger: Called Parameter with whitespace only.")
            return
        regex = "(" + parameter_name + "\\s*=)(.*)(\n*)"
        search = re.search(regex, self._text)
        if search:
            self._text = re.sub(regex, "\\1 " + str(parameter_value_absolute) + "\\3", self._text)
            return
        print("Parameter[" + parameter_name + "] not found")
        return

    def set_path(self, new_path):
        self.path = new_path

    def update_text(self):
        for key, value in self.entries.items():
            if self.get_parameter(key) != value:
                self.override_parameter(key, value)

    def write_config_file(self, path):
        self.update_text()
        with open(path, "w+") as file:
            file.write(self._text)

    def write(self):
        self.write_config_file(self.path)


class ModeChoiceConfig(Config):
    def __init__(self, path):
        super().__init__(path)
        self.limit = ModeLimitSimple(self)

    def get_main_parameters(self, active_mode_numerical=[0, 1, 2, 3, 4]):
        active_mode_list = [Mode(x) for x in active_mode_numerical]
        param_list = []
        specialized = ["dienst", "ausb", "eink", "arbeit", "freiz", "beruft", "hhgr", "pkw_1", "pkw_0", "female",
                       "service", "arbwo", "student", "shift_relief", "ebike", "age", "inc", "zk",
                       "csmit", "mode_bef", "_home_"]
        for key in self.entries.keys():
            if not any(x in key for x in specialized) and (Mode.get_mode_from_string(key) in active_mode_list):
                param_list.append(key)

        return param_list


class DestinationChoiceConfig(Config):
    def __init__(self, path):
        super().__init__(path)
        self.limit = DestinationLimitSimple(self)

    def get_main_parameters(self, active_mode_numerical=[0, 1, 2, 3, 4]):
        active_mode_list = [Mode(x) for x in active_mode_numerical]
        param_list = []
        for key in self.entries.keys():
            x = Mode.get_mode_from_string(key)
            if x is not None and x in active_mode_list:
                param_list.append(key)
        return param_list



