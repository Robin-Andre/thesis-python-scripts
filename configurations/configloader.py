import re
import sys
import random
from enum import Enum


class Mode(Enum):
    BIKE = 0
    DRIVER = 1
    PASSENGER = 2
    PEDESTRIAN = 3
    PUBLIC_TRANSPORT = 4
    TAXI = 7
    BIKE_SHARING = 9001  # TODO these modes have multiple representors in mobitopp and are not yet in the simulation
    CAR_SHARING = 9002
    RIDE_POOLING = 9003

    @classmethod
    def get_mode_from_string(cls, string):
        d = {
            "ped": 3,
            "bike": 0,
            "car_d": 1,
            "car_p": 2,
            "put": 4,
            "taxi": 7,
            "bs": 9001,
            "cs": 9002,
            "rp": 9003,
            "b_cost": 1,
            "elasticity_parken": 1
        }
        for x in d.keys():
            if x in string:
                return Mode(d[x])
        return None

class Config:

    def __init__(self, path):
        with open(path, "r") as file:
            self._text = file.read()
            self.path = path
            self.name = path.name
        self.entries = {}
        self.initialize_dictionary()

    def __str__(self):
        return self._text

    def __repr__(self):
        return f"Data: {self.entries}\nPath: {self.path}\nName: {self.name}\n"

    def randomize(self, parameter_list, lower_bound, upper_bound):
        for item in parameter_list:
            value = (upper_bound - lower_bound) * random() + lower_bound
            value = round(value, 0)
            self.override_parameter(item, value)

    def randomize_except_elasticity(self, rangev):
        for key, value in self.entries.items():
            if key.__contains__("elasti"):
                print(key)
            else:
                self.entries[key] = value + random.uniform(-rangev, rangev)

    def get_parameter_list(self):
        parameters = []
        splits = self._text.split("\n")
        for line in splits:
            if line.__contains__("="):
                name = line.split("=")[0].strip()
                parameters.append(name)

        return parameters

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

    def randomize_main_parameters(self, active_mode_numerical=[0, 1, 2, 3, 4]):
        params = self.get_main_parameters(active_mode_numerical)
        for param in params:
            self.entries[param] = random.uniform(-15, 15)

    def get_main_parameters(self, active_mode_numerical):
        active_mode_list = [Mode(x) for x in active_mode_numerical]
        param_list = []
        specialized = ["dienst", "ausb", "eink", "arbeit", "freiz", "beruft", "hhgr", "pkw_1", "pkw_0", "female",
                       "service", "elasticity", "arbwo", "student", "shift_relief", "ebike", "age", "inc", "zk",
                       "csmit"]
        for key in self.entries.keys():
            if not any(x in key for x in specialized) and (Mode.get_mode_from_string(key) in active_mode_list):
                param_list.append(key)

        return param_list

    def group_description_parameter(self):

        param_list = []

        for key in self.entries.keys():
            # Age, Income, Commuter Ticket, Car Sharing, any else
            specialized = ["dienst", "ausb", "eink", "arbeit", "freiz", "beruft", "hhgr", "pkw_1", "pkw_0","female",
                           "service", "elasticity", "arbwo", "student", "shift_relief", "ebike", "age", "inc", "zk", "csmit"]
            params = [False, False, False, False, False]
            age = False
            income = False
            if key.__contains__("age"):
                params[0] = True
            if key.__contains__("inc"):
                params[1] = True
            if key.__contains__("zk"):
                params[2] = True
            if key.__contains__("csmit"):
                params[3] = True
            if any(x in key for x in specialized):
                params[4] = True

            if not any(params):
                param_list.append(key)
                #print(f"Key: {key}, requires: {params}")
        return param_list

    def temp_name(self):
        for key in self.entries.keys():
            print(f"{key} : {Mode.get_mode_from_string(key)}")

    def get_corresponding_mode(self):
        d = {
            "ped": "Pedestrian",
            "bike": "Bike",
            "car_d": "Driver",
            "car_p": "Passenger",
            "put": "Public Transport",
            "taxi": "Taxi",
            "bs": "Bike Sharing",
            "cs": "Car Sharing",
            "rp": "Ride Pooling",
            "b_cost": "Driver",
            "elasticity_parken": "Driver"
        }
        for key in self.entries.keys():

            if not any(x in key for x in d.keys()):
                print(f"Key {key}")
            fitting_tokens = []
            for x in d.keys():

                if x in key:
                    fitting_tokens.append(x)

            print(f"{key} : {fitting_tokens}")


