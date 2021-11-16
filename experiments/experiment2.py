import evaluation
import yamlloader
import mobitopp_execution as simulation


def binary_parameter_search(config, cwd_internal, param_name, signum, num_iterations, cur_value, upper_bound):
    if num_iterations == 0:
        return cur_value
    print("Running mobitopp limit check on parameter: " + param_name + " | " + str(cur_value) + " | current max value"
          + str(upper_bound) + " iteration_depth: " + str(num_iterations))
    original_value = config.get_parameter(param_name)
    print("Original Config value: " + str(original_value))

    config.override_parameter(param_name, signum * cur_value)
    config.write()
    # Has the execution failed yes or no.
    return_value = simulation.run()
    config.override_parameter(param_name, original_value)
    config.write()
    new_upper_bound = upper_bound
    new_cur_value = cur_value
    signum_text = "Positive" if signum == 1 else "Negative"
    if return_value == 1:
        print("Run has failed! " + param_name + " ")
        new_upper_bound = cur_value
        new_cur_value = cur_value / 2
    else:
        print("Run succeeded! " + param_name + " ")
        evaluation.save_compressed_output(param_name,
                               "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/output/results"
                               "/calibration/throwaway/demandsimulationResult.csv",
                               "/home/paincrash/Desktop/master-thesis/experiment_results_permanent"
                               "/parameter_experiment/"
                               + config.name.split(".")[0] + "/",
                               signum_text)
        if upper_bound == -1:
            new_cur_value = 2 * cur_value
        else:
            new_cur_value = (cur_value + upper_bound) / 2

    return binary_parameter_search(config, cwd_internal, param_name, signum, num_iterations - 1, new_cur_value,
                                   new_upper_bound)


def run_parameter(config_internal, cwd_internal, item_internal, signum):
    original_value = config_internal.get_parameter(item_internal)
    signum_text = "Positive" if signum == 1 else "Negative"
    config_internal.override_parameter(item_internal, -500)
    config_internal.write()
    # Has the execution failed yes or no.
    return_value = simulation.run()
    if return_value == 1:
        print("Parameter: " + item_internal + "FAILED")
    else:
        evaluation.save_compressed_output(item_internal,
                                          "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/output/results"
                                          "/calibration/throwaway/demandsimulationResult.csv",
                                          "/home/paincrash/Desktop/master-thesis/experiment_results_permanent"
                                          "/parameter_experiment/"
                                          + config_internal.name.split(".")[0] + "/",
                                          signum_text)
    config_internal.override_parameter(item_internal, original_value)
    config_internal.write()


def run_every_parameter_in_config(config_internal, cwd_internal):
    parameter_list = config_internal.get_parameter_list()
    for item in parameter_list:
        print("Evaluating parameter [" + item + "]")
        run_parameter(config_internal, cwd_internal, item, -1)
        run_parameter(config_internal, cwd_internal, item, 1)
    return


if __name__ == '__main__':
    cwd = "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/"
    yaml_file = "config/rastatt/short-term-module-100p.yaml"
    yaml = yamlloader.YAML(cwd + yaml_file)
    yaml.data['seed'] = 1
    yaml.data['fractionOfPopulation'] = 0.01
    yaml.data['resultFolder'] = "output/results/calibration/throwaway"
    # yaml.data['modeChoice']['main'] = "calibration/mode_choice_main_parameters.txt"
    yaml.data['destinationChoice']['base'] = "calibration/destination_choice_utility_calculation_parameters.txt"
    yaml.write()

    configs = yaml.find_configs(cwd)
    print(configs[0].print())
    config = configs[0]
    lower_bound_vec = []
    upper_bound_vec = []
    for item in config.get_parameter_list():
        lower_bound_vec.append(binary_parameter_search(config, cwd, item, -1, 10, 16, -1))

        upper_bound_vec.append(binary_parameter_search(config, cwd, item, 1, 10, 16, -1))

    # run_every_parameter_in_config(configs[-1], cwd)
    # for config in configs:
    #    print(config.name)
    #    run_every_parameter_in_config(config, cwd)

    yaml.reset()
    print(lower_bound_vec)
    print(upper_bound_vec)
