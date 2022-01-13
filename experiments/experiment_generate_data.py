import random

import mobitopp_execution as simulation
from configurations import SPECS


def set_config_to_one(config_internal):
    for key in config_internal.entries:

        if config_internal.entries[key] < 2000:
            config_internal.entries[key] = 0
        else:
            print(f"Not touching: {key} in {config_internal.name}")

    config_internal.write()


def run_singular_value_experiment(key, value, config):
    print(f"Running Experiment: {key}: {value}")
    set_config_to_one(config)
    config.entries[key] = value
    config.write()
    simulation.clean_result_directory()
    data = simulation.run_experiment(key + str(value))
    exp_path = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/neural_network_close_data/"
    yaml = simulation.default_yaml()
    if data is not None:
        # data.draw()
        simulation.save(yaml, data, exp_path + key + str(value) + "/")
    else:
        print(f"Experiment failed: {key}, {value}")


if __name__ == '__main__':
    simulation.restore_experimental_configs()
    yaml = simulation.default_yaml()
    yaml.set_fraction_of_population(0.1)
    yaml.write()
    configs = yaml.configs

    simulation.clean_result_directory()
    data = simulation.run_experiment(yaml, "Baseline")
    simulation.save(yaml, data, SPECS.EXP_PATH + "/baseline")


    mode_config = yaml.mode_config()  # 0 for destination choice, -1 for mode choice
    dest_config = yaml.destination_config()
    data_list = []
    parameter_list_mode = ["asc_car_d_mu",
                           "asc_car_d_sig",
                           "asc_car_p_mu",
                           "asc_car_p_sig",
                           "asc_put_mu",
                           "asc_put_sig",
                           "asc_ped_mu",
                           "asc_ped_sig",
                           "asc_bike_mu",
                           "asc_bike_sig"]

    parameter_list_destination = ["asc_car_d",
                                  "asc_car_p",
                                  "asc_put",
                                  "asc_ped",
                                  "asc_bike",

                                  "b_tt_car_d",
                                  "b_tt_car_p",
                                  "b_tt_put",
                                  "b_tt_ped",
                                  "b_tt_bike"]

    #exp_path = SPECS.EXP_PATH + "/change_only_one_parameter_destination/"
    # for parameter in parameter_list_destination:
    #    for i in range(0, 51):
    #        simulation.restore_experimental_configs()
    #        simulation.clean_result_directory()
    #        dest_config.reset()
    #        if parameter.__contains__("b_tt_"):
    #            # dest_config.entries[parameter] = random.uniform(-1, 0)
    #            dest_config.entries[parameter] = (i - 50) / 50
    #        else:
    #            # dest_config.entries[parameter] = random.uniform(-25, 25)
    #            dest_config.entries[parameter] = i - 25
    #        dest_config.write()
    #        data = simulation.run_experiment(yaml, parameter + ":iteration" + str(i))
    #        simulation.save(yaml, data, exp_path + parameter + "/iteration" + str(i).zfill(4) + "/")

    exp_path = SPECS.EXP_PATH + "/change_only_one_parameter_mode/"

    parameter_list_mode = [("asc_car_d_mu", -10, 10),
                           ("asc_car_d_sig", -10, 10),
                           ("asc_car_p_mu", -10, 10),
                           ("asc_car_p_sig", -10, 10),
                           ("asc_put_mu", -10, 10),
                           ("asc_put_sig", -10, 10),
                           ("asc_ped_mu", -10, 10),
                           ("asc_ped_sig", -10, 10),
                           ("asc_bike_mu", -10, 10),
                           ("asc_bike_sig", -10, 10),

                           ("b_tt_car_p_mu", -5, 0),
                           ("b_tt_car_p_sig", -1, 1),
                           ("b_tt_car_d_mu", -5, 0),
                           ("b_tt_car_d_sig", -1, 1),
                           ("b_tt_put_mu", -5, 0),
                           ("b_tt_put_sig", -1, 1),
                           ("b_tt_bike_mu", -5, 0),
                           ("b_tt_bike_sig", -1, 1),
                           ("b_tt_ped", -5, 0),
                           ("b_cost", -1, 0),
                           ("b_cost_put", -1, 0),
                           ("b_u_put", -1, 0),
                           ("b_logsum_acc_put", -5, 0),
                           ("elasticity_acc_put", -1, 1),
                           ("b_park_car_d", -5, 0),
                           ("elasticity_parken", -1, 1)]

    for parameter, a, b in parameter_list_mode:
        for i in range(0, 51):
            simulation.restore_experimental_configs()
            simulation.clean_result_directory()
            mode_config.reset()
            mode_config.entries[parameter] = (i / 50) * (b - a) + a
            print(f"The current value is: {(i / 50) * (b - a) + a}")
            mode_config.write()
            # dest_config.randomize_main_parameters()
            # dest_config.write()
            data = simulation.run_experiment(yaml, parameter + ":iteration" + str(i))
            simulation.save(yaml, data, exp_path + parameter + "/iteration" + str(i).zfill(4) + "/")

    # test_val = 100
    # test_values = [10, 50, 100]
    # for test_val in test_values:
    #    for key in dest_config.entries:
    #        run_singular_value_experiment(key, test_val, dest_config)
    #        run_singular_value_experiment(key, -test_val, dest_config)
