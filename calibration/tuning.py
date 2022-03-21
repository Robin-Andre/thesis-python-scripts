from calibration.evolutionary.individual import BaseIndividual
from calibration.evolutionary.population import Population
from metrics.data import Data, Comparison


def __do_population_shenanigans(copy_ind_1, population, draw, mode):
    if population is not None:
        population._run(copy_ind_1)
        population.append(copy_ind_1.copy())
        if draw:
            population.draw_all_traveltime(mode)
        else:
            population.draw_boundaries_modal_split(sort=False)
    else:
        copy_ind_1.run()


def log_and_save_individual(individual, population, experiment_name, descriptor):
    #individual.save(SPECS.EXP_PATH + experiment_name + "/data/" + descriptor + "/" +  str(population.logger.iteration))
    if population is None:
        return
    population.append(individual)
    population.logger.log_detailed(population, individual, increase_counter=True)

    draw(individual, population.target)


def draw(ind, data):
    ind.data.draw_modal_split(reference=data)
    x = ind.data.travel_time.draw(reference=data.travel_time)

    x.show()



def run_and_set_fitness(individual, data, metric):
    individual.run()
    c = Comparison(individual.data, data)
    value = c.mode_metrics[metric]
    individual.fitness = -value



def tune(individual: BaseIndividual, data_target: Data, parameter, epsilon=0.05, population=None, draw=False, metric="ModalSplit_Default_Splits_sum_squared_error"):

    #print(f"Original Value {individual[parameter].value}")

    error = parameter.error(individual, data_target)
    l_errors = [(individual[parameter].value, error)]
    #print(f"Errors {l_errors}")
    if abs(error) < epsilon:
        print("Error too small. No optimization will be done")
        return individual
    #print(f"Error1 {error}")
    copy_ind_1 = individual.copy()
    copy_ind_2 = individual.copy()
    estimate_value = copy_ind_1[parameter].observe(individual, data_target)
    copy_ind_1[parameter].set(estimate_value)
    run_and_set_fitness(copy_ind_1, data_target, metric)
    #__do_population_shenanigans(copy_ind_1, population, draw, mode=parameter.requirements["tripMode"])
    log_and_save_individual(copy_ind_1, population, "", "")
    error = copy_ind_1[parameter].error(copy_ind_1, data_target)

    l_errors.append((copy_ind_1[parameter].value, error))
    #print(f"Errors {l_errors}")
    #print(f"Error2 {error}")

    counter = 0
    stop_criterion = 3
    best_error = min([x[1] for x in l_errors])
    while abs(error) > epsilon and counter < stop_criterion:
        #print(f"Current counter {counter}")
        counter += 1

        estimate_value = copy_ind_1[parameter].observe_detailed(copy_ind_2, copy_ind_1, data_target)
        copy_ind_2 = copy_ind_1.copy()
        copy_ind_1[parameter].set(estimate_value)
        #print(copy_ind_2[parameter])
        #print(copy_ind_1[parameter])

        run_and_set_fitness(copy_ind_1, data_target, metric)
        log_and_save_individual(copy_ind_1, population, "", "")
        temp_error = copy_ind_1[parameter].error(copy_ind_1, data_target)
        if abs(temp_error) < abs(best_error):
            #print("Improvement Found")
            counter = 0
            best_error = temp_error
        error = temp_error
        l_errors.append((copy_ind_1[parameter].value, error))

        #print(f"Error3 {error}")
    #print("The error list:")
    print(l_errors)
    best_result = min(l_errors, key=lambda t: abs(t[1]))
    print(f"Best result: {best_result}")
    copy_ind_1[parameter].set(best_result[0])

    return copy_ind_1

def search_parameter_optimum(individual: BaseIndividual, data_target: Data, parameter):
    low = parameter.lower_bound
    up = parameter.upper_bound



def tune_strategy1(individual: BaseIndividual, data_target: Data, epsilon, rounds=10):
    p = Population()
    p.set_target(data_target)
    p.append(individual)
    p.fitness_for_all_individuals()

    param_name_list = ["asc_bike_mu", "asc_car_d_mu", "asc_car_p_mu", "asc_ped_mu", "asc_put_mu"]
    flag = True
    for i in range(rounds):
        diff = individual.data._get_modal_split() - data_target._get_modal_split()
        if flag:
            individual = tune(individual, data_target, individual[param_name_list[diff.idxmin()["count"]]], population=p, epsilon=epsilon)

        else:
            individual = tune(individual, data_target, individual[param_name_list[diff.idxmax()["count"]]], population=p, epsilon=epsilon)
        flag = not flag

    p.draw_boundaries_modal_split(sort=False)
    print(p.logger.print_csv())
    return individual, p.best()


def tune_strategy2(individual: BaseIndividual, data_target: Data):
    p = Population()
    p.set_target(data_target)
    p.append(individual)
    p.fitness_for_all_individuals()

    param_name_list = ["b_tt_bike_mu", "b_tt_car_d_mu", "b_tt_car_p_mu", "b_tt_ped", "b_tt_put_mu"]

    for i in range(10):
        parameter = individual[param_name_list[i % 5]]
        individual = tune(individual, data_target, parameter, population=p, draw=True)

        p.draw_all_traveltime(parameter.requirements["tripMode"])

    return individual, p.best()
