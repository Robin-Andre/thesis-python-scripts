"""
Repeatedly running a simulation with random parameters is the simplest form
of calibration. This method creates a population with size 1 and keeps generating
a random individual.
"""
import random
import time

from calibration.evolutionary import selection, replace, individual, evo_strategies
from calibration.evolutionary.population import Population
import mobitopp_execution as simulation
from configurations import SPECS


def run_experiment(seed, population, repetition):
    random.seed(seed)

    population.load("../../tests/resources/test_population")
    _, data = simulation.load("../../tests/resources/compare_individual")
    population.set_target(data)
    population.fitness_for_all_individuals()
    for i in range(repetition):
        evo_strategies.simple_combine(population)
    population.logger.append_to_csv(", " + str(seed))
    return population.logger.print_csv()


def write(result, experiment, seed):
    with open(SPECS.EXP_PATH + f"MetricExperiment/{experiment}_{seed}.csv", "w+") as file:
        file.write(result)

def main():
    output = []
    repetitions = 50
    for seed in range(30, 40):
        population = Population(select_func=selection.double_tournament_selection, replace_func=replace.fancy_replace,
                            individual_constructor=individual.TravelTimeIndividual, seed=101)

        result = run_experiment(seed, population, repetitions)
        write(result, "traveltime", seed)
        print("---------------------------")
        print(result)
        print("---------------------------")
        population2 = Population(select_func=selection.double_tournament_selection, replace_func=replace.fancy_replace,
                                 individual_constructor=individual.Individual, seed=101)
        result2 = run_experiment(seed, population2, repetitions)
        write(result2, "traveldemand", seed)
        print("---------------------------")
        print(result2)
        print("---------------------------")
        population3 = Population(select_func=selection.double_tournament_selection, replace_func=replace.fancy_replace,
                                 individual_constructor=individual.ModalSplitIndividual, seed=101)
        result3 = run_experiment(seed, population3, repetitions)
        write(result3, "modalsplit", seed)
        print("---------------------------")
        print(result3)
        print("---------------------------")
        output.append(result)
        output.append(result2)
        output.append(result3)

    csv = "\n".join(output)
    print(csv)
    with open(SPECS.EXP_PATH + "MetricExperiment.csv", "w+") as file:
        file.write(csv)


if __name__ == '__main__':
    main()
