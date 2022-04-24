import re
from pathlib import Path

import pandas
from matplotlib import pyplot as plt

from configurations import SPECS
COLORS = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33"]


def reference_algo_seed_from_string(string):
    print(string[4:])
    return string[4:]

def get_algorithm_seed_from_string(string):
    seed = re.findall(r"\d*\_", string)[0][:-1]
    return seed

def get_target_seed_from_string(string):
    seed = re.findall(r"\d*\_", string)[1][:-1]
    return seed

def get_identifier(string, seperator):
    name = string.split(seperator)[0]
    print(name)
    return name

def at_which_iterations_were_the_best_elements_produced(df, metric):
    return df[df[metric + "_best"] == df[metric + "_current"]]


def ref_make_directory_into_one_big_csv(string_path, name, identifier):
    output_dfs = []
    path = Path(string_path)
    for file in path.iterdir():
        if file.is_dir():
            continue
        x = pandas.read_csv(file)
        x["algorithm_seed"] = reference_algo_seed_from_string(file.name)

        x["identifier"] = identifier
        output_dfs.append(x)
    df = pandas.concat(output_dfs)

    print(path.parent / "CSV_CONCATENATED" / name)
    data_name = name + ".csv"
    df = df.rename(columns=lambda col: col.strip())
    df.to_csv(path.parent / "CSV_CONCATENATED" / data_name, index=False)




def make_directory_of_csvs_into_one_big_csv(string_path, name, identifier, use_new_identifier=False):
    output_dfs = []
    error_dfs = []
    path = Path(string_path)
    for file in path.iterdir():
        if file.is_dir():
            continue
        x = pandas.read_csv(file)
        x["algorithm_seed"] = get_algorithm_seed_from_string(file.name)
        if file.name.__contains__("_errors"):
            x["target_seed"] = get_target_seed_from_string(file.name)
            error_dfs.append(x)
        else:
            if use_new_identifier:
                x["identifier"] = identifier
            else:
                x["identifier"] = get_identifier(file.name, identifier)
            output_dfs.append(x)
    df = pandas.concat(output_dfs)
    df_err = pandas.concat(error_dfs)
    writepath = Path("C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\CSV_CONCATENATED\\")
    print(writepath.parent / "CSV_CONCATENATED" / name)
    data_name = name + ".csv"
    df = df.rename(columns=lambda col: col.strip())
    df.to_csv(writepath.parent / "CSV_CONCATENATED" / data_name, index=False)
    print(writepath.parent / "CSV_CONCATENATED" / name)
    data_name = name + "_error.csv"
    df_err = df_err.rename(columns=lambda col: col.strip())
    df_err.to_csv(writepath.parent / "CSV_CONCATENATED" / data_name, index=False)


def pad_iterations(df, iter_id):
    full_index = list(range(1, df[iter_id].max() + 1))
    temp = df.set_index(iter_id)
    temp = temp.groupby(["identifier", "seed", "algorithm_seed"])
    temp = temp.apply(lambda group: group.reindex(full_index, method='nearest').reset_index())
    temp = temp.reset_index(drop=True)
    temp = temp.sort_index()
    return temp


"""
TravelTime
        tests = {"wilcoxon": scipy.stats.wilcoxon, "ttest": scipy.stats.ttest_rel, "ks": scipy.stats.ks_2samp}
        d_names = ["default", "aggegated_none", "all"]
        if input is None or comparison is None:
            for d_name in d_names:
                for test_name in tests.keys():
                    self.statistic_tests["CountComparisonStatisticTest_" + name + "_" + test_name + "_" + d_name

time
        mode_list = {"all": -1, "bike": 0, "car": 1, "passenger":2, "pedestrian": 3, "public_transport": 4}
        tests = {"ks": scipy.stats.kstest, "ttest": scipy.stats.ttest_ind, "ranksums": scipy.stats.ranksums}
name + "_" + test_name + "_" + mode_name
"""

def get_distribution_tests(name, mode_list=[-1, 0, 1, 2, 3, 4], test_list=["ks", "ttest", "ranksums"], which_element=["best"]):
    mode_dict = {-1: "all", 0: "bike", 1: "car", 2: "passenger", 3: "pedestrian", 4:"public_transport"}
    return [name + "_" + test_name + "_" + mode_dict[mode_num] + "_" + element for test_name in test_list for mode_num in mode_list for element in which_element]

