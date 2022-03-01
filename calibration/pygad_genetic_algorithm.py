import numpy
import pygad


import mobitopp_execution as simulation
from calibration.evolutionary.individual import Individual, ModalSplitIndividual, DestinationIndividual

PARAM_LIST = ["asc_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "asc_bike_mu"]
INDIVIDUAL_CONSTRUCTOR = DestinationIndividual


def fitness_func_factory(data, param_list, ind_constructor):

    def fitness_func(solution, idx):
        print(param_list)
        individual = ind_constructor(param_list=param_list)
        individual.set_list(solution)

        output = individual.run()
        fitness = individual.evaluate_fitness(data)
        a, b, c = individual.draw(reference=data)
        a.show()
        #        c.show()
        print(fitness)
        return fitness
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
    #print("Parameters of the best solution : {solution}".format(solution=solution))
    #print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))

    #prediction = numpy.sum(numpy.array(function_inputs) * solution)
    #print("Predicted output based on the best solution : {prediction}".format(prediction=prediction))


if __name__ == "__main__":
    main()
