from pathlib import Path

import mobitopp_execution as simulation

# experiment_path = "C:/Users/Admin/Desktop/master-thesis/neural_network_data"
experiment_path = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/"

def get_experiments():
    path = Path(experiment_path)
    return [file.name for file in path.iterdir()]


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