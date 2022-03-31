import logging

import visualization
from calibration import tuning
from calibration.evolutionary.individual import Individual
from calibration.evolutionary.population import Population
from calibration.tuning import TuningOptions
from configurations.observations import ObserverOptions, ModalSplitObservation, TimeModeObservation
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

def start_individual(param_list, comparison_data, metric, pop, seed):
    individual = Individual(seed, param_list)
    start_values = individual.average_value_list()
    individual.set_list(start_values)
    individual.run()
    set_fitness(individual, comparison_data, metric) # Because the logging requires a desired metric for the comp to the other algos
    log_and_save_individual(individual, pop, "", "") # Start element should be logged
    return individual


def tune(tuning_parameter_list, comparison_data, metric, seed=-1):
    pop = Population()
    pop.set_target(comparison_data)
    individual = start_individual(tuning_parameter_list, comparison_data, metric, pop, seed)
    opt = ObserverOptions()
    opt.use_better_travel_method = True
    individual.change_observer_options(opt)

    tuning_options = TuningOptions()

    individual = tune_travel_time_parameters(tuning_parameter_list, individual, comparison_data, metric, tuning_options, pop)
    individual.parameter_name_list = tuning_parameter_list
    print(">>>>>>>>>>>>>>>>>>")
    print(individual)
    print(">>>>>>>>>>>>>>>>>>")

    individual = tune_asc_parameters(tuning_parameter_list, individual, comparison_data, metric, tuning_options, pop)
    individual.parameter_name_list = tuning_parameter_list
    print(">>>>>>>>>>>>>>>>>>")
    print(individual)
    print(">>>>>>>>>>>>>>>>>>")

    result = pop.logger.print_csv()

    print(result)
    return pop, result

class Tuner:
    def __init__(self, tuning_parameter_list, comparison_data, metric, seed=-1):
        self.tuning_parameter_list = tuning_parameter_list
        self.comparison_data = comparison_data
        self.metric = metric
        self.seed = seed
        self.pop = Population()
        self.pop.set_target(comparison_data)
        self.individual = start_individual(tuning_parameter_list, comparison_data, metric, self.pop, seed)
        self.opt = ObserverOptions()
        self.opt.use_better_travel_method = True
        self.individual.change_observer_options(self.opt)
        self.func = execute_with_removal_and_readdal
        self.tuning_options = TuningOptions()
        self.tuning_options.epsilon = 0.02
        self.tuning_options.num_steps_hard_limit = 3

    def tune_beta_travel_cost(self):
        print("Tuning B_COST")
        self.individual = tune_travel_cost_parameters(self.tuning_parameter_list, self.individual, self.comparison_data, self.metric,
                                                 self.tuning_options, self.pop, func=self.func)
        assert self.individual.parameter_name_list == self.tuning_parameter_list

    def tune_beta_travel_time(self):
        print("Tuning B_TT")
        self.individual = tune_travel_time_parameters(self.tuning_parameter_list, self.individual, self.comparison_data, self.metric,
                                                 self.tuning_options, self.pop, func=self.func)
        assert self.individual.parameter_name_list == self.tuning_parameter_list

    def tune_alpha(self):
        print("Tuning ASC")
        self.individual = tune_asc_parameters(self.tuning_parameter_list, self.individual, self.comparison_data, self.metric,
                                                 self.tuning_options, self.pop, func=self.func)
        assert self.individual.parameter_name_list == self.tuning_parameter_list

    def print(self):
        print(self.individual)

    def error_result(self):
        return self.tuning_options.print_csv()

    def result(self):
        result = self.pop.logger.print_csv()

        print(result)
        return self.pop, result


def subroutine_default(tuner):
    tuner.tune_beta_travel_cost()
    tuner.print()
    tuner.tune_beta_travel_time()
    tuner.print()
    tuner.tune_alpha()
    tuner.print()


def subroutine_fixed_quantiles(tuner):
    tuner.opt.use_better_travel_method = False  # This disables quantile guessing so the quantiles are fixed
    tuner.opt.set_quantile_with_name("basic_quantiles", [.1, .2, .3, .4, .5, .6, .7, .8, .9])
    tuner.tuning_options.use_better_bounds_for_guessing = False

    tuner.tune_beta_travel_cost()
    tuner.tune_beta_travel_time()
    tuner.tune_alpha()


