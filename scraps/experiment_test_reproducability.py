import mobitopp_execution as simulation
from configurations import SPECS

if __name__ == '__main__':
    simulation.restore_experimental_configs()
    yaml = simulation.default_yaml()
    yaml.set_fraction_of_population(0.1)
    yaml.write()

    simulation.clean_result_directory()

    exp_path = SPECS.EXP_PATH + "reproducible_example/"
    mode_config = yaml.mode_config()
    dest_config = yaml.destination_config()
    data_list = []

    simulation.reset()
    _, data = simulation.run_mobitopp(yaml)
    simulation.save(yaml, data, exp_path + "iteration1")

    simulation.reset()

    _, data2 = simulation.run_mobitopp(yaml)

    simulation.save(yaml, data2, exp_path + "iteration2")



