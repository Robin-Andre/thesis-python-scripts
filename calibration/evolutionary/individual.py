import copy

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
        errvals = {}
        for p in self.parameter_name_list:
            errvals[p] = self[p].error(self, data)

        return errvals

    @abstractmethod
    def randomize_to_bound(self, mode_list):
        pass

    @abstractmethod
    def randomize(self):
        pass

    def draw(self, reference=None):

        return self.data.draw(reference)

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


class TravelTimeIndividual(Individual):

    def evaluate_fitness(self, compare_data):
        difference = Comparison(self.data, compare_data)
        return difference.travel_time


class ModalSplitIndividual(Individual):

    def evaluate_fitness(self, compare_data):
        difference = Comparison(self.data, compare_data)
        return difference.modal_split
