import time
from pathlib import Path
from calibration.evolutionary import combine, mutate, initialization, replace, selection

import visualization
from calibration.evolutionary.individual import Individual, BaseIndividual
from configurations.parameter import Parameter
from metrics.data import Comparison, Data

"""
This file contains two components, the population of the original evolutionary algorithm 
that was kept for convenience purposes and the logger that grew from the
requirement of keeping track of the simulation runs
"""

ACTIVE_PARAMETERS = ["asc_car_d_mu", "b_tt_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "b_tt_car_p_mu",
                     "b_tt_put_mu", "b_tt_ped", "asc_bike_mu", "b_tt_bike_mu", "b_cost", "b_cost_put",
                     #"asc_car_d_sig", "asc_car_p_sig", "asc_put_sig", "asc_ped_sig", "asc_bike_sig", "b_tt_car_p_sig",
                     #"b_tt_car_d_sig", "b_tt_put_sig", "b_tt_bike_sig",
                     "b_u_put",  "b_logsum_acc_put",
                     "elasticity_acc_put", "b_park_car_d", "elasticity_parken"]

"""
"""

class Logger:
    def __init__(self):
        self.start_time = time.time()
        self.old_time = time.time()
        self.new_time = time.time()
        self.iteration = 1
        self.csv = []
        self.title_column = ""

    def log(self, population, current_individual=None):
        self.new_time = time.time()
        c = Comparison(current_individual.data, population.target)
        if len(population.population) == 0 and current_individual is not None:
            string = f"{c.__str__()}, {self.iteration}, {self.new_time - self.start_time}, {population.configuration()}, " \
                     f"{c.__str__()}, {current_individual.yaml.get_seed()}"

        elif current_individual is not None:
            string = f"{Comparison(population.best().data, population.target).__str__()}, {self.iteration}, {self.new_time - self.start_time}, {population.configuration()}, " \
                f"{c.__str__()}, {current_individual.yaml.get_seed()}"
        else:
            string = f"{Comparison(population.best().data, population.target).__str__()}, {self.iteration}, {self.new_time - self.start_time}, {population.configuration()}, UNKNOWN, UNKNOWN"
        print(string)
        self.csv.append(string)
        self.old_time = time.time()


    def log_detailed(self, population, current_individual=None, increase_counter=False):
        self.new_time = time.time()
        c = Comparison(current_individual.data, population.target)
        self.title_column = self.detailed_column_description(c)
        if len(population.population) == 0 and current_individual is not None:

            string = f"{self.iteration}, {self.new_time - self.start_time}, {current_individual.yaml.get_seed()}, {current_individual.fraction_of_pop()}, {c.logger_vals()}, {population.configuration()}, " \
                     f"{c.logger_vals()}"

        elif current_individual is not None:
            best = Comparison(population.best().data, population.target)
            string = f"{self.iteration}, {self.new_time - self.start_time}, {current_individual.yaml.get_seed()}, {current_individual.fraction_of_pop()}, {best.logger_vals()}, {population.configuration()}, " \
                f"{c.logger_vals()}"
        else:
            best = Comparison(population.best().data, population.target)
            string = f"{self.iteration}, {self.new_time - self.start_time}, {current_individual.yaml.get_seed()}, {current_individual.fraction_of_pop()}, {best.logger_vals()}, {population.configuration()}, UNKNOWN, UNKNOWN"
        print(string)
        self.csv.append(string)
        if increase_counter:
            self.iteration += 1
        self.old_time = time.time()

    def detailed_column_description(self, comparison):
        return f"iteration, time, seed, size, {comparison.logger_keys('_best')}, combine_func, mutation_func, initialize_func, replace_func, selection_func, individual_constructor, " \
        f"{comparison.logger_keys('_current')}"

    def append_to_csv(self, string):
        self.csv = [s + string for s in self.csv]

    def print_csv(self):

        return "\n".join([self.title_column] + self.csv)


