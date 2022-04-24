import difflib

import pandas
from matplotlib import pyplot as plt

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

def plot_iteration(exp_path, name,  iteration, reference=None):
    data = Data()
    fullpath = exp_path + "data/" + name + "\\individual_" + str(iteration) + "\\results\\"
    print(fullpath)
    data.load(fullpath)
    a, b, c = data.draw_with_title(reference, title=iteration)
    a.show()
    b.show()
    c.show()
    return a, b, c

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

def get_p_row_analysis(df, colnames, title=""):
    temp = df[colnames]
    lol = temp.prod(axis=1)
    print(lol.max())
    print(lol.idxmax())
    #lol.plot(title=title)
    #plt.show()
    return lol

def plot_seed_thingy_spontan():
    reqs = ['workday', 'gender', 'employment', 'age', 'activityType',
            'tripMode', 'previousMode', 'economicalStatus', 'nominalSize', 'totalNumberOfCars']
    params = simulation.default_yaml().mode_config().get_all_parameter_names_on_requirements(reqs)
    d = Individual(seed=42, param_list=params)
    d.run()
    data = d.data
    d2 = Individual(seed=101, param_list=params)
    d2.run()
    a, b, c = d2.data.draw(reference=data)
    a.show()
    b.show()
    c.show()
    return

def main():

    path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\MyExperimentBetterErrorGuessing\\"
    #make_directory_of_csvs_into_one_big_csv(path, "BetterBoundEstimation", "BetterBounds")

    #path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\tuningAlphabeforeBeta\\"
    #make_directory_of_csvs_into_one_big_csv(path, "AlphaBeforeBeta", "Before")

    path = "\\\\ifv-fs\\User\\Abschlussarbeiten\\Robin.Andre\\Experimente\\Ergebnisse\\MyAlgorithmFullTwoPasses\\"
    #make_plots_for_showing_not_well_calibrated()
    #return
    name = "ImprovedDetailPasses100_Algo42"
    x = pandas.read_csv(path + name + ".csv")
    x["algorithm_seed"] = 100
    x["identifier"] = "Default"
    x = x.rename(columns=lambda col: col.strip())
    reqs = ['workday', 'gender', 'employment', 'age', 'activityType',
            'tripMode', 'previousMode', 'economicalStatus', 'nominalSize', 'totalNumberOfCars']
    params = simulation.default_yaml().mode_config().get_all_parameter_names_on_requirements(reqs)
    #d = Individual(seed=42, param_list=params)
    #d.run()
    #data = d.data
    #d2 = Individual(seed=101, param_list=params)
    #d2.run()
    #a, b, c = d2.data.draw(reference=data)
    #a.show()
    #b.show()
    #c.show()
    #return
    #plot_iteration(path, name, 508, reference=data)
    #plot_iteration(path, name, 553, reference=data)
    #plot_iteration(path, name, 546, reference=data)
    #plot_iteration(path, name, 1442, reference=data)
    #plot_iteration(path, name, 1455, reference=data)

    #values = get_metrics([1, 2, 3, 4], "All", 0, 0)
    #experiment_inspector.plot_subset(x, values)
    #values = get_count_tests(1, 1, None, 0)
    #experiment_inspector.plot_subset(x, values)
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

def __save_iterations(a, b, c, iteration):
    a.savefig("../../plots/Appendix/StatisticsIterationDetailed/" + "Demand" + str(iteration) + ".svg", format="svg")
    b.savefig("../../plots/Appendix/StatisticsIterationDetailed/" + "Time" + str(iteration) + ".svg", format="svg")
    c.savefig("../../plots/Appendix/StatisticsIterationDetailed/" + "Distance" + str(iteration) + ".svg", format="svg")

