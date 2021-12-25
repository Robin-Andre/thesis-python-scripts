from pathlib import Path

import mobitopp_execution as simulation

experiment_path = "C:/Users/Admin/Desktop/master-thesis/neural_network_data"


def get_experiments():
    path = Path(experiment_path)
    return [file.name for file in path.iterdir()]


def find_failed_data(experiment):
    for file in Path(experiment_path + "/" + experiment).iterdir():
        yaml, data = simulation.load(file)
        if data.empty():
            print(file)
