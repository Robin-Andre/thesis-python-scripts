import numpy

import configurations.configloader


def convert_mode(yaml_list, data_list):
    return neural_data_method(yaml_list, data_list, get_neural_training_data, get_main_parameter_mode)


def convert_dest(yaml_list, data_list):
    return neural_data_method(yaml_list, data_list, get_neural_training_data, get_main_parameter_destination)


def get_main_parameter_mode(yaml):
    return __helper(yaml.configs[5], configurations.configloader.ModeChoiceConfig)


def get_main_parameter_destination(yaml):
    return __helper(yaml.configs[4], configurations.configloader.DestinationChoiceConfig)


def __helper(config, expected_class):
    assert type(config) == expected_class
    return numpy.asarray([config.entries[key] for key in config.get_main_parameters()])


def neural_data_method(yaml_list, data_list, extract_input_data_method, extract_config_data_method):
    np_input = []
    np_expected = []
    for yaml, data in zip(yaml_list, data_list):
        np_input.append(extract_input_data_method(data))
        np_expected.append(extract_config_data_method(yaml))
    return numpy.vstack(np_input), numpy.vstack(np_expected)


def get_neural_training_data(data):
    test = data.get_modal_split()
    approxis_time = data.travel_time.approximations()
    approxis_distance = data.travel_distance.approximations()
    return __make_neural_numpy_array([test["amount"], approxis_time, approxis_distance])


def __make_neural_numpy_array(neural_data):
    data_list = list(neural_data[0].values)
    assert len(data_list) == 5
    for item in neural_data[1]:
        for element in item[1]:
            data_list.append(element)

    for item in neural_data[2]:
        for element in item[1]:
            data_list.append(element)
    return numpy.asarray(data_list)
