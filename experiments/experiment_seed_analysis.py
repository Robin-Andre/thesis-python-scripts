import mobitopp_execution as simulation
from configurations import SPECS

if __name__ == '__main__':
    exp_path = SPECS.EXP_PATH + "same_config_different_seed/"
    simulation.reset()

    for i in range(1, 11):

        simulation.reset()
        yaml = simulation.default_yaml()

        yaml.set_fraction_of_population(0.1)
        yaml.set_seed(i)

        _, data = simulation.run_mobitopp(yaml)
        simulation.save(yaml, data, exp_path + "seed" + str(i))

