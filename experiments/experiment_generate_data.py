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
    config.entries[key] = value
    config.write()
    data = simulation.run_experiment(key + str(value))
    exp_path = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/neural_network_data_modechoice/"
    yaml = simulation.default_yaml()
    if data is not None:
        data.draw()
        simulation.save(yaml, data, exp_path + key + str(value) + "/")


if __name__ == '__main__':
    simulation.restore_experimental_configs()
    yaml = simulation.default_yaml()
    yaml.set_fraction_of_population(0.1)
    yaml.write()
    configs = yaml.configs
    for config in configs:
        set_config_to_one(config)
    data = simulation.run_experiment()
    data.draw()
    exp_path = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/neural_network_data/"
    simulation.save(yaml, data, exp_path + "baseline/")
    dest_config = configs[-1]  # 0 for destination choice, -1 for mode choice
    print(dest_config.name)
    #test_val = 100
    test_vals = [10, 50]
    for test_val in test_vals:
        for key in dest_config.entries:
            run_singular_value_experiment(key, test_val, dest_config)
            run_singular_value_experiment(key, -test_val, dest_config)



