# This experiment is to test the original configs and testing which config has the biggest impact
import configloader
import evaluation
import yamlloader
import re
import mobitopp_execution as simulation


def extract_values_of_iteration(config, iteration):
    lines = config.text.split("\n")
    results = []
    for line in lines:
        test = re.sub("=\s*([-+])", "= \\1", line)
        test = re.split("(?<!=\s)([-+])", test)
        temp = 2 * iteration + 1
        results.append(" ".join(test[0:temp]))
    return "\n".join(results)


if __name__ == '__main__':
    simulation.restore_experimental_configs()
    cwd = "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/"
    csv_path = cwd + "output/results/calibration/throwaway/demandsimulationResult.csv"
    yaml_file = "config/rastatt/short-term-module-100p.yaml"
    yaml = yamlloader.YAML(cwd + yaml_file)
    config_list = yaml.find_configs(cwd)
    for config in config_list:
        for i in range(6):
            simulation.restore_experimental_configs()
            text = extract_values_of_iteration(config, i)
            configloader.write_config_file(text, cwd + config.path)
            print("Running config[" + config.name + "] number: " + str(i))
            simulation.run_experiment()
            evaluation.save_compressed_output(config.name + "iteration" + str(i),
                                          "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/output/results"
                                          "/calibration/throwaway/demandsimulationResult.csv",
                                          "/home/paincrash/Desktop/master-thesis/experiment_results_permanent"
                                          "/experiment5/",
                                          "")
