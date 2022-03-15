from calibration import pygad_genetic_algorithm
from calibration.evolutionary.individual import Individual


def launch_pygad(param_list, seed, exname):
    d = Individual(param_list=param_list)
    d.run()
    data = d.data
    pygad_genetic_algorithm.tune(param_list, data, "ModalSplit_Default_Splits_sum_squared_error", seed, experiment_name=exname)


if __name__ == "__main__":
    PARAMS = ["asc_car_d_mu", "asc_car_p_mu"]
    PARAMS = ["asc_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "asc_bike_mu", "b_tt_car_p_mu", "b_tt_car_d_mu", "b_tt_put_mu", "b_tt_bike_mu", "b_tt_ped"]
    ex_name = "pygad_10_parameters"
    launch_pygad(PARAMS, 101, ex_name)
    launch_pygad(PARAMS, 102, ex_name)
    launch_pygad(PARAMS, 103, ex_name)
