import subprocess

import yamlloader
import mobitopp_execution as simulation


def binary_parameter_search(config, cwd_internal, param_name, signum, num_iterations, lower_bound, upper_bound):
    if num_iterations == 0:
        return (lower_bound + upper_bound) / 2
    print("Running mobitopp limit check on parameter: " + param_name + " | " + str(lower_bound) + " | current max value"
          + str(upper_bound) + " iteration_depth: " + str(num_iterations))
    original_value = config.get_parameter(param_name)
    print("Original Config value: " + str(original_value))
    new_value = 0

    if upper_bound == -1:
        new_value = 2 * lower_bound
    else:
        new_value = (lower_bound + upper_bound) / 2
    config.override_parameter(param_name, signum * new_value)
    config.write()
    # Has the execution failed yes or no.
    return_value = simulation.run_mobitopp(cwd_internal)
    config.override_parameter(param_name, original_value)
    config.write()
    new_upper_bound = upper_bound
    new_lower_bound = lower_bound
    if return_value == 1:
        print("Run has failed! " + param_name + " ")
        new_upper_bound = new_value
    else:
        new_lower_bound = new_value
    return binary_parameter_search(config, cwd_internal, param_name, signum, num_iterations - 1, new_lower_bound, new_upper_bound)


def search_config(config):
    parameter_list = config.get_parameter_list()
    lower_bound_parameters = []
    upper_bound_parameters = []

    # This can be done smarter
    for item in range(len(parameter_list)):
        lower_bound_parameters.append(0)
        upper_bound_parameters.append(0)
    # config.randomize(config.get_parameter_list(), -100, 100)
    for item in range(len(parameter_list)):
        lower_bound_parameters[item] = binary_parameter_search(config, cwd, parameter_list[item], -1, 10, 1, -1)
        upper_bound_parameters[item] = binary_parameter_search(config, cwd, parameter_list[item], 1, 10, 1, -1)
    print(lower_bound_parameters)
    print(upper_bound_parameters)
    return [lower_bound_parameters, upper_bound_parameters]


if __name__ == '__main__':
    cwd = "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/"
    yaml_file = "config/rastatt/short-term-module-100p.yaml"
    yaml = yamlloader.YAML(cwd, yaml_file)
    yaml.data['seed'] = 1
    yaml.data['fractionOfPopulation'] = 0.001
    yaml.data['resultFolder'] = "output/results/calibration/throwaway"
    yaml.write()
    configs = yaml.find_configs(cwd)
    configs.pop(0) # A previous test has shown that the first accepts all [-500,500]
    results = []
    for co in configs:
        results.append(search_config(co))
    print(results)
    yaml.reset()


