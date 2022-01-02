from pathlib import Path

import pandas

import metric

import mobitopp_execution as simulation
import yamlloader


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

    exp_path = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/neural_network_mode_choice-b_only_one_zero/"
    mode_config = configs[-1]  # 0 for destination choice, -1 for mode choice
    dest_config = configs[0]
    data_list = []
    for i in range(0, 1000):
        simulation.restore_experimental_configs()
        simulation.clean_result_directory()
        mode_config.randomize_main_parameters()
        mode_config.write()
        #dest_config.randomize_main_parameters()
        #dest_config.write()
        data = simulation.run_experiment(str(i))
        simulation.save(yaml, data, exp_path + "iteration" + str(i) + "/")


    #test_val = 100
    #test_values = [10, 50, 100]
    #for test_val in test_values:
    #    for key in dest_config.entries:
    #        run_singular_value_experiment(key, test_val, dest_config)
    #        run_singular_value_experiment(key, -test_val, dest_config)