def subroutine_better_quantiles(tuner):
    tuner.opt.use_better_travel_method = True  # Quantiles are now calculated on a variable position
    tuner.opt.set_quantile_with_name("basic_quantiles", [.1, .2, .3, .4, .5, .6, .7, .8, .9])
    tuner.tuning_options.use_better_bounds_for_guessing = False

    tuner.tune_beta_travel_cost()
    tuner.tune_beta_travel_time()
    tuner.tune_alpha()


def s2(tuner):
    """
    Optimizes only cost and uses the bad recognition with massive search depth to deliberately run into a softlock
    """
    tuner.opt.use_better_travel_method = True
    tuner.opt.set_quantile_with_name("only5", [.5])
    tuner.tuning_options.num_steps_soft_limit = 1
    tuner.tuning_options.num_steps_hard_limit = 1
    tuner.tuning_options.use_better_bounds_for_guessing = False
    tuner.tune_beta_travel_cost()


def s3(tuner):
    tuner.opt.use_better_travel_method = True
    tuner.opt.set_quantile_with_name("only5", [.5])
    tuner.tuning_options.num_steps_soft_limit = 1
    tuner.tuning_options.num_steps_hard_limit = 1
    tuner.tuning_options.use_better_bounds_for_guessing = False
    tuner.tune_beta_travel_time()
    tuner.tuning_options.epsilon = 0.0000001
    tuner.tune_alpha()


def tune_new(tuning_parameter_list, comparison_data, metric, seed=-1, subroutine=subroutine_default):
    t = Tuner(tuning_parameter_list, comparison_data, metric, seed)
    subroutine(t)
    print(t.error_result())
    pop, result = t.result()
    return pop, result, t.error_result()


def temp2tune(tuning_parameter_list, comparison_data, metric):
    pop = Population()
    pop.set_target(comparison_data)

    options = TuningOptions()
    func = execute_with_removal
    individual = start_individual(tuning_parameter_list, comparison_data, metric, pop)
    individual = tune_travel_time_parameters(tuning_parameter_list, individual, comparison_data, metric, options,  pop, func=func)
    print(">>>>>>>>>>>>>>>>>>")
    print(individual)
    print(">>>>>>>>>>>>>>>>>>")

    errors = sorted_errors(individual, comparison_data)
    individual = tune_asc_parameters(tuning_parameter_list, individual, comparison_data, metric, options, pop, func=func)
    print(">>>>>>>>>>>>>>>>>>")
    print(individual)
    print(">>>>>>>>>>>>>>>>>>")

    individual = tune_travel_time_parameters(tuning_parameter_list, individual, comparison_data, metric, options, pop, func=func)
    print(">>>>>>>>>>>>>>>>>>")
    print(individual)
    print(">>>>>>>>>>>>>>>>>>")

    individual = tune_asc_parameters(tuning_parameter_list, individual, comparison_data, metric, options, pop, func=func)
    print(">>>>>>>>>>>>>>>>>>")
    print(individual)
    print(">>>>>>>>>>>>>>>>>>")
    result = pop.logger.print_csv()

    print(result)
    return pop, result



def execute_parameters_in_list(params, individual, comparison_data, metric, opt, population=None):
    temp_individual = individual.copy()
    temp_individual.parameter_name_list = params
    for i in range(opt.number.number_iterations):
        errors = sorted_errors(temp_individual, comparison_data)
        max_tuple = errors[-1]
        min_tuple = errors[0]
        if abs(max_tuple[1]) > abs(min_tuple[1]):
            p_name = max_tuple[0]
        else:
            p_name = min_tuple[0]
        print(f"The Name of the parameter SI: {p_name}")
        temp_individual = tuning.tune(temp_individual, comparison_data, individual[p_name], options=opt, population=population, metric=metric)
        draw(temp_individual, comparison_data)
    return temp_individual



def _help_tune_sublist(tuning_parameter_list, params, individual, comparison_data, metric, opt, population, func):
    if len(params) == 0:
        logging.warning("Warning list contains no parameters")
        return individual
    ind = func(params, individual, comparison_data, metric, opt, population)
    ind.parameter_name_list = tuning_parameter_list
    return ind


