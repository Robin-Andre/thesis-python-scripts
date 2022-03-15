import random
from pathlib import Path

import numpy
import pygad


import mobitopp_execution as simulation
from calibration.evolutionary.individual import Individual, ModalSplitIndividual, DestinationIndividual
from calibration.evolutionary.population import Population
from configurations import SPECS
from metrics.data import Comparison

PARAM_LIST = ["asc_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "asc_bike_mu"]
INDIVIDUAL_CONSTRUCTOR = DestinationIndividual


def tune(tuning_parameter_list, comparison_data, metric, seed=101, experiment_name="pygad_genetic_algorithm"):

    random.seed(seed)
    build_folders(experiment_name)
    individual = Individual(param_list=tuning_parameter_list)
    gene_space = individual.pygad_bound_dict()
    pop = Population(param_vector=tuning_parameter_list)
    pop.set_target(comparison_data)
    fitness_function = fitness_func_factory(comparison_data, tuning_parameter_list, Individual, metric, pop, experiment_name, seed)

    num_generations = 50
    num_parents_mating = 4

    sol_per_pop = 8
    num_genes = len(tuning_parameter_list)
    init_range_low = 0
    init_range_high = 25

    parent_selection_type = "sss"
    keep_parents = 1

    crossover_type = "single_point"

    mutation_type = "random"
    mutation_percent_genes = 10

    ga_instance = pygad.GA(num_generations=num_generations,
                           num_parents_mating=num_parents_mating,
                           fitness_func=fitness_function,
                           sol_per_pop=sol_per_pop,
                           num_genes=num_genes,
                           init_range_low=init_range_low,
                           init_range_high=init_range_high,
                           gene_space=gene_space,
                           parent_selection_type=parent_selection_type,
                           keep_parents=keep_parents,
                           crossover_type=crossover_type,
                           mutation_type=mutation_type,
                           mutation_percent_genes=mutation_percent_genes)

    ga_instance.run()

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print(solution, solution_fitness, solution_idx)

    result = pop.logger.print_csv()
    write(result, "DEFAULT", experiment_name)

def build_folders(folder):
    folder_path = Path(SPECS.EXP_PATH + folder)
    csv_path = Path(SPECS.EXP_PATH + folder + "/csv")
    data_path = Path(SPECS.EXP_PATH + folder + "/data")
    for x in [folder_path, csv_path, data_path]:
        if not x.exists():
            print(f"{x} does not exist:...creating")
            x.mkdir()



def write(result, experiment, folder):

    with open(SPECS.EXP_PATH + folder + f"/{experiment}.csv", "w+") as file:
        file.write(result)

def fitness_func_factory(data, param_list, ind_constructor, metric, population, experiment_name, seed=-1):
    p = Path(SPECS.EXP_PATH + experiment_name + "/data/seed_" + str(seed))
    p.mkdir(exist_ok=True)
    def fitness_func(solution, idx):
        print(param_list)
        individual = ind_constructor(param_list=param_list)
        individual.set_list(solution)

        output = individual.run()
        c = Comparison(individual.data, data)
        value = c.mode_metrics[metric]
        individual.fitness = -value

        individual.save(SPECS.EXP_PATH + experiment_name + "/data/seed_" + str(seed) + "/" + str(population.logger.iteration))

        population.append(individual)
        population.logger.log_detailed(population, individual, increase_counter=True)

        print(f"value is {value}")
        #fitness = individual.evaluate_fitness(data)
        #a, b, c = individual.draw(reference=data)
        #a.show()
        #        c.show()
        #print(fitness)
        return -value
    return fitness_func


def main():
    yaml, data = simulation.load("../tests/resources/compare_individual")

    p_list = list(yaml.mode_config().get_main_parameters_name_only())

    ind_constructor = ModalSplitIndividual
    d = ind_constructor(param_list=p_list)

    gene_space = d.pygad_bound_dict()
    print(gene_space)

    fitness_function = fitness_func_factory(data, p_list, ind_constructor)

    num_generations = 50
    num_parents_mating = 4

    sol_per_pop = 8
    num_genes = len(p_list)
    init_range_low = 0
    init_range_high = 25

    parent_selection_type = "sss"
    keep_parents = 1

    crossover_type = "single_point"

    mutation_type = "random"
    mutation_percent_genes = 10

    ga_instance = pygad.GA(num_generations=num_generations,
                           num_parents_mating=num_parents_mating,
                           fitness_func=fitness_function,
                           sol_per_pop=sol_per_pop,
                           num_genes=num_genes,
                           init_range_low=init_range_low,
                           init_range_high=init_range_high,
                           gene_space=gene_space,
                           parent_selection_type=parent_selection_type,
                           keep_parents=keep_parents,
                           crossover_type=crossover_type,
                           mutation_type=mutation_type,
                           mutation_percent_genes=mutation_percent_genes)

    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    print("Parameters of the best solution : {solution}".format(solution=solution))
    print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))

    #prediction = numpy.sum(numpy.array(function_inputs) * solution)
    #print("Predicted output based on the best solution : {prediction}".format(prediction=prediction))


if __name__ == "__main__":
    main()
