"""
Repeatedly running a simulation with random parameters is the simplest form
of calibration. This method creates a population with size 1 and keeps generating
a random individual.
"""
import random
import time

from calibration.evolutionary.population import Population
import mobitopp_execution as simulation


def main():
    seed = 101
    random.seed(seed)
    population = Population(seed=seed)
    population.load("../../tests/resources/test_population")
    _, data = simulation.load("../../tests/resources/compare_individual")
    population.set_target(data)
    population.fitness_for_all_individuals()
    population.draw_boundaries()
    for i in range(50):
        print(f"Iteration {i}: {population}")
        start = time.time()
        ind1, ind2 = population.desired_partner_selection()
        child = population.combine2(ind1, ind2)
        end = time.time()
        log(i + 2, end - start, child.fitness, population.best().fitness)
        #mutation = population.mutate(child)
        #if mutation.fitness > child.fitness:
        #    population.fancy_replace(mutation)
        #else:
        population.fancy_replace(child)
        if child.fitness > population.best().fitness:# or mutation.fitness > population.best().fitness:
            population.draw_boundaries()


def log(iteration, time_diff, current_element, best_element):
    print(f"{iteration}, {time_diff}, {current_element}, {best_element}")


if __name__ == '__main__':
    main()