def plot_subset(df, columns_list, legend_cols=None, hide_legend=False, title=None, color=None, slicer=None, areacol=None, axinput=None, rename_iteration=None, smoothen=False):


    temp = df[["iteration", "identifier", "seed", "algorithm_seed"] + columns_list]

    if rename_iteration is not None:
        temp = temp.rename(columns={"iteration": rename_iteration})
        iter_identifier = rename_iteration
    else:
        iter_identifier = "iteration"
    wololo = pad_iterations(temp, iter_identifier)
    print(f"Plotting columns: {columns_list}")
    temp = wololo.groupby([iter_identifier, "identifier"]).mean()[columns_list]
    temp = temp.groupby("identifier")
    if axinput is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    else:
        ax = axinput
    if areacol is not None:
        ax.axhspan(0, areacol, facecolor="green", alpha=0.2)

    #ax.axhline(y=159548)
    for i, (label, df) in enumerate(temp):
        df = df.droplevel("identifier")
        if legend_cols is not None:
            df.columns = legend_cols
        else:
            df = df.rename(columns={columns_list[0]: label})
        print(label)
        if slicer is not None:
            df = df.iloc[slicer, :]
        if smoothen:
            df = df.rolling(5, center=True, min_periods=1).mean()
        if color is not None:
            df.plot(ax=ax, color=color[i])
        else:
            df.plot(ax=ax)
    if hide_legend:
        ax.get_legend().remove()
    if axinput is None:
        fig.suptitle(title)
        fig.show()
        return fig
    return


METRICS = ["sum_squared_error", "mean_absolute_error", "mean_average_error",
             "root_mean_squared_error", "theils_inequality", "sum_squared_percent_error",
             "mean_sum_squared_error", "sum_cubed_error"]
def label_to_color(label):
    pass
def main():

    path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\MyExperimentBetterErrorGuessing\\"
    #make_directory_of_csvs_into_one_big_csv(path, "BetterBoundEstimation", "BetterBounds")

    #path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\tuningAlphabeforeBeta\\"
    #make_directory_of_csvs_into_one_big_csv(path, "AlphaBeforeBeta", "Before")

    path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\CSV_CONCATENATED\\"

    x = pandas.read_csv(path + "BetterBoundEstimation.csv")

    for metric in METRICS:
        metric_best = "TravelTime_All_" + metric + "_best"
        metric_current = "TravelTime_All_" + metric + "_current"

        plot_subset(x, [metric_best, metric_current])
    exit()
    metric = "theils_inequality"
    metric_best = "TravelTime_All_" + metric + "_best"
    metric_current = "TravelTime_All_" + metric + "_current"
    plot_subset(x, [metric_best])
    plot_subset(x, [metric_best, metric_current])
    plot_subset(x, get_distribution_tests("time", test_list=["ks"], which_element=["current"]))
    plot_subset(x, get_distribution_tests("time", test_list=["ttest"], which_element=["current"]))
    plot_subset(x, get_distribution_tests("time", test_list=["ranksums"], which_element=["current"]))


def alpha_before_beta():
    #path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\tuningAlphabeforeBeta\\"
    #make_directory_of_csvs_into_one_big_csv(path, "AlphaBeforeBeta", "Before")
    path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\CSV_CONCATENATED\\"

    x = pandas.read_csv(path + "AlphaBeforeBeta.csv")
    refs = pandas.read_csv(SPECS.EXP_PATH_LOCAL + "TargetArea002.csv", index_col=0)
    print(refs)
    for metric in METRICS:
        metric_best = "TravelTime_All_" + metric + "_best"
        areacol = refs["TravelTime_All_" + metric]["max"]
        #metric_current = "TravelTime_All_" + metric + "_current"

        plot_subset(x, [metric_best], areacol=areacol)

    print(x)

def quantiles_which_distribution():
   # path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\MyExperimentQuantiles\\"
   # make_directory_of_csvs_into_one_big_csv(path, "QuantileDistributionExperiment", "1")
    path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\CSV_CONCATENATED\\"

    x = pandas.read_csv(path + "QuantileDistributionExperiment.csv")

    #for metric in METRICS:
    #    metric_best = "TravelTime_All_" + metric + "_best"
    #    #metric_current = "TravelTime_All_" + metric + "_current"

    #    plot_subset(x, [metric_best])
    for metric in METRICS:
        metric_cur = "TravelTime_All_" + metric + "_current"
        #metric_current = "TravelTime_All_" + metric + "_current"

        plot_subset(x, [metric_cur])
    print(x)

