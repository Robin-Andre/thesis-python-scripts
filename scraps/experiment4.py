# In this experiment I want to analyze whether an existing calibration step is feasible with the metrics currently
# extracted. For this reason I rerun the existing calibration steps documented in the mode choice and destination choice
# parameter files.
from utils import utils
from configurations import configloader
import evaluation
import yamlloader
import mobitopp_execution as simulation




if __name__ == '__main__':
    simulation.restore_experimental_configs()
    cwd = "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/"
    csv_path = cwd + "output/results/calibration/throwaway/demandsimulationResult.csv"
    yaml_file = "config/rastatt/short-term-module-100p.yaml"
    yaml = yamlloader.YAML(cwd, yaml_file)
    config_list = yaml.find_configs(cwd)
    for i in range(6):  # Five iterations should be sufficient
        for config in config_list:
            text = utils.extract_values_of_iteration(config, i)
            configloader.write_config_file(text, cwd + config.path)
        print("Running config number: " + str(i))
        simulation.run_experiment()
        evaluation.save_compressed_output("iteration" + str(i),
                                          "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/output/results"
                                          "/calibration/throwaway/demandsimulationResult.csv",
                                          "/home/paincrash/Desktop/master-thesis/experiment_results_permanent"
                                          "/experiment4/",
                                          "")
