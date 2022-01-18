from pathlib import Path

import numpy
from sklearn.neural_network import MLPRegressor
import sklearn
import calibration.neural_network_data_generator
import mobitopp_execution as simulation
from configurations import SPECS




def main():
    path = Path(SPECS.EXP_PATH + "neural_network_random_data")

    data_list, neural_data_list, neural_expected_output_list = data_extraction(path)

    full_data = numpy.vstack(neural_data_list)
    full_expected_data = numpy.vstack(neural_expected_output_list)
    res = [x == y for x in data_list for y in data_list]

    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(full_data, full_expected_data, random_state=1)
    regr = MLPRegressor(random_state=1, max_iter=500, verbose=10).fit(X_train, y_train)

    for test in X_test:
        result = regr.predict(test)
        simulation.restore_experimental_configs()
        simulation.clean_result_directory()
        # TODO plot the simulation data,
        data = simulation.run_experiment()
        data.draw_distributions()
        #simulation.save(yaml, data, exp_path + "iteration" + str(i) + "/")


    temp = regr.predict(X_test)

    print(regr.score(X_test, y_test))


def data_extraction(path):
    data_list = []
    neural_data_list = []
    neural_expected_output_list = []
    for file in path.iterdir():
        print(file)
        yaml, data = simulation.load(str(file) + "/")
        # print(yaml.configs[-1])
        data_list.append(data)
        tempdata = calibration.get_neural_training_data(data)
        neural_data_list.append(tempdata)
        conf = yaml.destination_config()
        neural_expected_output_list.append(numpy.asarray(list(conf.parameters.values())))
        data.draw_distributions()
    return data_list, neural_data_list, neural_expected_output_list


if __name__ == "__main__":
    main()
