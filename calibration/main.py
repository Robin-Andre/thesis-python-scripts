from pathlib import Path
from calibration import pygad_genetic_algorithm, stochastic_perturbation_algorithm, pyswarms_algorithm, my_algorithm
from calibration.evolutionary.individual import Individual, DestinationIndividual
from configurations import SPECS
import random
import mobitopp_execution as simulation


def write(result, experiment, folder):
    with open(SPECS.EXP_PATH + folder + f"/{experiment}.csv", "w+") as file:
        file.write(result)


def build_folders(folder):
    folder_path = Path(SPECS.EXP_PATH + folder)
    csv_path = Path(SPECS.EXP_PATH + folder + "/csv")
    data_path = Path(SPECS.EXP_PATH + folder + "/data")
    for x in [folder_path, csv_path, data_path]:
        if not x.exists():
            print(f"{x} does not exist:...creating")
            x.mkdir()



def _help_launcher(param_list, seed, exname, descriptor, metric, individual_seed, d, algorithm, ind_constructor=Individual):
    build_folders(exname)
    if d is None:
        d = ind_constructor(seed=individual_seed, param_list=param_list)
        d.run()
    data = d.data
    p, result = algorithm(param_list, data, metric, seed, experiment_name=exname, descriptor=descriptor, individual_constructor=ind_constructor)
    write_helper(result, seed, exname, descriptor)

def launch_pygad(param_list, seed, exname="genetic_Unnamed", descriptor=None, metric="ModalSplit_Default_Splits_sum_squared_error", individual_seed=-1, d=None, individual_constructor=Individual):
    algorithm = pygad_genetic_algorithm.tune
    _help_launcher(param_list, seed, exname, descriptor, metric, individual_seed, d, algorithm=algorithm, ind_constructor=individual_constructor)



def launch_spsa(param_list, seed, exname="spsa_Unnamed", descriptor=None, metric="ModalSplit_Default_Splits_sum_squared_error", individual_seed=-1, d=None, individual_constructor=Individual):
    algorithm = stochastic_perturbation_algorithm.tune
    _help_launcher(param_list, seed, exname, descriptor, metric, individual_seed, d, algorithm=algorithm, ind_constructor=individual_constructor)



def launch_pyswarms(param_list, seed, exname="pyswarms_Unnamed", descriptor=None, metric="ModalSplit_Default_Splits_sum_squared_error", individual_seed=-1, d=None, individual_constructor=Individual):
    algorithm = pyswarms_algorithm.tune
    _help_launcher(param_list, seed, exname, descriptor, metric, individual_seed, d, algorithm=algorithm, ind_constructor=individual_constructor)


def launch_pygad_destination(param_list, seed, exname="genetic_Unnamed_destination", descriptor=None, metric="TravelDistance_Default_sum_squared_error", individual_seed=-1, d=None):
    launch_pygad(param_list, seed, exname, descriptor, metric, individual_seed, d, individual_constructor=DestinationIndividual)


def launch_spsa_destination(param_list, seed, exname="spsa_Unnamed_destination", descriptor=None, metric="TravelDistance_Default_sum_squared_error", individual_seed=-1, d=None):
    launch_spsa(param_list, seed, exname, descriptor, metric, individual_seed, d, individual_constructor=DestinationIndividual)


def launch_pyswarms_destination(param_list, seed, exname="pyswarms_Unnamed_destination", descriptor=None, metric="TravelDistance_Default_sum_squared_error", individual_seed=-1, d=None):
    launch_pyswarms(param_list, seed, exname, descriptor, metric, individual_seed, d, individual_constructor=DestinationIndividual)


def launch_my_algorithm(param_list, seed, exname="myalgorithm_Unnamed", descriptor=None, individual_seed=-1, d=None):
    random.seed(seed)
    build_folders(exname)
    if d is None:
        d = Individual(seed=individual_seed, param_list=param_list)
        d.run()
    data = d.data
    pop, result = my_algorithm.tune(param_list, data, "ModalSplit_Default_Splits_sum_squared_error")
    pop_save_helper(pop, seed, exname, descriptor)
    print(pop.best())
    write_helper(result, seed, exname, descriptor)


def launch_my_algorithm_new(param_list, seed, exname="myalgorithm_Unnamed", descriptor=None, individual_seed=-1, d=None):
    random.seed(seed)
    build_folders(exname)
    if d is None:
        d = Individual(seed=individual_seed, param_list=param_list)
        d.run()
    data = d.data
    pop, result = my_algorithm.tune_new(param_list, data, "ModalSplit_Default_Splits_sum_squared_error")
    pop_save_helper(pop, seed, exname, descriptor)
    print(pop.best())
    write_helper(result, seed, exname, descriptor)




def launch_my_other_algorithm(param_list, seed, exname="myalgorithm_Unnamed", descriptor=None, individual_seed=-1, d=None):
    random.seed(seed)
    build_folders(exname)
    if d is None:
        d = Individual(seed=individual_seed, param_list=param_list)
        d.run()
    data = d.data
    pop, result = my_algorithm.temp2tune(param_list, data, "ModalSplit_Default_Splits_sum_squared_error")
    pop_save_helper(pop, seed, exname, descriptor)
    print(pop.best())
    write_helper(result, seed, exname, descriptor)

def pop_save_helper(pop, seed, exname, descriptor):
    if descriptor is None:
        pop.save(SPECS.EXP_PATH + exname + "/data/seed" + str(seed) + "/")
    else:
        pop.save(SPECS.EXP_PATH + exname + "/data/" + descriptor + "/")