def tune_travel_cost_parameters(tuning_parameter_list, individual, comparison_data, metric, opt, population=None, func=execute_parameters_in_list):
    params = list(filter(lambda x: '_cost' in x, tuning_parameter_list))
    return _help_tune_sublist(tuning_parameter_list, params, individual, comparison_data, metric, opt, population, func)


def tune_travel_time_parameters(tuning_parameter_list, individual, comparison_data, metric, opt, population=None, func=execute_parameters_in_list):
    params = list(filter(lambda x: 'b_tt' in x, tuning_parameter_list))
    return _help_tune_sublist(tuning_parameter_list, params, individual, comparison_data, metric, opt, population, func)


def tune_asc_parameters(tuning_parameter_list, individual, comparison_data, metric, opt, population=None, func=execute_parameters_in_list):
    params = list(filter(lambda x: 'b_tt' not in x and '_cost' not in x, tuning_parameter_list))
    return _help_tune_sublist(tuning_parameter_list, params, individual, comparison_data, metric, opt, population, func)


def execute_with_removal(params, individual, comparison_data, metric, opt, population=None):
    temp_individual = individual.copy()
    params_copy = params.copy()
    temp_individual.parameter_name_list = params_copy
    while params_copy:
        errors = sorted_errors(temp_individual, comparison_data)
        print(errors)
        max_tuple = errors[-1]
        min_tuple = errors[0]
        if abs(max_tuple[1]) > abs(min_tuple[1]):
            p_name = max_tuple[0]
        else:
            p_name = min_tuple[0]
        print(f"The Name of the parameter IS: {p_name}")
        temp_individual = tuning.tune(temp_individual, comparison_data, individual[p_name], options=opt, population=population, metric=metric)
        draw(temp_individual, comparison_data)
        params_copy.remove(p_name)
        temp_individual.parameter_name_list = params_copy
        print(temp_individual.parameter_name_list)
    return temp_individual


def get_appropriate_string_from_mode_and_effect(transport_mode, su):
    d = {
        0: "bike",
        1: "car_d",
        2: "car_p",
        3: "ped",
        4: "put"
    }
    if su == "alpha":
        return "asc_" + d[transport_mode] + "_mu"
    elif su == "beta_time" and transport_mode != 3:
        return "b_tt_" + d[transport_mode] + "_mu"
    elif su == "beta_time" and transport_mode == 3:
        return "b_tt_" + d[transport_mode]
    elif su == "beta_cost":
        append = "" if transport_mode == 1 else "_put"
        return "b_cost" + append


def execute_with_removal_and_readdal(params, individual, comparison_data, metric, opt, population=None):
    temp_individual = individual.copy()
    params_copy = params.copy()
    temp_individual.parameter_name_list = params_copy
    while params_copy:
        errors = sorted_errors(temp_individual, comparison_data)
        print(errors)
        max_tuple = errors[-1]
        min_tuple = errors[0]
        if abs(max_tuple[1]) > abs(min_tuple[1]):
            p_name = max_tuple[0]
        else:
            p_name = min_tuple[0]
        param = individual[p_name]
        if len(param.requirements) > 1:
            main_p = None
            if type(param.observer) is ModalSplitObservation:
                main_p = get_appropriate_string_from_mode_and_effect(param.requirements["tripMode"], "alpha")

            elif type(param.observer) is TimeModeObservation:
                main_p = get_appropriate_string_from_mode_and_effect(param.requirements["tripMode"], "beta_time")
            elif type(param.observer) is TimeModeObservation:
                main_p = get_appropriate_string_from_mode_and_effect(param.requirements["tripMode"], "beta_cost")
            print(f"Main Para {main_p}")
            if main_p is not None and main_p not in params_copy:
                print("Appending")
                params_copy.append(main_p)
        print(f"The Name of the parameter IS: {p_name}")
        temp_individual = tuning.tune(temp_individual, comparison_data, individual[p_name], options=opt, population=population, metric=metric)
        draw(temp_individual, comparison_data)
        params_copy.remove(p_name)
        temp_individual.parameter_name_list = params_copy
        print(temp_individual.parameter_name_list)
    return temp_individual