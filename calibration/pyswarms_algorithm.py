import random

import numpy
from pyswarms.single.global_best import GlobalBestPSO
import mobitopp_execution as simulation
from calibration.evolutionary.individual import ModalSplitIndividual, Individual

from pyswarms.utils.functions import single_obj as fx

from calibration.evolutionary.population import Population
from configurations import SPECS
from metrics.data import Comparison


def tune(tuning_parameter_list, comparison_data, metric, seed=101, experiment_name="pyswarms_algorithm", descriptor=None, individual_constructor=Individual):
    random.seed(seed)
    numpy.random.seed(seed)
    if descriptor is None:
        descriptor = str(seed) + "_metric_" + metric + "/"
    pop = Population(param_vector=tuning_parameter_list)
    pop.set_target(comparison_data)
    loss_function = loss_factory(tuning_parameter_list, comparison_data, metric, pop, experiment_name, descriptor)
    individual = individual_constructor(param_list=tuning_parameter_list)
    bounds = individual.pyswarms_bound_lists()

    options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
    optimizer = GlobalBestPSO(n_particles=10, dimensions=len(tuning_parameter_list), options=options, bounds=bounds)

    cost, pos = optimizer.optimize(loss_function, iters=10)
    print(pos)
    result = pop.logger.print_csv()
    print(result)
    return pos, result


def log_and_save_individual(individual, population, experiment_name, descriptor):
    individual.save(SPECS.EXP_PATH + experiment_name + "/data/" + descriptor + "/" + str(population.logger.iteration))
    population.append(individual)
    population.logger.log_detailed(population, individual, increase_counter=True)


def loss_factory(p_list, data, metric, population, ex_name, descriptor):

    def loss(np_array):

        fitness_vals = []
        for x in np_array:
            ind = Individual(param_list=p_list)
            ind.set_list(x)
            ind.run()
            c = Comparison(ind.data, data)
            fitness = c.mode_metrics[metric]
            ind.fitness = -fitness # FItness has to be negative for logging but positive for spsp
            log_and_save_individual(ind, population, ex_name, descriptor)

            print(fitness)
            fitness_vals.append(fitness)

        return numpy.asarray(fitness_vals)
    return loss

"""def test(a):
    yaml, data = simulation.load("../tests/resources/compare_individual")
    p_list = list(yaml.mode_config().get_main_parameters_name_only())

    fitness_vals = []
    for x in a:


        individual = ind_constructor(param_list=p_list)
        individual.set_list(x)
        individual.run()

        #a, b, c = individual.draw(reference=data)
        #a.show()

        fitness = individual.evaluate_fitness(data)
        print(-fitness)
        fitness_vals.append(-fitness) # Pyswarms optimizes towards a minima so the fitness needs to be big if invalid

    return numpy.asarray(fitness_vals)"""


"""if __name__ == "__main__":

    yaml, data = simulation.load("../tests/resources/compare_individual")
    p_list = list(yaml.mode_config().get_main_parameters_name_only())
    #p_list = ["asc_car_d_mu"]
    ind_constructor = ModalSplitIndividual
    d = ind_constructor(param_list=p_list)

    d.run()
    data = d.data
    # instatiate the optimizer
    bounds = d.pyswarms_bound_lists()

    print(bounds)


    options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
    optimizer = GlobalBestPSO(n_particles=10, dimensions=len(p_list), options=options, bounds=bounds)

    # now run the optimization, pass a=1 and b=100 as a tuple assigned to args

    cost, pos = optimizer.optimize(test, iters=10)
    print(pos)
    x = d.copy()
    x.set_list(pos)
    x.run()

    a, b, c = x.draw(reference=data)
    a.show()
    b.show()
"""

