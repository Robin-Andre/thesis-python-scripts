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



def get_gene_space(tuning_parameter_list, individual_constructor):
    individual = individual_constructor(param_list=tuning_parameter_list)
    return individual.pygad_bound_dict()


def tune(tuning_parameter_list, comparison_data, metric, seed=101, experiment_name="pygad_genetic_algorithm", descriptor=None, individual_constructor=Individual):

    random.seed(seed)
    numpy.random.seed(seed)
    if descriptor is None:
        descriptor = str(seed) + "_metric_" + metric + "/"
    build_folders(experiment_name)
    gene_space = get_gene_space(tuning_parameter_list, individual_constructor)
    pop = Population(param_vector=tuning_parameter_list)
    pop.set_target(comparison_data)

    fitness_function = fitness_func_factory(comparison_data, tuning_parameter_list, individual_constructor, metric, pop, experiment_name, descriptor)

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
    return solution, result



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


def log_and_save_individual(individual, population, experiment_name, descriptor):
    individual.save(SPECS.EXP_PATH + experiment_name + "/data/" + descriptor + "/" +  str(population.logger.iteration))
    population.append(individual)
    population.logger.log_detailed(population, individual, increase_counter=True)


def metrics(comparision, metric):
    x = comparision.mode_metrics.get(metric)
    if x is None:
        x = comparision.destination_metrics.get(metric)
    return x


def fitness_func_factory(data, param_list, ind_constructor, metric, population, experiment_name, descriptor):
    p = Path(SPECS.EXP_PATH + experiment_name + "/data/" + descriptor)
    p.mkdir(exist_ok=True)

    def fitness_func(solution, idx):
        print(param_list)
        individual = ind_constructor(param_list=param_list)
        individual.set_list(solution)

        output = individual.run()
        c = Comparison(individual.data, data)
        value = metrics(c, metric)
        individual.fitness = -value

        log_and_save_individual(individual, population, experiment_name, descriptor)

        print(f"value is {value}")

        return -value
    return fitness_func

