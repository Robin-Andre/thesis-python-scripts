# This experiment tries to analyze which config has the most impact by setting all other configs to the default values 0
from utils import utils
from configurations import configloader
import evaluation
import yamlloader
import mobitopp_execution as simulation



def set_all_configs_to_zero(config_list_internal, cwd_internal):
    for config_internal in config_list_internal:
        text_internal = utils.extract_values_of_iteration(config_internal, 0)
        configloader.write_config_file(text_internal, cwd_internal + config_internal.path)


if __name__ == '__main__':
    simulation.restore_experimental_configs()
    cwd = "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/"
    csv_path = cwd + "output/results/calibration/throwaway/demandsimulationResult.csv"
    yaml_file = "config/rastatt/short-term-module-100p.yaml"
    yaml = yamlloader.YAML(cwd, yaml_file)
    config_list = yaml.find_configs(cwd)
    for config in config_list:
        for i in range(6):
            simulation.restore_experimental_configs()
            set_all_configs_to_zero(config_list, cwd)
            text = utils.extract_values_of_iteration(config, i)
            configloader.write_config_file(text, cwd + config.path)
            print("Running config[" + config.name + "] number: " + str(i))
            simulation.run_experiment()
            evaluation.save_compressed_output(config.name + "iteration" + str(i),
                                          "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/output/results"
                                          "/calibration/throwaway/demandsimulationResult.csv",
                                          "/home/paincrash/Desktop/master-thesis/experiment_results_permanent"
                                          "/experiment6/",
                                          "")