def make_stochastic_multiplication_plots():
    path = "\\\\ifv-fs\\User\\Abschlussarbeiten\\Robin.Andre\\Experimente\\Ergebnisse\\MyAlgorithmFullTwoPasses\\"
    #make_plots_for_showing_not_well_calibrated()
    #return
    name = "ImprovedDetailPasses100_Algo42"
    x = pandas.read_csv(path + name + ".csv")
    x["algorithm_seed"] = 100
    x["identifier"] = "Default"
    x = x.rename(columns=lambda col: col.strip())
    values = get_stochastic_tests(None, None, 0, 1)
    ks = get_p_row_analysis(x, values)
    values = get_stochastic_tests(None, None, 1, 1)
    ttest = get_p_row_analysis(x, values)
    values = get_stochastic_tests(None, None, 2, 1)
    ranksums = get_p_row_analysis(x, values)

    fig, ax = plt.subplots(1, 3, figsize=(6, 2))


    plot_frame = {"K-S": ks, "T-Test": ttest, "Wilcoxon": ranksums}
    plot_df = pandas.DataFrame(plot_frame)
    plot_df = plot_df.rolling(5, center=True, min_periods=1).mean()
    plot_df.plot(ax=ax[0])

    values = get_stochastic_tests(0, None, 0, 1)
    ks = get_p_row_analysis(x, values)
    values = get_stochastic_tests(0, None, 1, 1)
    ttest =get_p_row_analysis(x, values)
    values = get_stochastic_tests(0, None, 2, 1)
    ranksums = get_p_row_analysis(x, values)
    plot_frame = {"K-S": ks, "T-Test": ttest, "Wilcoxon": ranksums}
    plot_df = pandas.DataFrame(plot_frame)
    plot_df = plot_df.rolling(5, center=True, min_periods=1).mean()
    plot_df.plot(ax=ax[1])

    values = get_stochastic_tests(1, None, 0, 1)
    ks = get_p_row_analysis(x, values)
    values = get_stochastic_tests(1, None, 1, 1)
    ttest = get_p_row_analysis(x, values)
    values = get_stochastic_tests(1, None, 2, 1)
    ranksums = get_p_row_analysis(x, values)
    plot_frame = {"K-S": ks, "T-Test": ttest, "Wilcoxon": ranksums}
    plot_df = pandas.DataFrame(plot_frame)
    plot_df = plot_df.rolling(5, center=True, min_periods=1).mean()
    xshift = 0.8
    temp_descriptor = ["K-S", "T-Test", "Wilcoxon"]
    plot_df.plot(ax=ax[2])
    plt.tight_layout(rect=[0, 0.0, xshift, 1])
    ax[0].get_legend().remove()
    ax[1].get_legend().remove()
    ax[2].get_legend().remove()
    fig.legend(temp_descriptor, bbox_to_anchor=(xshift, 0.5), loc="center left")
    fig.show()
    fig.savefig("../../plots/multiplicative_statistics.svg", format="svg")

    reqs = ['workday', 'gender', 'employment', 'age', 'activityType',
            'tripMode', 'previousMode', 'economicalStatus', 'nominalSize', 'totalNumberOfCars']
    params = simulation.default_yaml().mode_config().get_all_parameter_names_on_requirements(reqs)
    d = Individual(seed=42, param_list=params)
    d.run()
    data = d.data
    a, b, c = plot_iteration(path, name, 423, reference=data)
    __save_iterations(a, b, c, 423)
    plot_iteration(path, name, 508, reference=data)
    a, b, c = plot_iteration(path, name, 546, reference=data)
    __save_iterations(a, b, c, 546)
    a, b, c = plot_iteration(path, name, 553, reference=data)
    __save_iterations(a, b, c, 553)
    a, b, c = plot_iteration(path, name, 933, reference=data)
    __save_iterations(a, b, c, 933)

    a, b, c = plot_iteration(path, name, 938, reference=data)
    __save_iterations(a, b, c, 938)
    a, b, c = plot_iteration(path, name, 1442, reference=data)
    __save_iterations(a, b, c, 1442)
    a, b, c = plot_iteration(path, name, 1455, reference=data)
    __save_iterations(a, b, c, 1455)

    #get_p_row_analysis(x, values, title="All Wilcoxons")
    #values = get_count_tests(2, 0, 0, 1)
    #get_p_row_analysis(x, values, title="Stochastic countiwl")
    #values = get_count_tests(2, 2, 0, 1)
    #get_p_row_analysis(x, values, title="Alll countiwl")
    #values = get_count_tests(2, 1, 0, 1)
    #get_p_row_analysis(x, values, title="None countiwl")