def write_helper(result, seed, exname, descriptor):
    if descriptor is None:
        write(result, "seed" + str(seed), exname)
    else:
        write(result, descriptor, exname)


def experiment_spsa_target_has_same_seed(params):
    for i in range(101, 106):
        launch_spsa(params, i, "spsa_10_parameters_target_has_same_seed")


def experiment_pygad_target_has_same_seed(params):
    for i in range(106, 111):
        launch_pygad(params, i, "pygad_10_parameters_target_has_same_seed")

def experiment_pygad_target_has_same_seed_time_metric(params):
    for i in range(106, 111):
        launch_pygad(params, i, "pygad_10_parameters_target_has_same_seed_time_metric", metric="TravelTime_Default_sum_squared_error")

def experiment_pyswarms_target_has_same_seed(params):
    for i in range(106, 111):
        launch_pyswarms(params, i, "pyswarms_10_parameters_target_has_same_seed")

def experiment_pyswarms_target_has_same_seed_time_metric(params):
    for i in range(106, 111):
        launch_pyswarms(params, i, "pyswarms_10_parameters_target_has_same_seed_time_metric", metric="TravelTime_Default_sum_squared_error")


def experiment_random_target_individual(params):

    for seed in [43, 45, 47]:

        random.seed(seed)
        target = Individual(seed=seed, param_list=params)
        target.randomize_active_parameters()

        target.run()

        exp_name = "random_target_10_parameters_time_metric"
        build_folders(exp_name)
        target.save(SPECS.EXP_PATH + exp_name + "/data/target/" + str(seed))

        #launch_pygad(params, seed, exp_name, descriptor="pygad_seed" + str(seed), d=target, metric="TravelTime_Default_sum_squared_error")
        #launch_pyswarms(params, seed, exp_name, descriptor="pyswarms_seed" + str(seed), d=target, metric="TravelTime_Default_sum_squared_error")
        #launch_spsa(params, seed, exp_name, descriptor="spsa_seed" + str(seed), d=target, metric="TravelTime_Default_sum_squared_error")
        launch_my_algorithm(params, seed, exp_name, descriptor="myalgorithm_seed" + str(seed), d=target)


def further_Exp(params):
    for seed in [48, 49, 50]:

        random.seed(seed)
        target = Individual(seed=seed, param_list=params)
        target.randomize_active_parameters()
        target.run()

        exp_name = "random_target_10_parameters_time_metric"
        build_folders(exp_name)
        target.save(SPECS.EXP_PATH + exp_name + "/data/target/")

        launch_pygad(params, seed, exp_name, descriptor="pygad_seed" + str(seed), d=target, metric="TravelTime_Default_sum_squared_error")
        launch_pyswarms(params, seed, exp_name, descriptor="pyswarms_seed" + str(seed), d=target, metric="TravelTime_Default_sum_squared_error")
        launch_spsa(params, seed, exp_name, descriptor="spsa_seed" + str(seed), d=target, metric="TravelTime_Default_sum_squared_error")
        launch_my_algorithm(params, seed, exp_name, descriptor="myalgorithm_seed" + str(seed), d=target)

if __name__ == "__main__":
    #PARAMS = ["asc_car_d_mu", "age_0_17_on_b_tt_ped"]
    PARAMS = ["asc_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "asc_bike_mu", "b_tt_car_p_mu", "b_tt_car_d_mu", "b_tt_put_mu", "b_tt_bike_mu", "b_tt_ped"]
    yaml = simulation.default_yaml()
    print(yaml.mode_config().get_all_parameter_names_on_requirements(["tripMode", "age", "gender"]))

    print(yaml.destination_config().get_all_parameter_names_on_requirements(["age", "gender"]))
    #exit(0)
    PARAMS = ["asc_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "asc_bike_mu", "b_tt_car_p_mu", "b_tt_car_d_mu", "b_tt_put_mu", "b_tt_bike_mu", "b_tt_ped", "female_on_asc_ped", "age_18_29_on_b_tt_car_d"]
    #experiment_pyswarms_target_has_same_seed(PARAMS)
    #experiment_pyswarms_target_has_same_seed_time_metric(PARAMS)
    launch_pyswarms(PARAMS, 52, "Detailed_test", descriptor="pyswarms_seed_detailedtest", metric="TravelTime_Default_sum_squared_error")


#experiment_pygad_target_has_same_seed_time_metric(PARAMS)
    #experiment_pygad_target_has_same_seed(PARAMS)
    exit(0)
#experiment_random_target_individual(PARAMS)
    #further_Exp(PARAMS)
    #exit(0)

    launch_my_algorithm_new(PARAMS, 2, "myalgo_10_parameters", descriptor="Diffseed2_2iters")
    #launch_my_algorithm(PARAMS, 3, "myalgo_10_parameters", descriptor="Diffseed3_2Iters")
    exit(0)

    launch_pyswarms(PARAMS, 103, "pyswarms")
    launch_pyswarms(PARAMS, 103, "pyswarms", descriptor="TEST")
    exit(0)

    launch_spsa(PARAMS, 102, "TE")
    exit(0)
    ex_name = "pygad_10_parameters"
    launch_pygad(PARAMS, 101, ex_name)
    launch_pygad(PARAMS, 102, ex_name)
    launch_pygad(PARAMS, 103, ex_name)
    #experiment_pyswarms_target_has_same_seed(PARAMS)
    #experiment_spsa_target_has_same_seed(PARAMS)


