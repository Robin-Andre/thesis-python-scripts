import difflib

import pandas
import experiment_inspector
import visualization
from calibration.evolutionary.individual import Individual
from metrics.data import Data
import mobitopp_execution as simulation

METRICS = ["sum_squared_error", "mean_absolute_error", "mean_average_error",
             "root_mean_squared_error", "theils_inequality", "sum_squared_percent_error",
             "mean_sum_squared_error", "sum_cubed_error"]
DATAFRAMES = ["TravelTime", "TrafficDemand", "TrafficDemand5min", "TrafficDemand15min", "TrafficDemand60min",
              "TravelDistance", "ZoneDemand"]
SPECIALIZATIONS = ["All", "Default", "None"]
MODAL_SPLIT_DFS = ["ModalSplit_Default", "ModalSplit_Detailed"]
MODAL_SPLIT_SPECS = ["Splits", "Counts"]

COUNTS_STATS = ["Destinations", "TravelDistance", "TrafficDemand", "TravelTime"]
COUNT_STAT_SPECS = ["default", "aggegated_none",  "all"]
COUNT_STAT_TESTS = ["wilcoxon", "ttest", "ks"]

TEST_STATS = ["time", "distance"]
TEST_STAT_SPECS = ["all", "bike", "car", "passenger", "pedestrian", "public_transport"]
TEST_STAT_TESTS = ["ks", "ttest", "ranksums"]

ELEMENT = ["best", "current"]

def get_vals(x, name_list):
    if x is None:
        return name_list
    if type(x) is int:
        return [name_list[x]]
    if type(x) is str:
        return difflib.get_close_matches(x, name_list)
    return list(name_list[i] for i in x)

def get_metrics(dfname=None, spec=None, funcs=None, ele=None):
    dfname = get_vals(dfname, DATAFRAMES)
    spec = get_vals(spec, SPECIALIZATIONS)
    funcs = get_vals(funcs, METRICS)
    ele = get_vals(ele, ELEMENT)
    ret_list = []
    for df in dfname:
        for s in spec:
            for func in funcs:
                for el in ele:
                    ret_list.append(df + "_" + s + "_" + func + "_" + el)

    return ret_list

def get_modal_metrics(dfname=None, spec=None, funcs=None, ele=None):
    dfname = get_vals(dfname, MODAL_SPLIT_DFS)
    spec = get_vals(spec, MODAL_SPLIT_SPECS)
    funcs = get_vals(funcs, METRICS)
    ele = get_vals(ele, ELEMENT)
    ret_list = []
    for df in dfname:
        for s in spec:
            for func in funcs:
                for el in ele:
                    ret_list.append(df + "_" + s + "_" + func + "_" + el)

    return ret_list

def get_count_tests(dfname=None, spec=None, funcs=None, ele=None):
    dfname = get_vals(dfname, COUNTS_STATS)
    spec = get_vals(spec, COUNT_STAT_SPECS)
    funcs = get_vals(funcs, COUNT_STAT_TESTS)

    ele = get_vals(ele, ELEMENT)
    ret_list = []
    for df in dfname:
        for s in spec:
            for func in funcs:
                for el in ele:
                    ret_list.append("CountComparisonStatisticTest_" + df + "_" + func + "_" + s + "_" + el)

    return ret_list

def get_stochastic_tests(dfname=None, spec=None, funcs=None, ele=None):
    dfname = get_vals(dfname, TEST_STATS)
    spec = get_vals(spec, TEST_STAT_SPECS)
    funcs = get_vals(funcs, TEST_STAT_TESTS)
    ele = get_vals(ele, ELEMENT)
    ret_list = []
    for df in dfname:
        for s in spec:
            for func in funcs:
                for el in ele:
                    ret_list.append(df + "_" + func + "_" + s + "_" + el)

    return ret_list

def plot_iteration_put_only(path, iteration, reference=None):
    data = Data()
    data.load(path + "\\individual_" + str(iteration) + "\\results\\")
    tt = data.travel_time
    df = tt.get_data_frame()
    df = df[df["tripMode"] == 4]
    tt._data_frame = df
    title = "Travel Time Distribution: Iteration " + str(iteration)
    if reference is not None:
        b = tt.draw(reference=reference.travel_time, suptitle=title)
    else:
        b = tt.draw(suptitle=title)
    b.show()


def are_you_not_calibrated(df, tests, epsilon=0.05):
    test = df[tests]
    print(test)
    min_series = test.min(axis=1)
    x = min_series.where(min_series <= epsilon)
    return x