def make_stochastic_insignificance_plots():
    path = "\\\\ifv-fs\\User\\Abschlussarbeiten\\Robin.Andre\\Experimente\\Ergebnisse\\MyAlgorithmFullTwoPasses\\"
    #make_plots_for_showing_not_well_calibrated()
    #return
    name = "ImprovedDetailPasses100_Algo42"
    x = pandas.read_csv(path + name + ".csv")
    x["algorithm_seed"] = 100
    x["identifier"] = "Default"
    x = x.rename(columns=lambda col: col.strip())
    values = get_count_tests(3, 2, None, 1)
    experiment_inspector.plot_subset(x, values)
    values = get_count_tests(0, 2, None, 1)
    experiment_inspector.plot_subset(x, values)

def make_count_plots_of_run():
    path = "\\\\ifv-fs\\User\\Abschlussarbeiten\\Robin.Andre\\Experimente\\Ergebnisse\\MyAlgorithmFullTwoPasses\\"
    name = "ImprovedDetailPasses100_Algo42"
    x = pandas.read_csv(path + name + ".csv")
    x["algorithm_seed"] = 100
    x["identifier"] = "Default"
    x = x.rename(columns=lambda col: col.strip())
    temp_descriptor = ["Wilcoxon", "T-Test", "K-S"]
    for k, v in {"Zones": 0, "Distance": 1, "Demand": 2, "Time": 3}.items():
        fig, ax = plt.subplots(1, 3, sharex=True, sharey=True, figsize=(6, 2))
        xshift = 0.8
        plt.tight_layout(rect=[0, 0.03, xshift, 0.97])
        subset_slicer = slice(None, None, 40)
        values = get_count_tests(v, 1, None, 1)
        experiment_inspector.plot_subset(x, values, title=k, hide_legend=True, axinput=ax[0], slicer=subset_slicer, rename_iteration="$\emptyset$")
        if v != 2:
            values = get_count_tests(v, 0, None, 1)
            experiment_inspector.plot_subset(x, values, title=k, hide_legend=True, axinput=ax[1], slicer=subset_slicer, rename_iteration="$m$")
        else:
            values = get_count_tests(v, 0, [0, 2], 1)
            experiment_inspector.plot_subset(x, values, title=k, hide_legend=True, axinput=ax[1], slicer=subset_slicer, rename_iteration="$m$")
        values = get_count_tests(v, 2, None, 1)
        experiment_inspector.plot_subset(x, values, title=k, hide_legend=True, axinput=ax[2], slicer=subset_slicer, rename_iteration="$keys$")
        fig.legend(temp_descriptor, bbox_to_anchor=(xshift, 0.5), loc="center left")
        fig.suptitle(k)
        fig.show()
        fig.savefig("../../plots/CountStatistic_simulation_run" + k + ".svg", format="svg")

def __help_plot(x, label_list, color_list, s_slicer, temp_descriptor, smoothen, data_slicer, which_df_num=0, save_file=None):
    fig, ax = plt.subplots(1, 3, sharex=True, sharey=True, figsize=(6, 2))
    values = get_stochastic_tests(which_df_num, None, 0, 1)[s_slicer]
    experiment_inspector.plot_subset(x, values, rename_iteration="K-S", hide_legend=True, axinput=ax[0], legend_cols=label_list[s_slicer], title="K-S", color=color_list[s_slicer], slicer=data_slicer, smoothen=smoothen)
    values = get_stochastic_tests(which_df_num, None, 1, 1)[s_slicer]
    experiment_inspector.plot_subset(x, values, rename_iteration="T-Test", hide_legend=True, axinput=ax[1], legend_cols=label_list[s_slicer], title="T-Test", color=color_list[s_slicer], slicer=data_slicer, smoothen=smoothen)
    values = get_stochastic_tests(which_df_num, None, 2, 1)[s_slicer]
    experiment_inspector.plot_subset(x, values, rename_iteration="Wilcoxon", hide_legend=True, axinput=ax[2], legend_cols=label_list[s_slicer], title="Wilcoxon", color=color_list[s_slicer], slicer=data_slicer, smoothen=smoothen)
    xshift = 1
    plt.tight_layout(rect=[0, 0.0, 0.75, 1])
    fig.legend(temp_descriptor, bbox_to_anchor=(xshift, 0.5), loc="center right")
    fig.show()
    if save_file is not None:
        fig.savefig(save_file, format="svg")


