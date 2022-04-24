#TODO https://qiskit.org/documentation/_modules/qiskit/algorithms/optimizers/spsa.html
import numpy
import numpy as np
from qiskit.algorithms.optimizers import SPSA
import mobitopp_execution as simulation

from calibration.evolutionary.individual import Individual, DestinationIndividual
from calibration.evolutionary.population import Population
from configurations import SPECS
from metrics.data import Comparison


def log_and_save_individual(individual, population, experiment_name, descriptor):
    individual.save(SPECS.EXP_PATH + experiment_name + "/data/" + descriptor + "/" +  str(population.logger.iteration))
    population.append(individual)
    population.logger.log_detailed(population, individual, increase_counter=True)


def tune(tuning_parameter_list, comparison_data, metric, seed=101, experiment_name="stochastic_perturbation", descriptor=None, individual_constructor=Individual):
    numpy.random.seed(seed)
    pop = Population(param_vector=tuning_parameter_list)
    if descriptor is None:
        descriptor = str(seed) + "_metric_" + metric + "/"
    loss_func = loss_factory(tuning_parameter_list, metric, comparison_data, pop, experiment_name, descriptor, individual_constructor)
    individual = individual_constructor(param_list=tuning_parameter_list)
    pop.set_target(comparison_data)
    second_order = False
    initial_points = individual.average_value_list()
    bounds = individual.spsa_bound_lists()
    print(bounds)
    print(initial_points)
    spsa = SPSA(maxiter=150, second_order=second_order)
    params_optimized = spsa.optimize(len(tuning_parameter_list), loss_func, initial_point=initial_points, variable_bounds=bounds)
    print(params_optimized)
    result = pop.logger.print_csv()
    return params_optimized, result


def metrics(comparision, metric):
    x = comparision.mode_metrics.get(metric)
    if x is None:
        x = comparision.destination_metrics.get(metric)
    return x

def loss_factory(p_list, metric, data, population, experiment_name, descriptor, individual_constructor):

    def loss(x):
        ind = individual_constructor(param_list=p_list)
        print(list(x))
        ind.set_list(list(x))
        ind.run()
        c = Comparison(ind.data, data)
        value = metrics(c, metric)
        ind.fitness = -value # Fitness has to be negative
        log_and_save_individual(ind, population, experiment_name, descriptor)
        print(value)
        return value
    return loss


"""def loss(x, p_list, metric, data, population, experiment_name, seed):
    ind = Individual(param_list=p_list)
    print(list(x))
    ind.set_list(list(x))
    ind.run()
    c = Comparison(ind.data, data)
    value = c.mode_metrics[metric]
    ind.fitness = value
    log_and_save_individual(ind, population, experiment_name, seed, metric)
    print(value)
    return value"""


"""if __name__ == "__main__":
    parameter_list = ["asc_car_d_mu", "asc_car_p_mu", "asc_ped_mu", "asc_put_mu", "asc_bike_mu"]
    run_individual = Individual(param_list=parameter_list)
    run_individual.run()
    data = run_individual.data

    spsa = SPSA(maxiter=2, learning_rate=[1.0, 1.0], perturbation=[1.0, 1.0], second_order=True)

    metric = "LolCAt"

    result = spsa.optimize(len(parameter_list), lambda x: loss(x, parameter_list, metric, data), initial_point=[5, 5, 5, 5, 5])
    print(result)"""
