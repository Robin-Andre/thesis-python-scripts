from pathlib import Path
from calibration import pygad_genetic_algorithm, stochastic_perturbation_algorithm, pyswarms_algorithm, my_algorithm
from calibration.evolutionary.individual import Individual
from configurations import SPECS
import random


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



def launch_pygad(param_list, seed, exname="genetic_Unnamed", descriptor=None):
    build_folders(exname)
    d = Individual(param_list=param_list)
    d.run()
    data = d.data
    p, result = pygad_genetic_algorithm.tune(param_list, data, "ModalSplit_Default_Splits_sum_squared_error", seed, experiment_name=exname, descriptor=descriptor)
    write_helper(result, seed, exname, descriptor)

def launch_spsa(param_list, seed, exname="spsa_Unnamed", descriptor=None):
    build_folders(exname)
    d = Individual(param_list=param_list)
    d.run()
    data = d.data
    p, result = stochastic_perturbation_algorithm.tune(param_list, data, "ModalSplit_Default_Splits_sum_squared_error", seed, experiment_name=exname, descriptor=descriptor)
    write_helper(result, seed, exname, descriptor)

def launch_pyswarms(param_list, seed, exname="pyswarms_Unnamed", descriptor=None):
    build_folders(exname)
    d = Individual(param_list=param_list)
    d.run()
    data = d.data
    p, result = pyswarms_algorithm.tune(param_list, data, "ModalSplit_Default_Splits_sum_squared_error", seed, experiment_name=exname, descriptor=descriptor)
    write_helper(result, seed, exname, descriptor)

def launch_my_algorithm(param_list, seed, exname="myalgorithm_Unnamed", descriptor=None):
    random.seed(seed)
    build_folders(exname)
    d = Individual(seed=seed, param_list=param_list)
    d.run()
    data = d.data
    pop, result = my_algorithm.tune(param_list, data, "ModalSplit_Default_Splits_sum_squared_error")
    pop_save_helper(pop, seed, exname, descriptor)
    print(pop.best())
    write_helper(result, seed, exname, descriptor)

def launch_my_other_algorithm(param_list, seed, exname="myalgorithm_Unnamed", descriptor=None):
    random.seed(seed)
    build_folders(exname)
    d = Individual(seed=seed, param_list=param_list)
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
    for i in range(101, 106):
        launch_pygad(params, i, "pygad_10_parameters_target_has_same_seed")

def experiment_pyswarms_target_has_same_seed(params):
    for i in range(101, 106):
        launch_pyswarms(params, i, "pyswarms_10_parameters_target_has_same_seed")

if __name__ == "__main__":
    #PARAMS = ["asc_car_d_mu", "age_0_17_on_b_tt_ped"]
    PARAMS = ["asc_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "asc_bike_mu", "b_tt_car_p_mu", "b_tt_car_d_mu", "b_tt_put_mu", "b_tt_bike_mu", "b_tt_ped"]
    experiment_pygad_target_has_same_seed(PARAMS)
    exit(0)

    launch_my_algorithm(PARAMS, 2, "myalgo_10_parameters", descriptor="Diffseed2_2iters")
    launch_my_algorithm(PARAMS, 3, "myalgo_10_parameters", descriptor="Diffseed3_2Iters")
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