def make_stochastic_mode_split_plots():
    path = "\\\\ifv-fs\\User\\Abschlussarbeiten\\Robin.Andre\\Experimente\\Ergebnisse\\MyAlgorithmFullTwoPasses\\"
    name = "ImprovedDetailPasses100_Algo42"
    x = pandas.read_csv(path + name + ".csv")
    x["algorithm_seed"] = 100
    x["identifier"] = "Default"
    x = x.rename(columns=lambda col: col.strip())
    data_slicer = slice(None, None, 2)
    s_slicer = slice(3, 6, None)
    label_list = visualization.label_modes(None, get_all_and_combined=True)
    color_list = visualization.color_modes(None, get_all_and_combined=True)
    smoothen = True
    s_slicer = slice(3, 6, None)
    temp_descriptor = ["Passenger", "Pedestrian", "Pub. Transp."]
    s = "../../plots/distribution_statistic_time_pub.svg"
    __help_plot(x, label_list, color_list, s_slicer, temp_descriptor, smoothen, data_slicer, save_file=s)
    s_slicer = slice(None, 3, None)
    temp_descriptor = ["All", "Bike", "Car"]
    s = "../../plots/distribution_statistic_time_car.svg"
    __help_plot(x, label_list, color_list, s_slicer, temp_descriptor, smoothen, data_slicer, save_file=s)

    s_slicer = slice(3, 6, None)
    temp_descriptor = ["Passenger", "Pedestrian", "Pub. Transp."]
    s = "../../plots/distribution_statistic_distance_pub.svg"
    __help_plot(x, label_list, color_list, s_slicer, temp_descriptor, smoothen, data_slicer, which_df_num=1, save_file=s)
    s_slicer = slice(None, 3, None)
    temp_descriptor = ["All", "Bike", "Car"]
    s = "../../plots/distribution_statistic_distance_car.svg"
    __help_plot(x, label_list, color_list, s_slicer, temp_descriptor, smoothen, data_slicer, which_df_num=1, save_file=s)
    return

    fig, ax = plt.subplots(1, 3, sharex=True, sharey=True, figsize=(6, 2))
    values = get_stochastic_tests(0, None, 0, 1)[s_slicer]
    experiment_inspector.plot_subset(x, values, rename_iteration="K-S", hide_legend=True, axinput=ax[0], legend_cols=label_list[s_slicer], title="K-S", color=color_list[s_slicer], slicer=data_slicer, smoothen=smoothen)
    values = get_stochastic_tests(0, None, 1, 1)[s_slicer]
    experiment_inspector.plot_subset(x, values, rename_iteration="T-Test", hide_legend=True, axinput=ax[1], legend_cols=label_list[s_slicer], title="T-Test", color=color_list[s_slicer], slicer=data_slicer, smoothen=smoothen)
    values = get_stochastic_tests(0, None, 2, 1)[s_slicer]
    experiment_inspector.plot_subset(x, values, rename_iteration="Wilcoxon", hide_legend=True, axinput=ax[2], legend_cols=label_list[s_slicer], title="Wilcoxon", color=color_list[s_slicer], slicer=data_slicer, smoothen=smoothen)

    xshift = 0.75
    plt.tight_layout(rect=[0, 0.0, xshift, 1])
    fig.legend(temp_descriptor, bbox_to_anchor=(xshift, 0.5), loc="center left")
    fig.show()

    values = get_stochastic_tests(1, None, 0, 1)[s_slicer]

    experiment_inspector.plot_subset(x, values, legend_cols=label_list[s_slicer], title="K-S", color=color_list[s_slicer], slicer=data_slicer, smoothen=smoothen)
    values = get_stochastic_tests(1, None, 1, 1)[s_slicer]
    experiment_inspector.plot_subset(x, values, legend_cols=label_list[s_slicer], title="T-Test", color=color_list[s_slicer], slicer=data_slicer, smoothen=smoothen)
    values = get_stochastic_tests(1, None, 2, 1)[s_slicer]
    experiment_inspector.plot_subset(x, values, legend_cols=label_list[s_slicer], title="Wilcoxon", color=color_list[s_slicer], slicer=data_slicer, smoothen=smoothen)



if __name__ == "__main__":
    #make_stochastic_insignificance_plots()
    #make_stochastic_multiplication_plots()
    #make_count_plots_of_run()
    #make_stochastic_mode_split_plots()
    main()