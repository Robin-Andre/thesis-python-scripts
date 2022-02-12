import unittest
from pathlib import Path

import numpy


import calibration.neural_network_data_generator
from configurations import SPECS
import mobitopp_execution as simulation

class MyTestCase(unittest.TestCase):

    #"Excessive Runtime! this test is for refactoring purposes only"
    def refactortest_something(self):
        experiment = 'neural_network_mode_choice-b_only_one_zero'
        expected_input_data = numpy.load(SPECS.NUMPY + experiment +"_input_data.npy")
        expected_output_data = numpy.load(SPECS.NUMPY + experiment +"_expected_data.npy")

        path = Path(SPECS.EXP_PATH + experiment)
        #yaml_list, data_list = zip(*[simulation.load(file) for file in path.iterdir() if file.name.endswith("00")])
        yaml_list, data_list = zip(*[simulation.load(file) for file in path.iterdir()])
        inp, exp = calibration.neural_network_data_generator.convert_mode(yaml_list, data_list)
        numpy.save(Path(SPECS.NUMPY + experiment + "result_input_data"), inp)
        numpy.save(Path(SPECS.NUMPY + experiment + "result_expected_data"), exp)
        self.assertTrue(numpy.array_equal(expected_input_data, inp))
        self.assertTrue(numpy.array_equal(expected_output_data, exp))

    def test_something_else(self):
        yaml_list, data_list = zip(*[simulation.load("resources/example_config_load"),
                                     simulation.load("resources/example_config_load2")])
        inp, exp = calibration.neural_network_data_generator.convert_dest(yaml_list, data_list)
        dc = yaml_list[0].destination_config()
        expected_params = dc.get_main_parameters_name_only()
        expected_values = [values for key, values in dc.parameters.items() if key in expected_params]
        self.assertEqual(list(exp[0]), expected_values)








if __name__ == '__main__':
    unittest.main()
