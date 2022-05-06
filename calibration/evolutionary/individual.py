import copy

from matplotlib import pyplot as plt

import mobitopp_execution as simulation
from abc import ABC, abstractmethod

from configurations import SPECS
from configurations.parameter import Parameter
from metrics.data import Comparison

""" 
This file originated as the individual data for the evolutionary algorithm
during the process of growing into a better calibration algorithm it shifted
the usage from the retired evolutionary algorithm into a convenience class
that made accessing the simulation parameters significantly easier. 
"""

"""
The base individual contains the parameters that are expected to be found 
in every mobitopp simulation 
"""

class BaseIndividual(ABC):

    """
    Initializes a simulation with default parameters
    Restores default configurations since the configs could be tainted from
    previous runs

    @:param seed: the seed for the simulation
    @param_list: the parameters which will be tuned
    @fraction_of_pop: The percentage of simulated agents
    """
    def __init__(self, seed=-1, param_list=[], fraction_of_pop=0.02):
        simulation.restore_experimental_configs()
        self.yaml = simulation.default_yaml()

        self.yaml.set_fraction_of_population(fraction_of_pop)
        self.yaml.set_seed(seed)
        self.fitness = None
        self.data = None
        self.parameter_name_list = param_list
        # The requirements are calculated from the set of parameters
        self.requirements = self.data_requirements()

    def __str__(self):
        return str(f"Value: {self.active_values()} Fitness: {self.fitness}")

    def __repr__(self):
        return f"{self.fitness}"

    """
    Convenience function to access the fraction of population
    """
    def fraction_of_pop(self):
        return self.yaml.get_fraction_of_population()

    def __lt__(self, other):
        return self.fitness < other.fitness

    def copy(self):
        return copy.deepcopy(self)

    """
    Convenience method to overwrite the requirements
    """
    def set_requirements(self, reqs):
        self.requirements = reqs

    def set_seed(self, value):
        self.yaml.set_seed(value)

    """
    Reduces the data to aggregate over the chosen list, mainly used to reduce
    the size of the output data for saving purposes
    """
    def reduce(self, keep_list):
        self.data.reduce(keep_list)

    """
    Returns a list of the individual errors for the parameter set win order 
    of the parameter list
    """
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

    """
    Visualization access method
    """
    def draw(self, reference=None, group="tripMode"):

        return self.data.draw(reference, group=group)

    @abstractmethod
    def active_values(self):
        pass

    """
    Determines the requirements of the parameter set by building the union 
    of requirments of the individual parameters
    """
    def data_requirements(self):
        all_requirements = set()
        for p in self.parameter_name_list:
            all_requirements = set.union(all_requirements, set(Parameter(p).requirements.keys()))
        return all_requirements

    """
    Execute the simulation and if the simulation fails for any reason: 
    write the mode config to the directory of the failed runs
    """
    def run(self):

        simulation.clean_result_directory()
        self.yaml.write()
        self.yaml.update_configs()
        return_code, self.data = simulation.run_mobitopp(self.yaml)
        if return_code == 1:
            with open(SPECS.EXP_PATH + "FAILED_RUNS/" + str(hash(self.yaml.mode_config())) + ".txt", "w+") as file:
                file.write(str(self.yaml.mode_config()._text))
            print("FAILED RUN")
            return return_code

        self.data.reduce(self.requirements)
        return return_code

    """
    Save the individual to the directory determined by the path
    """
    def save(self, path):
        simulation.save(self.yaml, self.data, path)

    """
    Load an individual from a path
    """
    def load(self, path):
        self.yaml, self.data = simulation.load(path)

    """
    Convenience method to overwrite the fitness for testing and manual
    manipulation purposes
    """
    def set_fitness(self, compare_data):
        self.fitness = self.evaluate_fitness(compare_data)

    @abstractmethod
    def evaluate_fitness(self, compare_data):
        return -1

    @abstractmethod
    def evaluate_fitness_by_group(self, compare_data):
        return -1


"""
The default individual for mode choice calibration
"""


