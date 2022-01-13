from pathlib import Path

import numpy
from sklearn.neural_network import MLPRegressor
import sklearn
import calibration.neural_network_data_generator
import experiment_manager
import mobitopp_execution as simulation
from configurations import SPECS


def data_extraction(path, dest_config):
    data_list = []
    neural_data_list = []
    neural_expected_output_list = []
    for file in path.iterdir():

        yaml, data = simulation.load(str(file) + "/")
        data_list.append(data)
        temp_data = calibration.get_neural_training_data(data)

        neural_data_list.append(temp_data)
        if dest_config:
            conf = yaml.destination_config()
        else:
            conf = yaml.mode_config()
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

def neural_start(input, expected):
    numpy.nan_to_num(input, copy=False)
    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(input, expected, random_state=1)
    regr = MLPRegressor(random_state=1, max_iter=5000, verbose=10, activation="logistic", hidden_layer_sizes=(100,)).fit(X_train, y_train)

    temp = regr.predict(X_test[0:1])
    temp_target = y_test[0:1]
    print(temp)
    print(temp_target)
    print(regr.score(X_test, y_test))


def main():

    #create_numpy_data_mode()
    temp = []
    for file in Path(SPECS.NUMPY).iterdir():

        x = numpy.load(file)

        temp.append((file, x))

    xl = [0, 2, 4, 6, 8]
    for x in xl:
        assert x % 2 == 0
        print(temp[x][0])
        neural_start(numpy.vstack(temp[x + 1][1]), numpy.vstack(temp[x][1]))
    return


def create_numpy_data_mode():
    ex_list_mode = ['neural_network_mode_choice-b_only_one_zero',
                    'neural_network_only_change_main_params',
                    'neural_network_only_change_main_params_better_beta_params',
                    'neural_network_only_change_main_params_no_sig_better_beta']
    for ex in ex_list_mode:
        extract(ex, False)


def create_numpy_data_dest():
    ex_list_dest = ['neural_network_dest_data_version2']
    for ex in ex_list_dest:
        extract(ex, True)  # destination has config number 4


def extract(ex, num):

    a, b, c = data_extraction(Path(SPECS.EXP_PATH + ex), num)
    numpy.save(Path(SPECS.NUMPY + ex + "_input_data"), b)
    numpy.save(Path(SPECS.NUMPY + ex + "_expected_data"), c)


if __name__ == "__main__":
    main()
