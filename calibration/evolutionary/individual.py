import mobitopp_execution as simulation
import random
from abc import ABC, abstractmethod

from configurations import SPECS
from metrics.data import Comparison


class BaseIndividual(ABC):
    def __init__(self, seed, param_list):
        simulation.restore_experimental_configs()
        self.yaml = simulation.default_yaml()

        self.yaml.set_fraction_of_population(0.02)
        self.yaml.set_seed(seed)
        self.fitness = None
        self.data = None
        self.parameter_list = param_list

    def __str__(self):
        return str(f"Value: {self.active_values()} Fitness: {self.fitness}")

    def __repr__(self):
        return f"{self.fitness}"

    def __lt__(self, other):
        return self.fitness < other.fitness

    def set_seed(self, value):
        self.yaml.set_seed(value)

    @abstractmethod
    def randomize_to_bound(self, mode_list):
        pass

    @abstractmethod
    def randomize(self):
        pass

    @abstractmethod
    def active_values(self):
        pass

    def run(self):
        simulation.clean_result_directory()
        self.yaml.write()
        self.yaml.update_configs()
        return_code, self.data = simulation.run_mobitopp(self.yaml)
        if return_code == 1:
            with open(SPECS.EXP_PATH + "FAILED_RUNS/" + hash(self.yaml.mode_config()), "w+") as file:
                file.write(self.yaml.mode_config())
            print("FAILED RUN")
            return

        self.data.reduce(["tripMode"])

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

    def randomize_to_bound(self, mode_list):
        self.yaml.mode_config().randomize_parameters_to_bound(self.parameter_list, mode_list)

    def randomize(self):
        self.yaml.mode_config().randomize_parameters(self.parameter_list)

    def active_values(self):
        return [(self.yaml.mode_config().parameters[x].name, self.yaml.mode_config().parameters[x].value) for x in self.parameter_list]

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



