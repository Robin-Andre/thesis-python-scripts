import visualization
from calibration import tuning
from calibration.evolutionary.individual import Individual
from calibration.evolutionary.population import Population
from metrics.data import Comparison


def draw(ind, data):
    ind.data.draw_modal_split(reference=data)
    x = ind.data.travel_time.draw(reference=data.travel_time)

    x.show()

def log_and_save_individual(individual, population, experiment_name, descriptor):
    #individual.save(SPECS.EXP_PATH + experiment_name + "/data/" + descriptor + "/" +  str(population.logger.iteration))
    population.append(individual)
    population.logger.log_detailed(population, individual, increase_counter=True)


def set_fitness(individual, data, metric):
    c = Comparison(individual.data, data)
    value = c.mode_metrics[metric]
    individual.fitness = -value

def sorted_errors(individual, comparison_data):
    errors = individual.errors(comparison_data)
    errors.sort(key=lambda x: x[1])
    print(errors)
    return errors

def tune(tuning_parameter_list, comparison_data, metric):
    pop = Population()
    pop.set_target(comparison_data)
    individual = Individual(-1, tuning_parameter_list)
    start_values = individual.average_value_list()
    individual.set_list(start_values)
    individual.run()
    set_fitness(individual, comparison_data, metric)
    log_and_save_individual(individual, pop, "", "")
    individual = tune_travel_time_parameters(tuning_parameter_list, individual, comparison_data, metric, pop)
    individual.parameter_name_list = tuning_parameter_list
    print(">>>>>>>>>>>>>>>>>>")
    print(individual)
    print(">>>>>>>>>>>>>>>>>>")

#log_and_save_individual(individual, pop, "", "")
    errors = sorted_errors(individual, comparison_data)
    individual = tune_asc_parameters(tuning_parameter_list, individual, comparison_data, metric, pop)
    individual.parameter_name_list = tuning_parameter_list
    print(">>>>>>>>>>>>>>>>>>")
    print(individual)
    print(">>>>>>>>>>>>>>>>>>")

#log_and_save_individual(individual, pop, "", "")
    result = pop.logger.print_csv()

    print(result)
    return pop, result


def temp2tune(tuning_parameter_list, comparison_data, metric):
    pop = Population()
    pop.set_target(comparison_data)
    individual = Individual(-1, tuning_parameter_list)
    start_values = individual.average_value_list()
    individual.set_list(start_values)
    individual.run()
    set_fitness(individual, comparison_data, metric)
    log_and_save_individual(individual, pop, "", "")
    individual = tune_travel_time_parameters(tuning_parameter_list, individual, comparison_data, metric, pop)
    individual.parameter_name_list = tuning_parameter_list
    print(">>>>>>>>>>>>>>>>>>")
    print(individual)
    print(">>>>>>>>>>>>>>>>>>")

    #log_and_save_individual(individual, pop, "", "")
    errors = sorted_errors(individual, comparison_data)
    individual = tune_asc_parameters(tuning_parameter_list, individual, comparison_data, metric, pop)
    individual.parameter_name_list = tuning_parameter_list
    print(">>>>>>>>>>>>>>>>>>")
    print(individual)
    print(">>>>>>>>>>>>>>>>>>")

    individual = tune_travel_time_parameters(tuning_parameter_list, individual, comparison_data, metric, pop, num_iters=2, epsilon=0.01)
    individual.parameter_name_list = tuning_parameter_list
    print(">>>>>>>>>>>>>>>>>>")
    print(individual)
    print(">>>>>>>>>>>>>>>>>>")

    individual = tune_asc_parameters(tuning_parameter_list, individual, comparison_data, metric, pop, num_iters=2, epsilon=0.005)
    individual.parameter_name_list = tuning_parameter_list
    print(">>>>>>>>>>>>>>>>>>")
    print(individual)
    print(">>>>>>>>>>>>>>>>>>")

    #log_and_save_individual(individual, pop, "", "")
    result = pop.logger.print_csv()

    print(result)
    return pop, result


def tune_travel_time_parameters(tuning_parameter_list, individual, comparison_data, metric, population=None, num_iters=5, epsilon=0.02):
    params = list(filter(lambda x: 'b_tt' in x, tuning_parameter_list))
    assert len(params) >= 1
    print(params)
    return _unnamed_helper_function(params, individual, comparison_data, metric, population, num_iters, epsilon)


def tune_asc_parameters(tuning_parameter_list, individual, comparison_data, metric, population=None, num_iters=5, epsilon=0.02):
    params = list(filter(lambda x: 'b_tt' not in x, tuning_parameter_list))
    assert len(params) >= 1
    return _unnamed_helper_function(params, individual, comparison_data, metric, population, num_iters, epsilon)


def _unnamed_helper_function(params, individual, comparison_data, metric, population=None, num_iters=5, epsilon=0.02):

    temp_individual = individual.copy()
    print(params)
    temp_individual.parameter_name_list = params
    for i in range(num_iters):
        errors = sorted_errors(temp_individual, comparison_data)
        max_tuple = errors[-1]
        min_tuple = errors[0]
        if abs(max_tuple[1]) > abs(min_tuple[1]):
            p_name = max_tuple[0]
        else:
            p_name = min_tuple[0]
        print(f"The Name of the parameter SI: {p_name}")
        temp_individual = tuning.tune(temp_individual, comparison_data, individual[p_name], epsilon=epsilon, population=population, metric=metric)
        draw(temp_individual, comparison_data)
    return temp_individual
