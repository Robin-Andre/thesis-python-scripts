"""
A relic from creating the own evolutionary algorithm
"""
def basic_initialization(population, size, parameter_list):
    for i in range(size):
        individual = population.individual_constructor(population.seed)
        individual.randomize()
        individual.run()
        population.population.append(individual)

def initialize_generous(population, size, parameter_list):
    mode_list = [0, 1, 2, 3, 4]
    for i in mode_list:
        print(mode_list)
        temp = mode_list.copy()
        temp.remove(i)
        print(temp)
        individual1 = population.individual_constructor(population.seed)
        individual2 = population.individual_constructor(population.seed)
        individual1.randomize_to_bound(parameter_list, [i])
        individual2.randomize_to_bound(parameter_list, temp)
        print(f"Running pref: {i}")
        individual1.run()
        print(f"Running denied: {i}")
        individual2.run()
        population.population.append(individual1)
        population.population.append(individual2)
