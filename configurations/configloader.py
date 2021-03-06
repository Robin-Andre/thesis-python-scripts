import re
import random

import utils.check_parameters_from_gen_files
from configurations import limits
from configurations.parameter import Parameter


class Config:

    def __init__(self, path):

        self.limits = self.get_dict()
        with open(path, "r") as file:
            self._text = file.read()
            self.path = path
            self.name = path.name
        self.parameters = {}
        self.initialize_dictionary()
        utils.check_parameters_from_gen_files.check_config(self, remove_invalid_parameters=True)
        self.parameters.pop("max_attractivity", None)  # This parameter is not part of the tuning process

    def __str__(self):
        return "\n".join([str(x) for x in self.parameters.values()])

    def __repr__(self):
        return self._text
        # return f"Data: {self.parameters}\nPath: {self.path}\nName: {self.name}\n"

    def __getitem__(self, item):
        if type(item) == Parameter:
            return self.parameters[item.name]
        else:
            return self.parameters[item]

    def get_dict(self):
        return limits.DEFAULT_DICT

    def get_parameter_list(self):
        parameter_list = []
        splits = self._text.split("\n")
        for line in splits:
            if line.__contains__("="):
                name = line.split("=")[0].strip()
                parameter_list.append(name)

        return parameter_list

    def set_list(self, new_list):
        for param, new_val in zip(self.parameters.values(), new_list):
            param.set(new_val)

    def reset(self):
        with open(self.path, "r") as file:
            self._text = file.read()

        self.initialize_dictionary()
        self.write()

    def get_main_parameters_name_only(self, active_mode_numerical=[0, 1, 2, 3, 4]):
        return []

    def randomize_main_parameters(self, active_mode_numerical=[0, 1, 2, 3, 4]):
        params = self.get_main_parameters_name_only(active_mode_numerical)
        for param in params:
            a, b = self.limit.limits[param]
            self.parameters[param].set(random.uniform(a, b))

    def initialize_dictionary(self):
        splits = self._text.split("\n")
        for line in splits:
            if line.__contains__("="):
                name = line.split("=")[0].strip()
                # TODO evil eval
                value = eval(line.split("=")[1])
                p = Parameter(name, value)
                p.initialize_bounds(self.limits)
                self.parameters[name] = p
            else:
                pass

    def get_parameter(self, parameter_name):
        splits = self._text.split("\n")
        for line in splits:
            if line.__contains__(parameter_name):
                # TODO maybe not all configs have an equal sign
                return eval(line.split("=")[1])
        # print("Parameter [" + parameter_name + "] not found")

    def set_parameter(self, parameter_name, new_value, absolute=False):
        assert isinstance(new_value, int) or isinstance(new_value, float)
        if parameter_name is None or parameter_name.strip() == "":
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
        # print("Parameter[" + parameter_name + "] not found")
        return

    def override_parameter(self, parameter_name, parameter_value_absolute):
        assert isinstance(parameter_value_absolute, int) or isinstance(parameter_value_absolute, float)
        if parameter_name is None or parameter_name.strip() == "":
            return

        regex = "(" + parameter_name + "\\s*=)(.*)(\n*)"
        search = re.search(regex, self._text)
        if search:
            self._text = re.sub(regex, "\\1 " + str(parameter_value_absolute) + "\\3", self._text)
            return
        # print("Parameter[" + parameter_name + "] not found")
        return

    def set_path(self, new_path):
        self.path = new_path

    def update_text(self):
        for key, parameter in self.parameters.items():
            if self.get_parameter(key) != parameter.value:
                self.override_parameter(key, parameter.value)

    def write_config_file(self, path):
        self.set_path(path)
        self.update_text()
        with open(path, "w+") as file:
            file.write(self._text)

    def write(self):
        self.write_config_file(self.path)