class Population:
    def __init__(self, target=None, seed=1, combine_func=combine.basic_combine, mutation_func=mutate.mutate
                 , initialize_func=initialization.basic_initialization, replace_func=replace.replace_worst_element,
                 select_func=selection.tournament_selection, individual_constructor=Individual, param_vector=ACTIVE_PARAMETERS,
                 fraction_of_pop_size=0.02):
        self.target = target
        self.seed = seed
        self.combine_func = combine_func
        self.mutation_func = mutation_func
        self.initialize_func = initialize_func
        self.replace_func = replace_func
        self.selection_func = select_func
        self.individual_constructor = individual_constructor
        self.population = []
        self.logger = Logger()
        self.active_parameters = param_vector
        self.ind_size = fraction_of_pop_size
        pass

    def __getitem__(self, item):
        self.population[item]

    def __repr__(self):
        return "\n".join([str(x) for x in self.population])

    def __str__(self):
        return str([x.fitness for x in self.population])

    def __len__(self):
        return len(self.population)

    def configuration(self):
        return ", ".join([x.__name__ for x in [self.combine_func, self.mutation_func, self.initialize_func, self.replace_func, self.selection_func, self.individual_constructor]])

    def best(self):
        return max(self.population)

    def data_requirements(self):
        all_requirements = set()
        for p in self.active_parameters:
            all_requirements = set.union(all_requirements, set(Parameter(p).requirements.keys()))
        return all_requirements

    def set_target(self, target: Data):
        self.target = target

    def initialize(self, size):
        self.initialize_func(self, size, ACTIVE_PARAMETERS)

    def select(self):
        return self.selection_func(self)

    def _help_constructor(self, seed=None):
        if seed is None:
            seed = self.seed
        return self.individual_constructor(seed, self.active_parameters, self.ind_size)

    def combine(self, ind1, ind2):
        child = self.combine_func(ind1, ind2, self._help_constructor(), self.target, self.active_parameters)
        self._run(child)

        #print(f"Parent fitness: {ind1.fitness} {ind2.fitness} -> {child.fitness}: {child.active_values()}")
        return child

    def mutate(self, ind1):
        mutation = self.mutation_func(ind1, self._help_constructor(), self.target)
        self._run(mutation)

        return mutation

    def insert(self, ind1):
        self.replace_func(self, ind1)

    def compare(self, ind1, ind2):
        return 0

    def save(self, path):
        for i, x in enumerate(self.population):
            x.save(path + "/individual_" + str(i))

    def load(self, path):
        for x in Path(path).iterdir():
            ind = self._help_constructor()
            ind.load(x)
            self.population.append(ind)
        self.fitness_for_all_individuals()

    def random_individual(self, make_basic=False):
        individual = self._help_constructor()
        if make_basic:
            individual.make_basic(nullify_exponential_b_tt=True)

        individual.randomize()
        self._run(individual)

        return individual

    def set_random_individual_as_target(self):
        individual = self._help_constructor()
        individual.randomize()
        individual.run()
        self.set_target(individual.data)
        return individual

    def seed_individual(self, seed):
        individual = self._help_constructor(seed=seed)
        self._run(individual)
        return individual

    def _run(self, individual):
        assert self.data_requirements().issubset(set(individual.requirements))
        individual.run()
        self.logger.log_detailed(self, individual)
        self.logger.iteration += 1
        individual.set_fitness(self.target)

    def append(self, ind):
        self.population.append(ind)

    def fitness_for_all_individuals(self):
        [x.set_fitness(self.target) for x in self.population]

    def similarities(self, individual):
        l = [x.similarity(individual) for x in self.population]
        #print(f"Similis: {l} best: {l.index(max(l))}")
        return [l.index(x) for x in sorted(l, reverse=True)]

    def draw_boundaries(self):
        big = self.population[0].data.traffic_demand.accumulate_padded(["tripMode"])
        for i, ind in enumerate(self.population):
            x = ind.data.traffic_demand.accumulate_padded(["tripMode"])
            x = x.rename(columns={"active_trips": "active_trips" + str(i)})
            big = big.join(x)
        big["min"] = big.min(axis=1)
        big["max"] = big.max(axis=1)
        big = big[["min", "max"]]
        big["target"] = self.target.traffic_demand.accumulate_padded(["tripMode"])
        big["best"] = self.best().data.traffic_demand.accumulate_padded(["tripMode"])

        big = big.rolling(60, center=True, min_periods=1).mean()
        big = big.reset_index()
        visualization.generic_min_max_best(big, "tripMode")

    def draw_boundaries_traveltime(self):
        big = self.population[0].data.travel_time.get_data_frame()
        big = big.set_index(["tripMode", "durationTrip"])
        for i, ind in enumerate(self.population):
            x = ind.data.travel_time.get_data_frame()
            x = x.rename(columns={"count": "count" + str(i)})
            x = x.set_index(["tripMode", "durationTrip"])
            big = big.join(x, how="outer")
        #big = big.fillna(0)
        big["min"] = big.min(axis=1)
        big["max"] = big.max(axis=1)
        big = big[["min", "max"]]
        big["target"] = self.target.travel_time.get_data_frame().set_index(["tripMode", "durationTrip"])
        big["best"] = self.best().data.travel_time.get_data_frame().set_index(["tripMode", "durationTrip"])
        big = big.reset_index()
        visualization.generic_min_max_best_travel_time(big, "tripMode")

    def __help_plot_all(self, mode, df_get_method, IDString):
        big = df_get_method(self.population[0].data)
        big = big.set_index(["tripMode", IDString])
        names = ["target"]
        for i, ind in enumerate(self.population):
            x = df_get_method(ind.data)
            name = "count" + str(i)
            names.append(name)
            x = x.rename(columns={"count": name})
            x = x.set_index(["tripMode", IDString])
            big = big.join(x, how="outer")

        big["target"] = df_get_method(self.target).set_index(["tripMode", IDString])
        big = big.reset_index()
        visualization.generic_smol_plot(big, "tripMode", names, IDString, mode)
        return big

    def draw_all_traveltime(self, mode):
        return self.__help_plot_all(mode, lambda x: x.travel_time.get_data_frame(), "durationTrip")

    def draw_all_traveldistance(self, mode):
        return self.__help_plot_all(mode, lambda x: x.travel_distance.get_data_frame(), "distanceInKm")

    def draw_boundaries_modal_split(self, sort=True):
        y = self.population.copy()
        if sort:
            y.sort()
        temp = [x.data for x in y]
        visualization.draw_modal_split(temp + [self.target])


class OldPopulation:
    def __init__(self, target=None, seed=1):
        self.target = target
        self.seed = seed
        self.population = []
        pass

    def __getitem__(self, item):
        return self.population[item]

    def best(self):
        return max(self.population)

    def draw_best(self):
        best = max(self.population)
        a, b, c = best.data.draw(self.target)





