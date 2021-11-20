import os
import pandas
import visualization as plot


def helper_plot_method(directory):
    file_original = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/seed_experiment/1/1Seed"
    df_original = pandas.read_csv(file_original)
    df_original["identifier"] = "Original"
    df_original_modal = pandas.read_csv(file_original + "MODAL")
    df_original_modal["identifier"] = "OriginalModal"
    configs = ["destination_choice_utility_calculation_parameters.txt",
               "destination_choice_parameters_SHOPPING.txt",
               "destination_choice_parameters_SERVICE.txt", "destination_choice_parameters_LEISURE.txt",
               "destination_choice_parameters_BUSINESS.txt", "mode_choice_main_parameters.txt"]
    #configs = ["mode_choice_main_parameters.txt"]
    for config in configs:
        for i in range(6):
            df_cur = pandas.read_csv(directory + config + "iteration" + str(i))
            df_cur["identifier"] = "Iteration" + str(i)
            df_cur_modal = pandas.read_csv(directory + config + "iteration" + str(i) + "MODAL")
            df_cur_modal["identifier"] = "Iteration" + str(i)
            title = config.split(".")[0] + " Iteration " + str(i)
            # j = i + 1
            # df_next = pandas.read_csv(directory + config + "iteration" + str(j))
            # df_next["identifier"] = "Iteration" + str(j)
            # df_next_modal = pandas.read_csv(directory + config + "iteration" + str(j) + "MODAL")
            # df_next_modal["identifier"] = "Iteration" + str(j)

            # plot.draw(pandas.concat([df_cur, df_next]), plot.aggregate_traffic_two_sets)
            # plot.draw(pandas.concat([df_cur_modal, df_next_modal]), plot.aggregate_traffic_modal_two_sets)
            save_dir = directory + "plots/"
            plot.draw(pandas.concat([df_cur, df_original]), plot.aggregate_traffic_two_sets, title=title, path=save_dir, show=False)
            title = title + "Modal"
            plot.draw(pandas.concat([df_cur_modal, df_original_modal]), plot.aggregate_traffic_modal_two_sets, title=title, path=save_dir, show=False)


if __name__ == '__main__':
    directory_5 = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/experiment5/" # When only the config is reset
    directory_6 = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/experiment6/" # When all but the current config is reset
    helper_plot_method(directory_5)
    helper_plot_method(directory_6)