class ModeChoiceConfig(Config):
    def __init__(self, path):
        super().__init__(path)

    def get_dict(self):
        return limits.MODE_CHOICE_LIMITS

    def randomize_parameters(self, parameter_name_list):
        for parameter in parameter_name_list:
            p = self.parameters[parameter]
            p.randomize()

    def randomize_parameters_to_bound(self, parameter_name_list, mode_prevalence_list):
        for parameter in parameter_name_list:
            p = self.parameters[parameter]
            if p.requirements["tripMode"] in mode_prevalence_list:
                p.randomize_with_limits(p.upper_bound, p.upper_bound)
                # p.randomize_with_limits((p.upper_bound + p.lower_bound) / 2, p.upper_bound)
            else:
                p.randomize_with_limits(p.lower_bound, p.lower_bound)
                # p.randomize_with_limits(p.lower_bound, (p.upper_bound + p.lower_bound) / 2)

    def get_all_requirement_options(self):
        options = set()
        for parameter in self.parameters.values():
            options = options.union(set(parameter.requirements.keys()))

        return list(options)

    def get_main_parameters_name_only(self, requested_modes=[0, 1, 2, 3, 4]):
        param_list = []
        for parameter in self.parameters.values():
            # Mode choice parameters always require a mode so checking for length 1 is sufficient
            if len(parameter.requirements) == 1 and parameter.requirements["tripMode"] in requested_modes:
                param_list.append(parameter.name)

        return param_list

    def get_main_parameters(self, requested_modes=[0, 1, 2, 3, 4]):
        param_list = []
        for parameter in self.parameters.values():
            # Mode choice parameters always require a mode so checking for length 1 is sufficient
            if len(parameter.requirements) == 1 and parameter.requirements["tripMode"] in requested_modes and not parameter.__contains__("_cost"):
                param_list.append(parameter)

        return param_list

    def get_all_parameter_names_on_requirements(self, attribute_list, requested_modes=[0, 1, 2, 3, 4]):
        param_list = []
        assert "tripMode" in attribute_list
        for parameter in self.parameters.values():
            # Mode choice parameters always require a mode so checking for length 1 is sufficient
            all_requirements_satisfied = set(parameter.requirements).issubset(set(attribute_list))
            if all_requirements_satisfied and parameter.requirements["tripMode"] in requested_modes:
                param_list.append(parameter.name)
        if "b_cost" in param_list: param_list.remove("b_cost")
        if "b_cost_put" in param_list: param_list.remove("b_cost_put")
        if "b_inc_high_on_b_cost" in param_list: param_list.remove("b_inc_high_on_b_cost")
        if "b_inc_high_on_b_cost_put" in param_list: param_list.remove("b_inc_high_on_b_cost_put")
        if "cost" in attribute_list:  # Hack to get cost into the list
            param_list.append("b_cost")
            param_list.append("b_cost_put")
            if "economicalStatus" in attribute_list:
                param_list.append("b_inc_high_on_b_cost")
                param_list.append("b_inc_high_on_b_cost_put")

        return param_list


class DestinationChoiceConfig(Config):
    def __init__(self, path):
        super().__init__(path)

    def get_dict(self):
        return limits.DESTINATION_CHOICE_LIMITS

    def get_main_parameters_name_only(self, requested_modes=[0, 1, 2, 3, 4]):
        param_list = []
        for parameter in self.parameters.values():

            if len(parameter.requirements) == 1 and parameter.requirements["tripMode"] in requested_modes:
                param_list.append(parameter.name)

        return param_list

    def get_all_parameter_names_on_requirements(self, attribute_list, requested_modes=[0, 1, 2, 3, 4]):
        param_list = []
        for parameter in self.parameters.values():
            # Mode choice parameters always require a mode so checking for length 1 is sufficient
            all_requirements_satisfied = set(parameter.requirements).issubset(set(attribute_list))
            if all_requirements_satisfied:
                param_list.append(parameter.name)

        return param_list
