from pathlib import Path

import numpy
from sklearn.neural_network import MLPRegressor
import sklearn

import experiment_manager
import mobitopp_execution as simulation
from configurations import SPECS


def make_neural_numpy_array(neural_data):
    data_list = list(neural_data[0].values)
    assert len(data_list) == 5
    for item in neural_data[1]:
        for element in item[1]:
            data_list.append(element)

    for item in neural_data[2]:
        for element in item[1]:
            data_list.append(element)
    return numpy.asarray(data_list)


def set_config_from_output(config, data):
    for item in enumerate(config.entries):
        config.entries.values[item] = data[item]
    config.write()
    print(config.entries)


def data_extraction(path, config_number):
    data_list = []
    neural_data_list = []
    neural_expected_output_list = []
    for file in path.iterdir():
        print(file)
        yaml, data = simulation.load(str(file) + "/")
        # print(yaml.configs[-1])
        data_list.append(data)
        tempdata = data.get_neural_training_data()
        neural_data_list.append(make_neural_numpy_array(tempdata))
        conf = yaml.configs[4]
        neural_expected_output_list.append(numpy.asarray(
            [conf.entries[key] for key in conf.get_main_parameters()]
        ))
        #data.draw_distributions()
    return data_list, neural_data_list, neural_expected_output_list


def data_comparison(path):
    data_list = []
    for file in path.iterdir():
        yaml, data = simulation.load(str(file) + "/")
        data_list.append(data)
        data.draw_distributions()
    return data_list


def main():
    path = SPECS.EXP_PATH + "neural_network_random_data/"
    # All the experiments for neural networking
    ex_list_mode = ['neural_network_mode_choice-b_only_one_zero',
                    'neural_network_only_change_main_params',
                    'neural_network_only_change_main_params_better_beta_params',
                    'neural_network_only_change_main_params_no_sig_better_beta']

    ex_list_dest = ['neural_network_dest_data_version2']
    for ex in ex_list_mode:
        a, b, c = data_extraction(Path(SPECS.EXP_PATH + ex), 5)  # mode has config number 5
        numpy.save(Path(SPECS.NUMPY + ex + "_input_data"), b)
        numpy.save(Path(SPECS.NUMPY + ex + "_expected_data"), c)
        #a = data_comparison(Path(SPECS.EXP_PATH + ex))
        #res = [x == y for x in a for y in a]
    return


if __name__ == "__main__":
    main()
