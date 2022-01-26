import random
from pathlib import Path

import numpy
import pandas
from matplotlib import pyplot as plt

import mobitopp_execution as simulation
import visualization


class Population:
    def __init__(self, target=None, seed=1):
        self.target = target
        self.seed = seed
        self.population = []
        pass

    def __getitem__(self, item):
        return self.population[item]

    def initialize(self, size):
        for i in range(size):
            individual = Individual(self.seed)
            individual.randomize()
            individual.run()
            self.population.append(individual)

    def set_target(self, target):
        self.target = target

    def fitness_for_all_individuals(self):
        [x.set_fitness(self.target) for x in self.population]

    def similarities(self, individual):
        l = [x.similarity(individual) for x in self.population]
        print(f"Similis: {l} best: {l.index(max(l))}")
        return [l.index(x) for x in sorted(l, reverse=True)]

    def random_individual(self):
        individual = Individual(self.seed)

        individual.randomize()
        individual.run()
        individual.set_fitness(self.target)
        return individual

    def random_individual_with_mutation(self):
        individual = Individual(self.seed)

        individual.randomize()
        individual.run()
        mutation = self.mutate(individual)
        individual.set_fitness(self.target)
        print(f"Random Individual with fitness: {individual.fitness} mutation : {mutation.fitness}")
        if mutation.fitness > self.best().fitness or individual.fitness > self.best().fitness:

            if individual.fitness > mutation.fitness:
                self.replace_worst_element(individual)
            else:
                self.replace_worst_element(mutation)


    def save(self, path):
        for i, x in enumerate(self.population):
            x.save(path + "/individual_" + str(i))

    def load(self, path):
        for x in Path(path).iterdir():
            ind = Individual(self.seed)
            ind.load(x)
            self.population.append(ind)

    def replace_worst_non_forced(self, individual):
        worst = min(self.population)
        worst_index = self.population.index(worst)
        if individual.fitness > worst.fitness:
            self.population[worst_index] = individual

    def replace_worst_element(self, individual):
        worst = min(self.population)
        worst_index = self.population.index(worst)
        self.population[worst_index] = individual

    def __repr__(self):
        return "\n".join([str(x) for x in self.population])

    def __str__(self):
        return str([x.fitness for x in self.population])

    def best(self):
        return max(self.population)

    def tournament_selection(self):
        a, b = random.sample(self.population, 2)
        return a if a.fitness > b.fitness else b

    def double_tournament_selection(self):
        x = random.sample(self.population, 4)
        x.sort()
        return x[-2:]

    def combine(self, ind1, ind2):
        child = Individual(self.seed)
        child.set_seed(self.seed)
        for param in ACTIVE_PARAMETERS:
            a = ind1.yaml.mode_config().parameters[param].value
            b = ind2.yaml.mode_config().parameters[param].value
            c = random.uniform(min(a, b), max(a, b))

            child.yaml.mode_config().parameters[param].set(c)
        child.run()
        child.set_fitness(self.target)
        print(f"Parent fitness: {ind1.fitness} {ind2.fitness} -> {child.fitness}: {child.active_values()}")
        return child

    def fancy_combine(self, ind1, ind2):
        child = Individual(self.ssed)
        parent1_bounds = ind1.evaluate_fitness_by_group(self.target)
        parent2_bounds = ind2.evaluate_fitness_by_group(self.target)
        for param in ACTIVE_PARAMETERS:
            a = ind1.yaml.mode_config().parameters[param]
            b = ind2.yaml.mode_config().parameters[param]
            y1 = parent1_bounds.iloc[a.requirements['tripMode']]['active_trips']
            x1 = a.value
            y2 = parent2_bounds.iloc[b.requirements['tripMode']]['active_trips']
            x2 = b.value
            if x1 - x2 < 0.1:# or numpy.sign(y1) == numpy.sign(y2):
                set_val = a.value if ind1.fitness > ind2.fitness else b.value
                child.yaml.mode_config().parameters[param].set(set_val)
                continue
            assert x1 - x2 != 0
            m = (y2 - y1) / (x2 - x1)
            c = y1 - m * x1
            target = -c / m
            target = min(a.upper_bound, max(a.lower_bound, target))
            print(f"[{a.lower_bound},{a.upper_bound}] {target}")
            assert a.upper_bound >= target >= a.lower_bound
            print(f"{param} {x1} {y1}|{x2} {y2} {target} [{a.lower_bound},{a.upper_bound}]")
            child.yaml.mode_config().parameters[param].set(target)
        child.run()
        child.set_fitness(self.target)
        print(f"Parent fitness: {ind1.fitness} {ind2.fitness} -> {child.fitness}: {child.active_values()}")
        return child

    def mutate(self, individual):
        mutation = Individual(self.seed)
        temp = individual.evaluate_fitness_by_group(self.target)
        print(temp)
        temp = -(temp / temp.abs().sum())
        print(temp)
        alpha = 0.2
        for param in ACTIVE_PARAMETERS:
            a = individual.yaml.mode_config().parameters[param]
            if a.value > 0:
                target = a.value * (1 + alpha * temp.at[a.requirements["tripMode"], "active_trips"])
                target = max(a.value, target)
            else:
                target = a.value * (1 - alpha * temp.at[a.requirements["tripMode"], "active_trips"])
                target = min(a.value, target)

            mutation.yaml.mode_config().parameters[param].set(target)
            #print(f"{param} : {target} ")
        mutation.run()
        mutation.set_fitness(self.target)
        print(f"Original {individual.fitness} Mutation {mutation.fitness}")
        return mutation

    def mutate2(self, individual):
        mutation = Individual(self.seed)
        temp = individual.evaluate_fitness_by_group(self.target)
        print(temp)
        temp = -(temp / temp.abs().sum())
        print(temp)

        alpha = 0.2
        for param in ACTIVE_PARAMETERS:

            a = individual.yaml.mode_config().parameters[param]
            target = a.value + alpha * temp.at[a.requirements["tripMode"], "active_trips"] * (a.upper_bound - a.lower_bound)

            mutation.yaml.mode_config().parameters[param].set(target)
            print(f"{param} :{a.value} -> {target} ")
        mutation.run()
        mutation.set_fitness(self.target)
        print(f"Original {individual.fitness} Mutation {mutation.fitness}")
        return mutation



    def fancy_replace(self, individual):
        for number in self.similarities(individual):
            if self.population[number].fitness < individual.fitness:
                self.population[number] = individual
                return
        print("Found no worse element, no replacement done")

    def draw_best(self):
        best = max(self.population)
        a, b, c = best.data.draw(self.target)

    def draw_boundaries(self):
        big = self.population[0].data.traffic_demand.accumulate_padded(["tripMode"])
        for i, ind in enumerate(self.population):
            x = ind.data.traffic_demand.accumulate_padded(["tripMode"])
            x = x.rename(columns={"active_trips": "active_trips" + str(i)})
            big = pandas.merge(big, x, left_index=True, right_index=True)
        big["min"] = big.min(axis=1)
        big["max"] = big.max(axis=1)
        big = big[["min", "max"]]
        big["target"] = self.target.traffic_demand.accumulate_padded(["tripMode"])
        big["best"] = self.best().data.traffic_demand.accumulate_padded(["tripMode"])

        big = big.rolling(60, center=True, min_periods=1).mean()
        big = big.reset_index()
        visualization.generic_min_max_best(big, "tripMode")

    def temp_rename2(self):
        ind1, ind2 = self.double_tournament_selection()
        child = self.fancy_combine(ind1, ind2)
        self.fancy_replace(child)

    def temp_rename(self):
        ind1, ind2 = self.double_tournament_selection()
        child = self.combine(ind1, ind2)
        self.fancy_replace(child)

    def mutate_best(self):
        self.replace_worst_non_forced(self.mutate(self.best()))

    def mutate_best2(self):
        self.replace_worst_non_forced(self.mutate2(self.best()))


