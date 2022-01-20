import random
from pathlib import Path

import mobitopp_execution as simulation


class Population:
    def __init__(self, target=None):
        self.target = target
        self.population = []
        pass

    def __getitem__(self, item):
        return self.population[item]

    def initialize(self, size):
        for i in range(size):
            individual = Individual()
            individual.randomize()
            individual.run()
            self.population.append(individual)

    def set_target(self, target):
        self.target = target

    def fitness_for_all_individuals(self):
        [x.set_fitness(self.target) for x in self.population]

    def similarities(self, individual):
        print([x.similarity(individual) for x in self.population])

    def save(self, path):
        for i, x in enumerate(self.population):
            x.save(path + "/individual_" + str(i))

    def load(self, path):
        for x in Path(path).iterdir():
            ind = Individual()
            ind.load(x)
            self.population.append(ind)

    def replace_worst_element(self, individual):
        worst = min(self.population)
        worst_index = self.population.index(worst)
        self.population[worst_index] = individual

    def __repr__(self):
        return "\n".join([str(x) for x in self.population])

    def __str__(self):
        return str([x.fitness for x in self.population])

    def tournament_selection(self):
        a, b = random.sample(self.population, 2)
        return a if a.fitness > b.fitness else b

    def double_tournament_selection(self):
        x = random.sample(self.population, 4)
        x.sort()
        return x[-2:]

    def combine(self, ind1, ind2):
        child = Individual()
        a = ind1.yaml.mode_config().parameters["asc_car_d_mu"].value
        b = ind2.yaml.mode_config().parameters["asc_car_d_mu"].value
        c = random.uniform(min(a, b), max(a, b))
        #print(f"{min(a, b)} {c} {max(a, b)}")

        child.yaml.mode_config().parameters["asc_car_d_mu"].set(c)
        child.run()
        child.set_fitness(self.target)
        print(f"Parent fitness: {ind1.fitness} {ind2.fitness} -> {child.fitness}: {child.yaml.mode_config().parameters['asc_car_d_mu'].value}")
        return child

    def temp_rename(self):
        ind1 = self.tournament_selection()
        ind2 = self.tournament_selection()
        child = self.combine(ind1, ind2)
        child.set_fitness(self.target)
        self.replace_worst_element(child)


class Individual:
    def __init__(self):
        self.yaml = simulation.default_yaml()

        self.yaml.set_fraction_of_population(0.01)
        self.fitness = None
        self.data = None

    def __str__(self):
        return str(f"Value: {self.yaml.mode_config().parameters['asc_car_d_mu'].value} Fitness: {self.fitness}")

    def __repr__(self):
        return f"{self.fitness}"

    def __lt__(self, other):
        return self.fitness < other.fitness

    def randomize(self):
        self.yaml.mode_config().randomize_parameters(["asc_car_d_mu"])

    def run(self):
        simulation.clean_result_directory()
        _, self.data = simulation.run_mobitopp(self.yaml)
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

    def similarity(self, compare_individual):
        return self.evaluate_fitness(compare_individual.data)

