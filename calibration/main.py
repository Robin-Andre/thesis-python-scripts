from calibration import pygad_genetic_algorithm, stochastic_perturbation_algorithm, pyswarms_algorithm, my_algorithm
from calibration.evolutionary.individual import Individual
from configurations import SPECS


def write(result, experiment, folder):
    with open(SPECS.EXP_PATH + folder + f"/{experiment}.csv", "w+") as file:
        file.write(result)


def launch_pygad(param_list, seed, exname, descriptor=None):
    d = Individual(param_list=param_list)
    d.run()
    data = d.data
    p, result = pygad_genetic_algorithm.tune(param_list, data, "ModalSplit_Default_Splits_sum_squared_error", seed, experiment_name=exname, descriptor=descriptor)
    write_helper(result, seed, exname, descriptor)

def launch_spsa(param_list, seed, exname, descriptor=None):
    d = Individual(param_list=param_list)
    d.run()
    data = d.data
    p, result = stochastic_perturbation_algorithm.tune(param_list, data, "ModalSplit_Default_Splits_sum_squared_error", seed, experiment_name=exname, descriptor=descriptor)
    write_helper(result, seed, exname, descriptor)

def launch_pyswarms(param_list, seed, exname, descriptor=None):
    d = Individual(param_list=param_list)
    d.run()
    data = d.data
    p, result = pyswarms_algorithm.tune(param_list, data, "ModalSplit_Default_Splits_sum_squared_error", seed, experiment_name=exname, descriptor=descriptor)
    write_helper(result, seed, exname, descriptor)

def launch_my_algorithm(param_list, seed, exname, descriptor=None):
    d = Individual(param_list=param_list)
    d.run()
    data = d.data
    my_algorithm.tune(param_list, data, "ModalSplit_Default_Splits_sum_squared_error")

def write_helper(result, seed, exname, descriptor):
    if descriptor is None:
        write(result, "seed" + str(seed), exname)
    else:
        write(result, descriptor, exname)

if __name__ == "__main__":
    PARAMS = ["asc_car_d_mu", "asc_car_p_mu"]
    PARAMS = ["asc_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "asc_bike_mu", "b_tt_car_p_mu", "b_tt_car_d_mu", "b_tt_put_mu", "b_tt_bike_mu", "b_tt_ped"]

    launch_my_algorithm(PARAMS, 2, "myalgo")
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