class Individual(BaseIndividual):

    """
    Access method returns parameter from the mode configuration
    """
    def __getitem__(self, item):
        return self.yaml.mode_config()[item]

    """
    Randomize the parameters to the bounds set by the parameter
    """
    def randomize_to_bound(self, mode_list):
        self.yaml.mode_config().randomize_parameters_to_bound(self.parameter_name_list, mode_list)

    def randomize(self):
        self.yaml.mode_config().randomize_parameters(self.parameter_name_list)

    """
    Returns a list of tuples of the names and current values of all the active
    parameters. Used by the meta heuristic algorithms
    """
    def active_values(self):
        return [(self.yaml.mode_config().parameters[x].name, self.yaml.mode_config().parameters[x].value) for x in
                self.parameter_name_list]

    """
    Returns the parameter bounds in the format for the pygad genetic algorithm
    """
    def pygad_bound_dict(self):
        l = []
        for p in self.parameter_name_list:
            l.append({"low": self[p].lower_bound, "high": self[p].upper_bound})

        return l

    """
    Gives a list of the average values of the active parameters. Used for determining
    the start values of the tuning algorithm
    """
    def average_value_list(self):
        l_average = []
        for p in self.parameter_name_list:
            l_average.append((self[p].upper_bound + self[p].lower_bound) / 2)

        return l_average

    """
    Returns a list of the parameter bound srequired by the pyswarms algorithm
    """
    def pyswarms_bound_lists(self):
        l_lower = []
        l_upper = []
        for p in self.parameter_name_list:
            l_lower.append(self[p].lower_bound)
            l_upper.append(self[p].upper_bound)

        return l_lower, l_upper

    """
    Returns the list of parameter bounds for the spsa format
    """
    def spsa_bound_lists(self):
        l_tuples = []
        for p in self.parameter_name_list:
            l_tuples.append((self[p].lower_bound, self[p].upper_bound))
        return l_tuples

    """
    Returns all parameter names of the mode config
    """
    def parameter_names(self):
        return self.yaml.mode_config().parameters.keys()

    """ 
    Sets the active parameters by passing a list of values of equal length
    """
    def set_list(self, new_val_list):
        for p, val in zip(self.parameter_name_list, new_val_list):
            print(f"{p} {val}")
            self[p].set(val)

    def randomize_active_parameters(self):
        for p in self.parameter_name_list:
            self[p].randomize()

    """
    Overwrite the observer options for all parameters
    """
    def change_observer_options(self, options):
        for p in self.parameter_name_list:
            self[p].observer.options = options

    """
    Create a mode config with all zeros, if the nullify parameter is set
    the beta parameter are set close to -infinity to counteract
    the negative exponential function of beta parameters
    """
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

"""
THe destination individual is anadatpation of the base individual
to operate on the destination configurations rather than the mode config
"""


class DestinationIndividual(Individual):
    def __getitem__(self, item):
        if type(item) is tuple:
            return self.yaml.activity_destination_config(item[0])[item[1]]
        return self.yaml.destination_config()[item]

    def parameter_names(self):
        return self.yaml.destination_config().parameters.keys()
    """
    Attempt to calibrate the destination choice by shifting all asc parameters
    of the main destination configuration. The result is unfortunately useless
    """
    def tune_asc(self, delta):
        for p in self.parameter_names():
            if p.__contains__("asc_"):
                self[p].value = self[p].value + delta

    """
    THe same effect for beta parameters, sadly no efficent tuning result
    can occur from this tuning
    """
    def tune_b_tt(self, delta):
        for p in self.parameter_names():
            if p.__contains__("b_tt"):
                self[p].value = self[p].value + delta

    """
    Overwrites the active values method because the destination configuration
    allows for 5 different conficuations which need to be accessed speeratels
    """
    def active_values(self):
        return [(self[x].name, self[x].value) for x in
                self.parameter_name_list]


    def evaluate_fitness(self, compare_data):

        difference = Comparison(self.data, compare_data)
        return difference.sum_zones()

    """
    Attempt to evaluate the impact of the logsum
    """
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


"""
OBSOLETE
"""

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
