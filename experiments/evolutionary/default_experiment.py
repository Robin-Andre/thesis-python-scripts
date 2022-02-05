import random
import time

from calibration.evolutionary import evo_strategies
from calibration.evolutionary.population import Population
from configurations import SPECS
import mobitopp_execution as simulation


def run_experiment(seed, population, repetition, strategy=evo_strategies.simple_combine, load=True):
    random.seed(seed)
    if load:
        population.load("../../tests/resources/test_population")
    _, data = simulation.load("../../tests/resources/compare_individual")
    population.set_target(data)
    population.fitness_for_all_individuals()

    while population.logger.iteration <= repetition:
        strategy(population)

    population.logger.append_to_csv(", " + str(seed))
    return population.logger.print_csv()


def write(result, experiment, seed, folder):
    with open(SPECS.EXP_PATH + folder + f"/{experiment}_{seed}_{time.strftime('%d-%m-%Y_%H-%M')}.csv", "w+") as file:
        file.write(result)
