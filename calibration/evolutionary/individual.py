import copy

from matplotlib import pyplot as plt

import mobitopp_execution as simulation
import random
from abc import ABC, abstractmethod

from configurations import SPECS
from configurations.parameter import Parameter
from metrics.data import Comparison


class BaseIndividual(ABC):
    def __init__(self, seed=-1, param_list=[], fraction_of_pop=0.02):
        simulation.restore_experimental_configs()
        self.yaml = simulation.default_yaml()

        self.yaml.set_fraction_of_population(fraction_of_pop)
        self.yaml.set_seed(seed)
        self.fitness = None
        self.data = None
        self.parameter_name_list = param_list
        self.requirements = self.data_requirements()

    def __str__(self):
        return str(f"Value: {self.active_values()} Fitness: {self.fitness}")

    def __repr__(self):
        return f"{self.fitness}"

    def fraction_of_pop(self):
        return self.yaml.get_fraction_of_population()

    def __lt__(self, other):
        return self.fitness < other.fitness

    def copy(self):
        return copy.deepcopy(self)

    def set_requirements(self, reqs):
        self.requirements = reqs

    def set_seed(self, value):
        self.yaml.set_seed(value)

    def reduce(self, keep_list):
        self.data.reduce(keep_list)

    def errors(self, data):
        errvals = []
        for p in self.parameter_name_list:
            errvals.append((p, self[p].error(self, data)))

        return errvals

    @abstractmethod
    def randomize_to_bound(self, mode_list):
        pass

    @abstractmethod
    def randomize(self):
        pass

    def draw(self, reference=None, group="tripMode"):

        return self.data.draw(reference, group=group)

    @abstractmethod
    def active_values(self):
        pass

    def data_requirements(self):
        all_requirements = set()
        for p in self.parameter_name_list:
            all_requirements = set.union(all_requirements, set(Parameter(p).requirements.keys()))
        return all_requirements

    def run(self):

        simulation.clean_result_directory()
        self.yaml.write()
        self.yaml.update_configs()
        return_code, self.data = simulation.run_mobitopp(self.yaml)
        if return_code == 1:
            with open(SPECS.EXP_PATH + "FAILED_RUNS/" + str(hash(self.yaml.mode_config())), "w+") as file:
                file.write(str(self.yaml.mode_config()))
            print("FAILED RUN")
            return

        self.data.reduce(self.requirements)

    def save(self, path):
        simulation.save(self.yaml, self.data, path)

    def load(self, path):
        self.yaml, self.data = simulation.load(path)

    def set_fitness(self, compare_data):
        self.fitness = self.evaluate_fitness(compare_data)

    @abstractmethod
    def evaluate_fitness(self, compare_data):
        return -1

    @abstractmethod
    def evaluate_fitness_by_group(self, compare_data):
        return -1


