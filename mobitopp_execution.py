import subprocess
from pathlib import Path

import configloader
import metric
import yamlloader


def run_mobitopp(directory, yaml_name):
    process = subprocess.Popen(["./gradlew",
                                yaml_name],
                               cwd=directory,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout = process.communicate()[0]
    stderr = process.communicate()[1]
    return_code = process.returncode
    #print(stdout)
    #print('STDOUT:{}'.format(stdout))

    process.wait()
    return return_code


def run():
    default_path = "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/"
    return run_mobitopp(default_path, "runRastatt_100p_ShortTermModule")


# TODO implement loading dumps
def load(relative_path):
    yaml = yamlloader.YAML(Path(relative_path + "launch.yaml"))
    config_dir = Path(relative_path + "configs/").glob('*.txt')
    configs = []
    for path in config_dir:
        config = configloader.Config(path)
        configs.append(config)
    yaml.set_configs(configs)
    data = metric.Data(lo)
    return yaml


# Saves all the data in the relative path
def save(yaml, data, relative_path):
    Path(relative_path).mkdir(parents=True, exist_ok=True)
    yaml.write_path(relative_path + "/launch.yaml")
    Path(relative_path + "/configs").mkdir(parents=True, exist_ok=True)
    for config in yaml.configs:
        config.write_config_file(relative_path + "/configs/" + config.name)
    if data is not None:
        Path(relative_path + "/results").mkdir(parents=True, exist_ok=True)
        data.write(relative_path + "/results/")


# Restores the configs IF the default experimental yaml is used. TODO make check to test for default experimental yaml
def restore_experimental_configs():
    standard_config_path = "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/"
    original_configs = "config/shared/parameters/"
    calibration_configs = "calibration/"
    configs = ["destination_choice_utility_calculation_parameters.txt", "destination_choice_parameters_SHOPPING.txt",
               "destination_choice_parameters_SERVICE.txt", "destination_choice_parameters_LEISURE.txt",
               "destination_choice_parameters_BUSINESS.txt", "mode_choice_main_parameters.txt"]
    for config in configs:
        input_file = open(standard_config_path + original_configs + config, "r")
        text = input_file.read()
        output_file = open(standard_config_path + calibration_configs + config, "w")
        output_file.write(text)
        input_file.close()
        output_file.close()
    return


def run_experiment():
    default_path = "/home/paincrash/Desktop/master-thesis/mobitopp-example-rastatt/"
    return run_mobitopp(default_path, "runRastatt_100p_ShortTermModule")
