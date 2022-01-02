import shutil
from pathlib import Path

import mobitopp_execution as simulation

#experiment_path = "C:/Users/Admin/Desktop/master-thesis/neural_network_data"
experiment_path = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/"

accepted_files = ["configs", "launch.yaml", "destination_choice_parameters_BUSINESS.txt",
                  "destination_choice_parameters_LEISURE.txt", "destination_choice_parameters_SERVICE.txt",
                  "destination_choice_parameters_SHOPPING.txt", "destination_choice_utility_calculation_parameters.txt",
                  "mode_choice_main_parameters.txt", "results", "Time.csv", "Demand.csv", "Distance.csv"]


def get_experiments():
    path = Path(experiment_path)
    return [file.name for file in path.iterdir() if file.name != "FAILED_RUNS"]


def find_failed_data(experiment):
    names = []
    for file in Path(experiment_path + "/" + experiment).iterdir():
        yaml, data = simulation.load(file)
        if data.empty():
            #print(file)
            names.append(file)

    return names


def get_configs_from_failures(paths):
    data_list = []
    for path in paths:
        yaml, data = simulation.load(path)
        data_list.append(yaml.configs[4])

    return data_list

def get_dest_configs_from_failures(paths):
    data_list = []
    for path in paths:
        yaml, data = simulation.load(path)
        data_list.append(yaml.configs[2])

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
    yaml, data = simulation.load(experiment_full_path)
    #simulation.run

def rerun(experiment_full_path):
    pass