class Individual(BaseIndividual):

    def __getitem__(self, item):
        return self.yaml.mode_config()[item]

    def randomize_to_bound(self, mode_list):
        self.yaml.mode_config().randomize_parameters_to_bound(self.parameter_name_list, mode_list)

    def randomize(self):
        self.yaml.mode_config().randomize_parameters(self.parameter_name_list)

    def active_values(self):
        return [(self.yaml.mode_config().parameters[x].name, self.yaml.mode_config().parameters[x].value) for x in
                self.parameter_name_list]

    def pygad_bound_dict(self):
        l = []
        for p in self.parameter_name_list:
            l.append({"low": self[p].lower_bound, "high": self[p].upper_bound})

        return l

    def average_value_list(self):
        l_average = []
        for p in self.parameter_name_list:
            l_average.append((self[p].upper_bound + self[p].lower_bound) / 2)

        return l_average

    def pyswarms_bound_lists(self):
        l_lower = []
        l_upper = []
        for p in self.parameter_name_list:
            l_lower.append(self[p].lower_bound)
            l_upper.append(self[p].upper_bound)

        return l_lower, l_upper

    def spsa_bound_lists(self):
        l_tuples = []
        for p in self.parameter_name_list:
            l_tuples.append((self[p].lower_bound, self[p].upper_bound))
        return l_tuples

    def parameter_names(self):
        return self.yaml.mode_config().parameters.keys()

    def set_list(self, new_val_list):
        for p, val in zip(self.parameter_name_list, new_val_list):
            print(f"{p} {val}")
            self[p].set(val)

    def randomize_active_parameters(self):
        for p in self.parameter_name_list:
            self[p].randomize()

    def change_observer_options(self, options):
        for p in self.parameter_name_list:
            self[p].observer.options = options

    def make_basic(self, nullify_exponential_b_tt=False):
        for param in self.yaml.mode_config().parameters.values():
            param.value = 0

        for param in self.yaml.mode_config().get_main_parameters():
            # Elasticity is an exponent in calculation, sadly 0^0 causes terrible scenarios :(
            if param.name.__contains__("elasticity"):
                param.value = 1

            # All Travel time components except pedestrian are using a negative exponential curve, setting this to a
            # really small number should result in no weight being put on the time component
            if param.name.__contains__("b_tt") and param.name.__contains__("_mu") and nullify_exponential_b_tt:
                param.value = -999999999

    def evaluate_fitness(self, compare_data):
        difference = Comparison(self.data, compare_data)
        return difference.travel_demand

    def evaluate_fitness_by_group(self, compare_data):
        x = self.data.traffic_demand
        y = compare_data.traffic_demand

        z = x - y
        z = z.groupby("tripMode").sum()
        return z

    def similarity(self, compare_individual):
        return self.evaluate_fitness(compare_individual.data)


def temp_helper(x, y, vals):
    return [x + y * v for v in vals]


class DestinationIndividual(Individual):
    def __getitem__(self, item):
        if type(item) is tuple:
            return self.yaml.activity_destination_config(item[0])[item[1]]
        return self.yaml.destination_config()[item]

    def parameter_names(self):
        return self.yaml.destination_config().parameters.keys()

    def tune_asc(self, delta):
        for p in self.parameter_names():
            if p.__contains__("asc_"):
                self[p].value = self[p].value + delta

    def tune_b_tt(self, delta):
        for p in self.parameter_names():
            if p.__contains__("b_tt"):
                self[p].value = self[p].value + delta


    def evaluate_fitness(self, compare_data):

        difference = Comparison(self.data, compare_data)
        return difference.sum_zones()

    def draw_utility_functions(self):
        modes = ["car_d", "car_p", "put", "ped", "bike"]
        xvals = list(range(0, 100))
        for x in modes:
            asc = "asc_" + x
            b_tt = "b_tt_" + x
            asc_val = self[asc].value
            b_tt_val = self[b_tt].value
            print(asc_val)
            print(b_tt_val)
            yvals = temp_helper(asc_val, b_tt_val, xvals)
            plt.plot(xvals, yvals)
        plt.legend(["car_d", "car_p", "put", "ped", "bike"])
        plt.show()

    def randomize_special_config(self, activity):
        for p in self.yaml.activity_destination_config(activity).parameters.values():
            p.randomize()


    def randomize(self):
        for p in self.yaml.destination_config().parameters.values():
            p.randomize()

        #special_configs = ["leisure", "shopping", "business", "service"]
        #for s in special_configs:
        #    for p in self.yaml.activity_destination_config(s).parameters.values():
        #        p.value = random.uniform(-10, 10)


class ShoppingDestinationIndividual(DestinationIndividual):

    def __getitem__(self, item):

        return self.yaml.activity_destination_config("shopping")[item]


    def randomize(self):
        for p in self.yaml.activity_destination_config("shopping").parameters.values():
            p.randomize()




class TravelTimeIndividual(Individual):

    def evaluate_fitness(self, compare_data):
        difference = Comparison(self.data, compare_data)
        return difference.travel_time


class ModalSplitIndividual(Individual):

    def evaluate_fitness(self, compare_data):
        difference = Comparison(self.data, compare_data)
        return difference.modal_split
