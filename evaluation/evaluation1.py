import os
import pandas
import visualization as plot

if __name__ == '__main__':
    directory = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/parameter_experiment" \
                "/mode_choice_main_parameters"
    file_original = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/parameter_experiment/ReferenceOriginal"
    df_original = pandas.read_csv(file_original)
    df_original["identifier"] = "Original"
    df_original_modal = pandas.read_csv(file_original + "MODAL")
    df_original_modal["identifier"] = "OriginalModal"
    for file in os.listdir(directory):
        if not file.__contains__("MODAL"):
            df = pandas.read_csv(directory + "/" + file)
            df["identifier"] = file
            # df = df.append(df_original)

            df_modal = pandas.read_csv(directory + "/" + file + "MODAL")
            df_modal["identifier"] = file + "MODAL"
            #df_modal = df_modal.append(df_original_modal)
            temp = pandas.concat([df_original, df])
            plot.draw(temp, plot.aggregate_traffic_two_sets)
            temp = pandas.concat([df_original_modal, df_modal])
            plot.draw(temp, plot.aggregate_traffic_modal_two_sets)
            # ggsave(plot=plot, filename=file, path=directory+"/plots")
            # ggsave(plot=plot_modal, filename=file+"Modal", path=directory + "/plots")
            #print(plot)
            #print(plot_modal)
    #df = pandas.read_csv()