def make_big_csvs():
    path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\MyExperimentQuantiles\\"
    make_directory_of_csvs_into_one_big_csv(path, "QuantileDistributionExperiment", "1")

    path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\MyExperimentVariableQuantiles\\"
    make_directory_of_csvs_into_one_big_csv(path, "MyExperimentVariableQuantiles", "1")
    path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\MyExperimentVariableQuantilesFixedOutput\\"
    make_directory_of_csvs_into_one_big_csv(path, "MyExperimentVariableQuantilesFixedOutput", "1")
    path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\MyExperimentVariableQuantilesCostFixedOutput\\"
    make_directory_of_csvs_into_one_big_csv(path, "MyExperimentVariableQuantilesCostFixedOutput", "1")
    path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\MyExperimentVeryHighPrecision\\"
    make_directory_of_csvs_into_one_big_csv(path, "MyExperimentVeryHighPrecision", "1")
    path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\RecreatingManualTuningProcess2\\"
    make_directory_of_csvs_into_one_big_csv(path, "RecreatingTuningProcess", "1")

def __helper(name, identifier):
    path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\"+ name + "\\"
    print(path)
    ref_make_directory_into_one_big_csv(path, name, identifier)



def make_ref_csvs():
    dirs_and_ids = {
        "pygad_10_parameters_target_has_same_seed": "GA_Modal",
        "pygad_10_parameters_target_has_same_seed_time_metric": "GA_Time",
        "pygad_main_destination_same_seed": "GA_D",
        "pygad_main_destination_same_seed_plus_all": "GA_D+All",
        "pygad_main_destination_same_seed_plus_business": "GA_D+B",
        "pygad_main_mode_all_parameters": "GA_Full",
        "pyswarms_10_parameters_target_has_same_seed": "Swarm_Modal",
        "pyswarms_10_parameters_target_has_same_seed_time_metric": "Swarm_Time",
        "pyswarms_main_destination_same_seed": "Swarm_D",
        "pyswarms_main_destination_same_seed_plus_all": "Swarm_D+All",
        "pyswarms_main_destination_same_seed_plus_business": "Swarm_D+B",
        "pyswarms_main_mode_all_parameters": "Swarm_Full",
        "spsa_10_parameters_target_has_same_seed": "SPSA_Modal",
        "spsa_main_destination_same_seed": "SPSA_D",
        "spsa_main_destination_same_seed_plus_all": "SPSA_D+All",
        "spsa_main_destination_same_seed_plus_business": "SPSA_D+B",
        "spsa_main_mode_all_parameters": "SPSA_Full",
        "pyswarms_10_parameters_target_has_same_seed_time_metric2": "Swarm_Seed",
        "pygad_10_parameters_target_has_same_seed_time_metric2": "GA_Seed",
        "spsa_10_parameters_target_has_same_seed_time_metric2": "SPSA_Seed"

    }
    for k, v in dirs_and_ids.items():
        __helper(k, v)


def __helper_ifv(name, identifier):
    path = "\\\\ifv-fs\\User\\Abschlussarbeiten\\Robin.Andre\\Experimente\\Ergebnisse\\" + name + "\\"
    print(path)
    make_directory_of_csvs_into_one_big_csv(path, name, identifier, use_new_identifier=True)

def make_ifv_csvs():
    dirs_and_ids = {
        "MyAlgorithmFullMode": "Algo",
        "MyAlgorithmFullTwoPasses": "Algo2PassesOld",
        "MyAlgorithmFullTwoPassesNewSetWithTargetSeed": "Algo2Passes",
        "MyAlgorithmFullTwoPassesNoMinMax": "Algo2PassesNoMinMax",
    }
    for k, v in dirs_and_ids.items():
        __helper_ifv(k, v)

if __name__ == "__main__":
    make_ifv_csvs()
    make_ref_csvs()
    make_big_csvs()
    #quantiles_which_distribution()
    #alpha_before_beta()
    #main()
