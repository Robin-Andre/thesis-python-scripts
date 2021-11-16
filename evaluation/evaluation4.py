import os
import pandas
import visualization as plot

if __name__ == '__main__':
    directory = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/experiment4/"
    file_original = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/seed_experiment/1/1Seed"
    df_original = pandas.read_csv(file_original)
    df_original["identifier"] = "Original"
    df_original_modal = pandas.read_csv(file_original + "MODAL")
    df_original_modal["identifier"] = "OriginalModal"
    for i in range(5):
        df_cur = pandas.read_csv(directory + "iteration" + str(i))
        df_cur["identifier"] = "Iteration" + str(i)
        df_cur_modal = pandas.read_csv(directory + "iteration" + str(i) + "MODAL")
        df_cur_modal["identifier"] = "Iteration" + str(i)

        j = i + 1
        df_next = pandas.read_csv(directory  + "iteration" + str(j))
        df_next["identifier"] = "Iteration" + str(j)
        df_next_modal = pandas.read_csv(directory + "iteration" + str(j) + "MODAL")
        df_next_modal["identifier"] = "Iteration" + str(j)
        plot.draw(pandas.concat([df_cur, df_next]), plot.aggregate_traffic_two_sets)
        plot.draw(pandas.concat([df_cur_modal, df_next_modal]), plot.aggregate_traffic_modal_two_sets)
