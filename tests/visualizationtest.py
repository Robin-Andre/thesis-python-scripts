import unittest

import numpy as np
import pandas
from matplotlib import pyplot as plt

import metrics.data
from metrics import metric
import visualization
import visualization as plot


class VisualizationTestCase(unittest.TestCase):
    # TODO this is an ggplot and might be unneccessary
    def nontest_plot1(self):
        comparison = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/parameter_experiment" \
                    "/mode_choice_main_parameters/asc_car_p_sigPositive"
        file_original = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/parameter_experiment/ReferenceOriginal"
        df_original = pandas.read_csv(file_original)
        df_original["identifier"] = "Original"
        df_comparison = pandas.read_csv(comparison)
        df_comparison["identifier"] = "Something"
        plot.draw(pandas.concat([df_original, df_comparison]), plot.aggregate_traffic_two_sets)
        self.assertEqual(True, False)  # add assertion here
    # TODO this is an ggplot and might be unneccessary
    def nontest_plot2(self):
        file_original = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/parameter_experiment/ReferenceOriginal"
        df_original = pandas.read_csv(file_original)
        df_original["identifier"] = "Original"
        plot.draw(df_original, plot.aggregate_traffic_two_sets)
        self.assertEqual(True, False)  # add assertion here
    # TODO this is an ggplot and might be unneccessary
    def nontest_plot3(self):
        file_original = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/parameter_experiment/ReferenceOriginalMODAL"
        df_original = pandas.read_csv(file_original)
        df_original["identifier"] = "Original"
        plot.draw(df_original, plot.aggregate_traffic_modal_two_sets)
        self.assertEqual(True, False)  # add assertion here
    # TODO this is an ggplot and might be unneccessary
    def nontest_plot4(self):
        file_original = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/parameter_experiment/ReferenceOriginalMODAL"
        comparison = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/parameter_experiment" \
                    "/mode_choice_main_parameters/asc_car_p_sigPositiveMODAL"
        df_original = pandas.read_csv(file_original)
        df_original["identifier"] = "Original"
        df_comparison = pandas.read_csv(comparison)
        df_comparison["identifier"] = "Something"
        plot.draw(pandas.concat([df_original, df_comparison]), plot.aggregate_traffic_modal_two_sets, modulo=1*60)
        self.assertEqual(True, False)  # add assertion here


    def test_modal_split_plot(self):
        data = metrics.data.Data()
        data2 = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        data2.load("resources/example_config_load2/results/")

        modal_split = data.get_modal_split()
        modal_split2 = data2.get_modal_split()

        print(plot.draw_modal_split([modal_split, modal_split2]))

    def test_mode_choice_aggregate_time_plot(self):
        data = metrics.data.Data()
        data2 = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        data2.load("resources/example_config_load2/results/")

        print(plot.draw_travel_distance_per_mode(data.travel_distance._data_frame))
        plot.draw_travel_distance_per_mode(data2.travel_distance._data_frame)


    def test_rewritten_function(self):
        data = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        temp = data.travel_distance._data_frame
        resolution = 1
        for i in [-1, 0, 1, 2, 3, 4]:

            savess = metric.get_distribution(temp, "distanceInKm", i, resolution=resolution, quantile=1)

            savess.plot.bar(width=1.0, alpha=0.5, color=visualization.color_modes(i))
            #savess.plot()
            pdf, data_points, error = metric.get_fit_and_error_from_dataframe(temp, "distanceInKm", i, dist_name="gamma", resolution=resolution)
            print(data_points)
            print(error)
            plt.plot(np.linspace(0, len(pdf) / 10, len(pdf)), pdf, color=visualization.color_modes(i))
            plt.title(visualization.label_modes(i))
            plt.tick_params(bottom=None, labelbottom=True)
            plt.show()


    def test_approxis(self):
        data = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        data2 = metrics.data.Data()
        data2.load("resources/example_config_load2/results/")

        data.travel_time.draw_all_distributions()
        data2.travel_time.draw_all_distributions()

        data.travel_distance.draw_all_distributions()
        data2.travel_distance.draw_all_distributions()

        print(visualization.draw_modal_split([data.get_modal_split(), data2.get_modal_split()]))

    def test_traffic_demand(self):
        data = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        visualization.draw_travel_demand(data.traffic_demand.get_mode_specific_data(-1))
        visualization.draw_travel_demand(data.traffic_demand.get_mode_specific_data(1))

    # TODO remove after testing
    def test_traffic_demand_smoothing(self):
        data = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        temp = data.traffic_demand.get_mode_specific_data(-1)
        for i in [2, 15, 30, 60, 240, 1440]:
            tmp = temp.rolling(i).mean()
            tmp2 = temp.ewm(span=i).mean()
            #temp = temp.rolling(3).mean()
            visualization.draw_travel_demand(tmp, title="Simple" + str(i))
            visualization.draw_travel_demand(tmp2, title="Exponen" + str(i))



    def test_traffic_demand_mode(self):
        data = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        visualization.draw_travel_demand_by_mode(data.traffic_demand)

    def test_pedestal(self):
        data = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        data.travel_time.draw_distribution(mode=3)

    def test_difference_plot(self):
        data = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        data2 = metrics.data.Data()
        data2.load("resources/example_config_load2/results/")
        visualization.draw_travel_demand_by_mode(data.traffic_demand.smoothen(60) - data2.traffic_demand.smoothen(60))


if __name__ == '__main__':
    unittest.main()
