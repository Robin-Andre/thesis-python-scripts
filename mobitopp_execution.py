import inspect
import os
import platform
from datetime import datetime
import subprocess
from pathlib import Path

import pandas

import metrics.data
from configurations import configloader, SPECS
from metrics import metric
import yamlloader


def default_yaml():
    yaml_file = "config/rastatt/short-term-module-100p.yaml"
    yaml = yamlloader.YAML(Path(SPECS.CWD + yaml_file))
    yaml.set_configs(yaml.find_calibration_configs(SPECS.CWD))
    return yaml


def run_mobitopp(yaml=default_yaml()):
    yaml.write_path(SPECS.CWD + "config/rastatt/short-term-module-100p.yaml")
    clean_result_directory(yaml)
    if platform.system() == "Linux":
        return __run_mobitopp_linux(), results(yaml)
    if platform.system() == "Windows":
        return __run_mobitopp_windows(), results(yaml)

    raise EnvironmentError("Platform not supported by calibration tool: " + inspect.currentframe())

#TODO eventually pass that windows do not need a change of path
def __run(command):
    process = subprocess.Popen([command,
                                "runRastatt_100p_ShortTermModule"],
                               cwd=Path(SPECS.CWD),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    stdout = process.communicate()[0]
    stderr = process.communicate()[1]
    return_code = process.returncode
    # print(stdout)
    # print(stderr)
    # print('STDOUT:{}'.format(stdout))

    process.wait()
    return return_code


def __run_mobitopp_linux():
    ret = __run(".gradlew")
    restore_default_yaml()
    return ret


def __run_mobitopp_windows():
    old_dir = os.getcwd()
    os.chdir(SPECS.CWD)
    ret = __run("gradlew.bat")
    os.chdir(old_dir)
    restore_default_yaml()
    return ret


def load(relative_path_raw):
    relative_path = str(relative_path_raw) + "/"
    yaml = yamlloader.YAML(Path(relative_path + "launch.yaml"))
    config_dir = Path(relative_path + "configs/").glob('*.txt')
    configs = []
    for path in config_dir:

        if path.name.__contains__("mode_choice_main_parameters"):
            config = configloader.ModeChoiceConfig(path)
        if path.name.__contains__("destination_choice_utility_calculation_parameters"):
            config = configloader.DestinationChoiceConfig(path)
        else:
            config = configloader.Config(path)

        configs.append(config)
    yaml.set_configs(configs)
    yaml.set_config_to_calibration()
    data = metrics.data.Data()
    if Path(relative_path + "results/").exists():
        data.load(relative_path + "results/")
    return yaml, data


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


def results(yaml=default_yaml()):
    file = SPECS.CWD + yaml.data["resultFolder"] + "/demandsimulationResult.csv"
    if Path(file).exists():
        return metrics.data.Data(pandas.read_csv(file, sep=";"))
    return None


# Restores the configs IF the default experimental yaml is used. TODO make check to test for default experimental yaml
def restore_experimental_configs():
    original_configs = "config/shared/parameters/"
    calibration_configs = "calibration/"
    configs = ["destination_choice_utility_calculation_parameters.txt", "destination_choice_parameters_SHOPPING.txt",
               "destination_choice_parameters_SERVICE.txt", "destination_choice_parameters_LEISURE.txt",
               "destination_choice_parameters_BUSINESS.txt", "mode_choice_main_parameters.txt"]
    for config in configs:
        # TODO open with()
        input_file = open(SPECS.CWD + original_configs + config, "r")
        text = input_file.read()
        output_file = open(SPECS.CWD + calibration_configs + config, "w")
        output_file.write(text)
        input_file.close()
        output_file.close()
    return


def restore_default_yaml():
    yaml = "short-term-module-100p.yaml"
    folder = "rastatt/"
    # TODO open with()
    input_file = open(SPECS.CWD + "calibration/" + yaml, "r")
    text = input_file.read()
    output_file = open(SPECS.CWD + "config/" + folder + yaml, "w")
    output_file.write(text)
    input_file.close()
    output_file.close()


def clean_result_directory(yaml=default_yaml()):
    clean_directory(Path(SPECS.CWD + yaml.data["resultFolder"]))


def clean_directory(path):
    for file in path.iterdir():
        Path.unlink(file)

def run_experiment(yaml=default_yaml(), experiment_name=""):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"Running Experiment: {experiment_name} : starting at {current_time}")

    result = run_mobitopp(yaml)
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"Experiment {experiment_name} finished at {current_time} with return code {result}")
    if result == 0:
        return results()
    return None
