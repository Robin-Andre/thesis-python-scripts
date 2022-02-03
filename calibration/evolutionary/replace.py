

def replace_worst_non_forced(population, individual):
    worst = min(population.population)
    worst_index = population.population.index(worst)
    if individual.fitness > worst.fitness:
        population.population[worst_index] = individual


def replace_worst_element(population, individual):
    worst = min(population.population)
    worst_index = population.population.index(worst)
    population.population[worst_index] = individual


def fancy_replace(population, individual):
    for number in population.similarities(individual):
        if population.population[number].fitness < individual.fitness:
            population.population[number] = individual
            return
    print("Found no worse element, no replacement done")