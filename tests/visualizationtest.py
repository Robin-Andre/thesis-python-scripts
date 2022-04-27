import unittest

import numpy as np
import pandas
from matplotlib import pyplot as plt

import metrics.data
from calibration.evolutionary.individual import Individual
from metrics import metric
import visualization
import visualization as plot


class VisualizationTestCase(unittest.TestCase):

    def test_modal_split_plot(self):
        data = metrics.data.Data()
        data2 = metrics.data.Data()
        data.load("resources/example_config_load_new/results/")
        data2.load("resources/example_config_load_new2/results/")

        modal_split = data._get_modal_split()
        modal_split2 = data2._get_modal_split()

        print(plot.draw_modal_split([modal_split, modal_split2]))

    def test_mode_choice_aggregate_time_plot(self):
        data = metrics.data.Data()
        data2 = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        data2.load("resources/example_config_load2/results/")

        print(plot.draw_travel_distance_per_mode(data.travel_distance._data_frame))
        plot.draw_travel_distance_per_mode(data2.travel_distance._data_frame)

    def test_approxis(self):
        data = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        data2 = metrics.data.Data()
        data2.load("resources/example_config_load2/results/")

        data.travel_time.draw_all_distributions()
        data2.travel_time.draw_all_distributions()

        data.travel_distance.draw_all_distributions()
        data2.travel_distance.draw_all_distributions()

        print(visualization.draw_modal_split([data._get_modal_split(), data2._get_modal_split()]))

    def test_traffic_demand(self):
        data = metrics.data.Data()
        data.load("resources/example_config_load_new/results/")
        visualization.draw_travel_demand(data.traffic_demand.get_mode_specific_data(-1))
        visualization.draw_travel_demand(data.traffic_demand.get_mode_specific_data(1))

    def test_detailed_ind(self):
        x = Individual(21, [])
        x_d = Individual(22, [])
        x.load("resources/detailed_individual")
        x_d.load("resources/even_more_detailed_individual")
        #y = x.data.travel_time.get_data_frame()
        #visualization.two_level_travel_time(y, "gender")
        d = x_d.data.get_grouped_modal_split(["age", "gender"])
        visualization.draw_grouped_modal_split(d, reference=d)


    def test_traffic_demand_mode(self):
        data = metrics.data.Data()
        data.load("resources/example_config_load_new/results/")
        data2 = metrics.data.Data()
        data2.load("resources/example_config_load_new2/results/")
        #visualization.draw_modal_split_new_name(data, None, data2)
        #visualization.draw_modal_split_new_name(data, "gender", data2)
        fig, ax = plt.subplots()
        visualization.draw_modal_split_new_name(data, None, data2, ax=ax)
        fig.suptitle("Modal Split")
        fig.set_tight_layout(True)
        fig.show()
        fig.savefig("../plots/example_modal_split.svg", format="svg")
        fig = data.traffic_demand.draw(reference=data2.traffic_demand)
        fig.show()
        fig.savefig("../plots/example_traffic.svg", format="svg")
        fig2 = data.traffic_demand.draw_smooth(reference=data2.traffic_demand, smoothness_factor=15)
        fig2.show()
        fig2 = data.travel_time.draw(reference=data2.travel_time, suptitle="Time Distribution")
        fig2.show()
        fig2.savefig("../plots/example_travel_time.svg", format="svg")
        fig3 = data.travel_distance.draw(reference=data2.travel_distance, suptitle="Distance Distribution")
        fig3.show()
        fig3.savefig("../plots/example_travel_distance.svg", format="svg")
        visualization.draw_modal_split_new_name(data, None, data2)
        #data.travel_time.draw_distribution()

    def test_pedestal(self):
        data = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        data.draw()
        data.travel_time.draw_distribution(mode=3)

    def test_difference_plot(self):
        data = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        data2 = metrics.data.Data()
        data2.load("resources/example_config_load2/results/")
        visualization.draw_travel_demand_by_mode(data.traffic_demand.smoothen(60), reference_df=data2.traffic_demand.smoothen(60)).show()
        #visualization.draw_travel_demand_by_mode(data.traffic_demand.smoothen(60) - data2.traffic_demand.smoothen(60)).show()

    def test_modal_split_plot(self):
        data = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        visualization.draw_modal_split(data)

    def test_modal_split_plot_two(self):
        data = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        data2 = metrics.data.Data()
        data2.load("resources/example_config_load2/results/")
        visualization.draw_modal_split([data, data2, data, data, data2, data2])

    def test_travel_time_plot(self):
        data = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        visualization.draw_travel_time(data.travel_time)
        visualization.draw_travel_time(data.travel_time.smoothen(3))

    def test_travel_time_plot_two(self):
        data = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        data2 = metrics.data.Data()
        data2.load("resources/example_config_load2/results/")
        visualization.draw_travel_time(data.travel_time)
        visualization.draw_travel_time(data2.travel_time)
        visualization.draw_travel_time(data.travel_time - data2.travel_time)
        visualization.draw_travel_time(data.travel_time, reference=data2.travel_time)

    def test_travel_time_with_reference(self):
        data = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        data2 = metrics.data.Data()
        data2.load("resources/example_config_load2/results/")
        dt1 = data.travel_time
        dt2 = data2.travel_time
        visualization.draw_travel_time_per_mode(dt1, reference_df=dt2).show()
        visualization.draw_travel_time_per_mode(dt1.smoothen(10), reference_df=dt2.smoothen(10)).show()

    def test_travel_distance_with_reference(self):
        data = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        data2 = metrics.data.Data()
        data2.load("resources/example_config_load2/results/")
        dt1 = data.travel_distance
        dt2 = data2.travel_distance
        visualization.draw_travel_distance_per_mode(dt1, reference_df=dt2).show()
        visualization.draw_travel_distance_per_mode(dt1.smoothen(10), reference_df=dt2.smoothen(10)).show()

if __name__ == '__main__':
    unittest.main()