ACTIVE_PARAMETERS = ["asc_car_d_mu", "b_tt_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "b_tt_car_p_mu",
                     "b_tt_put_mu", "b_tt_ped", "asc_bike_mu", "b_tt_bike_mu", "b_cost", "b_cost_put",
                     "asc_car_d_sig", "asc_car_p_sig", "asc_put_sig", "asc_ped_sig", "asc_bike_sig", "b_tt_car_p_sig",
                     "b_tt_car_d_sig", "b_tt_put_sig", "b_tt_bike_sig", "b_u_put",  "b_logsum_acc_put",
                     "elasticity_acc_put", "b_park_car_d", "elasticity_parken"]


class Individual:
    def __init__(self, seed=1):
        self.yaml = simulation.default_yaml()

        self.yaml.set_fraction_of_population(0.02)
        self.yaml.set_seed(seed)
        self.fitness = None
        self.data = None

    def __str__(self):
        return str(f"Value: {self.active_values()} Fitness: {self.fitness}")

    def __repr__(self):
        return f"{self.fitness}"

    def __lt__(self, other):
        return self.fitness < other.fitness

    def set_seed(self, value):
        self.yaml.set_seed(value)

    def randomize(self):
        self.yaml.mode_config().randomize_parameters(ACTIVE_PARAMETERS)

    def active_values(self):
        return [(self.yaml.mode_config().parameters[x].name, self.yaml.mode_config().parameters[x].value) for x in ACTIVE_PARAMETERS]

    def run(self):
        simulation.clean_result_directory()
        self.yaml.mode_config().write()
        return_code, self.data = simulation.run_mobitopp(self.yaml)
        if return_code == 1:
            print(self.yaml.mode_config())
            exit()

        self.data.reduce(["tripMode"])

    def save(self, path):
        simulation.save(self.yaml, self.data, path)

    def load(self, path):
        self.yaml, self.data = simulation.load(path)

    def set_fitness(self, compare_data):
        self.fitness = self.evaluate_fitness(compare_data)

    def evaluate_fitness(self, compare_data):
        x = self.data.traffic_demand
        y = compare_data.traffic_demand

        z = x - y

        result = (z["active_trips"] ** 2)
        return -result.sum()

    def evaluate_fitness_by_group(self, compare_data):
        x = self.data.traffic_demand
        y = compare_data.traffic_demand

        z = x - y
        z = z.groupby("tripMode").sum()
        return z

    def similarity(self, compare_individual):
        return self.evaluate_fitness(compare_individual.data)

