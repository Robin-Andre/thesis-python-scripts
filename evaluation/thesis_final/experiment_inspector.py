import re
from pathlib import Path

import pandas
from matplotlib import pyplot as plt


def get_algorithm_seed_from_string(string):
    seed = re.findall(r"\d*\_", string)[0][:-1]
    return seed

def get_target_seed_from_string(string):
    seed = re.findall(r"\d*\_", string)[1][:-1]
    return seed

def get_identifier(string, seperator):
    name = string.split(seperator)[0]
    return name

def at_which_iterations_were_the_best_elements_produced(df, metric):
    return df[df[metric + "_best"] == df[metric + "_current"]]

def add_missing_iterations():
    pass

def make_directory_of_csvs_into_one_big_csv(string_path, name, identifier):
    output_dfs = []
    error_dfs = []
    path = Path(string_path)
    for file in path.iterdir():
        x = pandas.read_csv(file)
        x["algorithm_seed"] = get_algorithm_seed_from_string(file.name)
        if file.name.__contains__("_errors"):
            x["target_seed"] = get_target_seed_from_string(file.name)
            error_dfs.append(x)
        else:
            x["identifier"] = get_identifier(file.name, identifier)
            output_dfs.append(x)
    df = pandas.concat(output_dfs)
    df_err = pandas.concat(error_dfs)
    print(path.parent / "CSV_CONCATENATED" / name)
    data_name = name + ".csv"
    df = df.rename(columns=lambda col: col.strip())
    df.to_csv(path.parent / "CSV_CONCATENATED" / data_name, index=False)
    print(path.parent / "CSV_CONCATENATED" / name)
    data_name = name + "_error.csv"
    df_err = df_err.rename(columns=lambda col: col.strip())
    df_err.to_csv(path.parent / "CSV_CONCATENATED" / data_name, index=False)


def pad_iterations(df):
    full_index = list(range(1, df['iteration'].max() + 1))
    temp = df.set_index("iteration")
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

def plot_subset(df, columns_list, legend_cols=None, title=None, color=None):
    temp = df[["iteration", "identifier", "seed", "algorithm_seed"] + columns_list]
    wololo = pad_iterations(temp)
    print(f"Plotting columns: {columns_list}")
    temp = wololo.groupby(["iteration", "identifier"]).mean()[columns_list]
    temp = temp.groupby("identifier")

    fig, ax = plt.subplots(figsize=(8, 6))

    for label, df in temp:
        df = df.droplevel("identifier")
        if legend_cols is not None:
            df.columns = legend_cols
        else:
            df = df.rename(columns={columns_list[0]: label})
        print(label)
        df.plot(ax=ax, color=color)

    fig.suptitle(title)
    fig.show()


METRICS = ["sum_squared_error", "mean_absolute_error", "mean_average_error",
             "root_mean_squared_error", "theils_inequality", "sum_squared_percent_error",
             "mean_sum_squared_error", "sum_cubed_error"]
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
    path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\tuningAlphabeforeBeta\\"
    make_directory_of_csvs_into_one_big_csv(path, "AlphaBeforeBeta", "Before")
    path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\CSV_CONCATENATED\\"

    x = pandas.read_csv(path + "AlphaBeforeBeta.csv")
    for metric in METRICS:
        metric_best = "TravelTime_All_" + metric + "_best"
        #metric_current = "TravelTime_All_" + metric + "_current"

        plot_subset(x, [metric_best])

    print(x)


if __name__ == "__main__":
    #alpha_before_beta()
    main()
