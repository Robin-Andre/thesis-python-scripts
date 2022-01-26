"""
Repeatedly running a simulation with random parameters is the simplest form
of calibration. This method creates a population with size 1 and keeps generating
a random individual.
"""
import time

from calibration.population import Population
import mobitopp_execution as simulation


def main():
    population = Population()
    _, data = simulation.load("../../tests/resources/compare_individual")
    population.set_target(data)
    start = time.time()
    population.initialize(1)
    population.fitness_for_all_individuals()
    end = time.time()
    log(1, end - start, population.best().fitness, population.best().fitness)
    for i in range(100):
        start = time.time()
        ind = population.random_individual()
        end = time.time()
        log(i + 2, end - start, ind.fitness, population.best().fitness)
        population.replace_worst_non_forced(ind)


def log(iteration, time_diff, current_element, best_element):
    print(f"{iteration}, {time_diff}, {current_element}, {best_element}")


if __name__ == '__main__':
    main()