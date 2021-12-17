from pathlib import Path

import pandas

import metric

import mobitopp_execution as simulation
import yamlloader
if __name__ == '__main__':
    expath = Path("/home/paincrash/Desktop/master-thesis/experiment_results_permanent/neural_network_data_modechoice")
    for path in expath.iterdir():
        yaml, data = simulation.load(str(path) + "/")
        data.draw_distributions()



