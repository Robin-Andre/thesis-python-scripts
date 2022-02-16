from calibration.evolutionary.population import Population


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


def tune(individual, data_target, parameter, epsilon=0.05, population=None, draw=False):

    print(f"Original Value {individual[parameter].value}")
    error = parameter.error(individual, data_target)
    if error < epsilon:
        print("Error too small. No optimization will be done")
        return individual
    print(f"Error{error}")
    copy_ind_1 = individual.copy()
    copy_ind_2 = individual.copy()
    estimate_value = parameter.observe(individual, data_target)
    copy_ind_1[parameter].set(estimate_value)
    __do_population_shenanigans(copy_ind_1, population, draw, mode=parameter.requirements["tripMode"])
    #copy_ind_1.run()

    error = parameter.error(copy_ind_1, data_target)
    print(f"Error{error}")
    while error > epsilon:

        estimate_value = parameter.observe_detailed(copy_ind_2, copy_ind_1, data_target)
        copy_ind_2 = copy_ind_1.copy()
        copy_ind_1[parameter].set(estimate_value)
        print(copy_ind_1[parameter])
        print(copy_ind_2[parameter])
        __do_population_shenanigans(copy_ind_1, population, draw, mode=parameter.requirements["tripMode"])

        error = parameter.error(copy_ind_1, data_target)
        print(f"Error{error}")

    return copy_ind_1


def tune_strategy1(individual, data_target, epsilon):
    p = Population()
    p.set_target(data_target)
    p.append(individual)
    p.fitness_for_all_individuals()

    param_name_list = ["asc_bike_mu", "asc_car_d_mu", "asc_car_p_mu", "asc_ped_mu", "asc_put_mu"]
    flag = True
    for i in range(10):
        diff = individual.data.get_modal_split() - data_target.get_modal_split()
        #print(diff)
        #print(diff.idxmin())
        #print(diff.idxmax())

        if flag:
            #print(param_name_list[diff.idxmin()["count"]])
            individual = tune(individual, data_target, individual[param_name_list[diff.idxmin()["count"]]], population=p, epsilon=epsilon)

        else:
            #print(param_name_list[diff.idxmax()["count"]])
            individual = tune(individual, data_target, individual[param_name_list[diff.idxmax()["count"]]], population=p, epsilon=epsilon)
        flag = not flag

    p.draw_boundaries_modal_split(sort=False)
    print(p.logger.print_csv())
    return individual, p.best()


def tune_strategy2(individual, data_target):
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