def make_plots_for_showing_not_well_calibrated():
    path = "\\\\ifv-fs\\User\\Abschlussarbeiten\\Robin.Andre\\"

    x = pandas.read_csv(path + "ImprovedDetailPasses100_Algo42.csv")
    print(x.columns.values)
    x["algorithm_seed"] = 100
    x["identifier"] = "Default"
    x = x.rename(columns=lambda col: col.strip())

    values = get_stochastic_tests(0, 5, None, 1)
    print(are_you_not_calibrated(x, values))
    experiment_inspector.plot_subset(x, values, legend_cols=["K-S", "T-Test", "Wilcoxon"], title="Public Transport Stochastic Tests")
    reqs = ['workday', 'gender', 'employment', 'age', 'activityType',
            'tripMode', 'previousMode', 'economicalStatus', 'nominalSize', 'totalNumberOfCars']
    params = simulation.default_yaml().mode_config().get_all_parameter_names_on_requirements(reqs)
    plot_iteration_put_only(r"\\ifv-fs\User\Abschlussarbeiten\Robin.Andre\Experimente\Ergebnisse\MyAlgorithmFullTwoPasses\data\ImprovedDetailPasses100_Algo42", 161)

    d = Individual(seed=42, param_list=params)
    d.run()
    data = d.data
    plot_iteration_put_only(r"\\ifv-fs\User\Abschlussarbeiten\Robin.Andre\Experimente\Ergebnisse\MyAlgorithmFullTwoPasses\data\ImprovedDetailPasses100_Algo42", 619, reference=data)

    plot_iteration_put_only(r"\\ifv-fs\User\Abschlussarbeiten\Robin.Andre\Experimente\Ergebnisse\MyAlgorithmFullTwoPasses\data\ImprovedDetailPasses100_Algo42", 160, reference=data)

    plot_iteration_put_only(
        r"\\ifv-fs\User\Abschlussarbeiten\Robin.Andre\Experimente\Ergebnisse\MyAlgorithmFullTwoPasses\data\ImprovedDetailPasses100_Algo42",
        1400, reference=data)


def main():

    path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\MyExperimentBetterErrorGuessing\\"
    #make_directory_of_csvs_into_one_big_csv(path, "BetterBoundEstimation", "BetterBounds")

    #path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\tuningAlphabeforeBeta\\"
    #make_directory_of_csvs_into_one_big_csv(path, "AlphaBeforeBeta", "Before")

    path = "\\\\ifv-fs\\User\\Abschlussarbeiten\\Robin.Andre\\"
    #make_plots_for_showing_not_well_calibrated()
    #return
    x = pandas.read_csv(path + "ImprovedDetailPasses100_Algo42.csv")
    print(x.columns.values)
    x["algorithm_seed"] = 100
    x["identifier"] = "Default"
    x = x.rename(columns=lambda col: col.strip())



    #values = get_metrics([1, 2, 3, 4], "All", 0, 0)
    #experiment_inspector.plot_subset(x, values)
    #values = get_count_tests(1, 1, None, 0)
    #experiment_inspector.plot_subset(x, values)

    for k, v in {"Zones": 0, "Distance": 1, "Demand": 2, "Time": 3}.items():
        values = get_count_tests(v, 1, None, 1)
        experiment_inspector.plot_subset(x, values, title=k)
        if v != 2:
            values = get_count_tests(v, 0, None, 1)
            experiment_inspector.plot_subset(x, values, title=k)
        values = get_count_tests(v, 2, None, 1)
        experiment_inspector.plot_subset(x, values, title=k)

    slicer = slice(None, None, 20)
    values = get_stochastic_tests(0, None, 0, 1)
    experiment_inspector.plot_subset(x, values, legend_cols=visualization.label_modes(None, get_all_and_combined=True), title="K-S", color=visualization.color_modes(None, get_all_and_combined=True), slicer=slicer)
    values = get_stochastic_tests(0, None, 1, 1)
    experiment_inspector.plot_subset(x, values, legend_cols=visualization.label_modes(None, get_all_and_combined=True), title="T-Test", color=visualization.color_modes(None, get_all_and_combined=True), slicer=slicer)
    values = get_stochastic_tests(0, None, 2, 1)
    experiment_inspector.plot_subset(x, values, legend_cols=visualization.label_modes(None, get_all_and_combined=True), title="Wilcoxon", color=visualization.color_modes(None, get_all_and_combined=True), slicer=slicer)
    #values = get_stochastic_tests(0, None, 1, 1)
    #experiment_inspector.plot_subset(x, values)
    #values = get_count_tests(3, 2, None, 1)
    #experiment_inspector.plot_subset(x, values)
    #values = get_count_tests(0, 2, None, 1)
    #experiment_inspector.plot_subset(x, values)
    #values = get_metrics([1, 4], None, 4, 1)
    #experiment_inspector.plot_subset(x, values)
    #values = get_metrics([0], 0, 6, 1)
    #experiment_inspector.plot_subset(x, values)
    #experiment_inspector.plot_subset(x, get_metrics())
    #experiment_inspector.plot_subset(x, get_modal_metrics())
    #experiment_inspector.plot_subset(x, get_count_tests())
    #experiment_inspector.plot_subset(x, get_stochastic_tests())
    return

    supergroup = "TravelTime_All_"
    supergroup = "ModalSplit_Detailed_Counts_"
    set_1 = "ModalSplit"
    for metric in METRICS:
        metric_best = supergroup + metric + "_best"
        metric_current = supergroup + metric + "_current"

        experiment_inspector.plot_subset(x, [metric_best, metric_current])

if __name__ == "__main__":
    main()