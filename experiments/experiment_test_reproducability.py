from pathlib import Path

import pandas

import metric

import mobitopp_execution as simulation
import yamlloader
from configurations import SPECS

if __name__ == '__main__':
    simulation.restore_experimental_configs()
    yaml = simulation.default_yaml()
    yaml.set_fraction_of_population(0.1)
    yaml.write()
    configs = yaml.configs

    simulation.clean_result_directory()

    exp_path = SPECS.EXP_PATH + "reproducible_example/"
    mode_config = configs[-1]  # 0 for destination choice, -1 for mode choice
    dest_config = configs[0]
    data_list = []

    simulation.restore_experimental_configs()
    simulation.restore_default_yaml()
    simulation.clean_result_directory()

    _, data = simulation.run_mobitopp(yaml)
    simulation.save(yaml, data, exp_path + "iteration1")

    simulation.restore_experimental_configs()
    simulation.restore_default_yaml()
    simulation.clean_result_directory()

    _, data2 = simulation.run_mobitopp(yaml)

    simulation.save(yaml, data2, exp_path + "iteration2")



