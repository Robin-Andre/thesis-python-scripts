# This experiment tries to analyze which config has the most impact by setting all other configs to the default values 0
import os

import configloader
import evaluation
import yamlloader
import re
import mobitopp_execution as simulation


def extract_values_of_iteration(config_internal, iteration):
    lines = config_internal._text.split("\n")
    results = []
    for line in lines:
        test = re.sub("=\s*([-+])", "= \\1", line)
        test = re.split("(?<!=\s)([-+])", test)
        temp = 2 * iteration + 1
        results.append(" ".join(test[0:temp]))
    return "\n".join(results)


def set_all_configs_to_zero(config_list_internal, cwd_internal):
    for config_internal in config_list_internal:
        text_internal = extract_values_of_iteration(config_internal, 0)
        configloader.write_config_file(text_internal, cwd_internal + config_internal.path)


if __name__ == '__main__':
    yaml_file = "config/rastatt/short-term-module-100p.yaml"
    cwd = "../../mobitopp-example-rastatt/"
    yaml = yamlloader.YAML(cwd, yaml_file)
    simulation.save(yaml, None, "../tests/resources/example_config_load")
    for config in yaml.configs:
        config._text = extract_values_of_iteration(config, 0)
        print(config._text)
    simulation.save(yaml, None, "../tests/resources/example_config_load2")
