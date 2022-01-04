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
        #data.draw_distributions()
    a, b = data_list[0], data_list[1]
    x = a.traffic_demand.get_data_frame()
    y = b.traffic_demand.get_data_frame()
    print(y)
    x = x.set_index(["tripMode", "time"])
    y = y.set_index(["tripMode", "time"])
    z = x.sub(y, fill_value=0)
    z = z.reset_index()
    a.traffic_demand._data_frame = z
    print(z)
    visualization.draw_travel_demand_by_mode(a.traffic_demand)
    print(z)



