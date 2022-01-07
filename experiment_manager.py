import shutil
from pathlib import Path

import mobitopp_execution as simulation

#experiment_path = "C:/Users/Admin/Desktop/master-thesis/neural_network_data"
from configurations import SPECS

experiment_path = SPECS.EXP_PATH

accepted_files = ["configs", "launch.yaml", "destination_choice_parameters_BUSINESS.txt",
                  "destination_choice_parameters_LEISURE.txt", "destination_choice_parameters_SERVICE.txt",
                  "destination_choice_parameters_SHOPPING.txt", "destination_choice_utility_calculation_parameters.txt",
                  "mode_choice_main_parameters.txt", "results", "Time.csv", "Demand.csv", "Distance.csv"]


def get_experiments(sub_folder=""):
    path = Path(experiment_path + sub_folder)
    return [file.name for file in path.iterdir() if file.name != "FAILED_RUNS"]


def find_failed_data(experiment):
    names = []
    for file in Path(experiment_path + "/" + experiment).iterdir():
        yaml, data = simulation.load(file)
        if data.empty():
            #print(file)
            names.append(file)

    return names


def plot_data(experiment):
    for file in Path(experiment_path + "/" + experiment).iterdir():
        print(file)
        simulation.plot(file)


def get_configs_from_failures(paths):
    data_list = []
    for path in paths:
        yaml, data = simulation.load(path)
        data_list.append(yaml.mode_config())

    return data_list


def get_dest_configs_from_failures(paths):
    data_list = []
    for path in paths:
        yaml, data = simulation.load(path)
        data_list.append(yaml.destination_config())

    return data_list


def move_data_to_failure(data_path):
    temp = Path(experiment_path + "/FAILED_RUNS")
    if not temp.exists():
        temp.mkdir()
    for file in find_failed_data(data_path):
        shutil.move(str(file), str(temp) + data_path)


def test_cleanliness(ex_path):
    for file in Path(experiment_path + "/" + ex_path).iterdir():
        all_files_conform = all([i.name in accepted_files for i in file.rglob("*")])
        print(f"File {file.name} is clean {all_files_conform}")


def verify(experiment_full_path):
    simulation.clean_result_directory()
    yaml, data = simulation.load(experiment_full_path)
    simulation.run_mobitopp(yaml)
    return data, simulation.results()


def add_plots(ex_path):
    for path in Path(ex_path).iterdir():
        simulation.plot(path)


def rerun(experiment_full_path):
    pass