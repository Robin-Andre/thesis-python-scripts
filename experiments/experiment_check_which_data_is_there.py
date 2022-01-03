from pathlib import Path

from metrics import metric

import mobitopp_execution as simulation

if __name__ == '__main__':
    expath = Path("/home/paincrash/Desktop/master-thesis/experiment_results_permanent/neural_network_data_modechoice")
    for path in expath.iterdir():
        yaml, data = simulation.load(str(path) + "/")
        if not str(path).__contains__("elastic"):
            print(path)
            print(data.travel_time.data_frame.columns)
            #data.travel_time.draw()
            print(metric.get_all_existing_modes(data.travel_time.data_frame))
            data.draw_distributions()
        #data.draw_distributions()



