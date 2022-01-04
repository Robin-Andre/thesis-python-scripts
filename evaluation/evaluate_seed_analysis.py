from pathlib import Path

import mobitopp_execution as simulation
import visualization
from configurations import SPECS

if __name__ == '__main__':
    exp_path = SPECS.EXP_PATH + "same_config_different_seed/"
    simulation.reset()
    data_list = []
    for file in Path(exp_path).iterdir():

        yaml, data = simulation.load(file)
        print(yaml.get_seed())
        data_list.append(data)
    for i, x in enumerate(data_list):
        for j, y in enumerate(data_list):
            if x != y:
                visualization.draw_travel_demand_by_mode(x.traffic_demand.smoothen(60) - y.traffic_demand.smoothen(60), title=str(i) + "->" + str(j))
    a, b = data_list[0].traffic_demand, data_list[1].traffic_demand
    c, d = a.smoothen(60), b.smoothen(60)
    visualization.draw_travel_demand_by_mode(c - d)
    visualization.draw_travel_demand_by_mode(a - b)




