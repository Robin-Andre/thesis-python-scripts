import os
import unittest
import pandas
import scipy

import metric
import visualization as plot


class VisualizationTestCase(unittest.TestCase):
    def test_plot1(self):
        comparison = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/parameter_experiment" \
                    "/mode_choice_main_parameters/asc_car_p_sigPositive"
        file_original = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/parameter_experiment/ReferenceOriginal"
        df_original = pandas.read_csv(file_original)
        df_original["identifier"] = "Original"
        df_comparison = pandas.read_csv(comparison)
        df_comparison["identifier"] = "Something"
        plot.draw(pandas.concat([df_original, df_comparison]), plot.aggregate_traffic_two_sets)
        self.assertEqual(True, False)  # add assertion here

    def test_plot2(self):
        file_original = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/parameter_experiment/ReferenceOriginal"
        df_original = pandas.read_csv(file_original)
        df_original["identifier"] = "Original"
        plot.draw(df_original, plot.aggregate_traffic_two_sets)
        self.assertEqual(True, False)  # add assertion here

    def test_plot3(self):
        file_original = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/parameter_experiment/ReferenceOriginalMODAL"
        df_original = pandas.read_csv(file_original)
        df_original["identifier"] = "Original"
        plot.draw(df_original, plot.aggregate_traffic_modal_two_sets)
        self.assertEqual(True, False)  # add assertion here

    def test_plot4(self):
        file_original = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/parameter_experiment/ReferenceOriginalMODAL"
        comparison = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/parameter_experiment" \
                    "/mode_choice_main_parameters/asc_car_p_sigPositiveMODAL"
        df_original = pandas.read_csv(file_original)
        df_original["identifier"] = "Original"
        df_comparison = pandas.read_csv(comparison)
        df_comparison["identifier"] = "Something"
        plot.draw(pandas.concat([df_original, df_comparison]), plot.aggregate_traffic_modal_two_sets, modulo=1*60)
        self.assertEqual(True, False)  # add assertion here

    def test_plot5(self):
        file_original = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/parameter_experiment/ReferenceOriginalMODAL"
        comparison = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/parameter_experiment" \
                    "/mode_choice_main_parameters/asc_car_p_sigPositiveMODAL"
        comparison2 = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/parameter_experiment" \
                    "/mode_choice_main_parameters/asc_car_p_sigNegativeMODAL"
        df_original = pandas.read_csv(file_original)
        df_original["identifier"] = "Original"
        df_comparison = pandas.read_csv(comparison)
        df_comparison["identifier"] = "Something"
        df_comparison2 = pandas.read_csv(comparison2)
        df_comparison2["identifier"] = "SomethingElse"
        plot.draw(pandas.concat([df_original, df_comparison, df_comparison2]), plot.aggregate_traffic_modal_two_sets, modulo=1*60)
        self.assertEqual(True, False)  # add assertion here

    def test_plot6(self):
        file_original = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/parameter_experiment/ReferenceOriginalMODAL"
        dir = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/parameter_experiment/destination_choice_utility_calculation_parameters/"
        param_name = "b_tt_car_d"
        neg = "NegativeMODAL"
        pos = "PositiveMODAL"
        comparison = dir + param_name + neg
        comparison2 = dir + param_name + pos
        df_original = pandas.read_csv(file_original)
        df_original["identifier"] = "Original"
        df_comparison = pandas.read_csv(comparison)
        df_comparison["identifier"] = "Negative"
        df_comparison2 = pandas.read_csv(comparison2)
        df_comparison2["identifier"] = "Positive"
        plot.draw(pandas.concat([df_original, df_comparison, df_comparison2]), plot.aggregate_traffic_modal_two_sets, modulo=1*60)
        self.assertEqual(True, False)  # add assertion here


    def test_modal_split_plot(self):
        data = metric.Data()
        data2 = metric.Data()
        data.load("resources/example_config_load/results/")
        data2.load("resources/example_config_load2/results/")

        modal_split = data.get_modal_split()
        modal_split2 = data2.get_modal_split()

        print(plot.draw_modal_split([modal_split, modal_split2]))




if __name__ == '__main__':
    unittest.main()
