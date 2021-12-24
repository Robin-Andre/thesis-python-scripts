from pathlib import Path

import numpy
from sklearn.neural_network import MLPRegressor
import sklearn

import mobitopp_execution as simulation


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


def main():
    path = Path("C:/Users/Admin/Desktop/master-thesis/neural_network_data/neural_network_random_data")
    data_list = []
    neural_data_list = []
    neural_expected_output_list = []
    for file in path.iterdir():
        print(file)
        yaml, data = simulation.load(str(file) + "/")
        #print(yaml.configs[-1])
        data_list.append(data)
        tempdata = data.get_neural_training_data()
        neural_data_list.append(make_neural_numpy_array(tempdata))
        conf = yaml.configs[-1]
        neural_expected_output_list.append(numpy.asarray(list(conf.entries.values())))
        data.draw_distributions()

    full_data = numpy.vstack(neural_data_list)
    full_expected_data = numpy.vstack(neural_expected_output_list)
    res = [x == y for x in data_list for y in data_list]

    X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(full_data, full_expected_data, random_state=1)
    regr = MLPRegressor(random_state=1, max_iter=15000, verbose=10).fit(X_train, y_train)
    temp = regr.predict(X_test)

    print(regr.score(X_test, y_test))

if __name__ == "__main__":
    main()
