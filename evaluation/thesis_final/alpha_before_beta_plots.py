import math

import pandas
from matplotlib import pyplot as plt

from calibration.evolutionary.individual import Individual
from configurations import SPECS
from plotting_individual_errors import plot_main_asc_params, plot_main_beta_params
from plot_detailed_run import get_stochastic_tests, get_p_row_analysis, plot_iteration, get_metrics, get_modal_metrics
from experiment_inspector import plot_subset, pad_iterations

METRICS = ["sum_squared_error", "mean_absolute_error", "mean_average_error",
           "root_mean_squared_error", "theils_inequality", "sum_squared_percent_error",
           "mean_sum_squared_error", "sum_cubed_error"]
COLORS = ["#e41a1c", "#377eb8", "#4daf4a", "#984ea3", "#ff7f00", "#ffff33"]


# COLORS = ["#1f77b4", "#ff7f0e"]
def get_color_from_label(label):
    d = {
        "Alpha": COLORS[0],
        "Beta": COLORS[1]
    }
    return d[label]


def plot_multiplicative_per_id(df, legend_cols=None, make_both_best_and_current=False, hide_legend=False, title=None,
                               test_set_num=None, metric_num=0, cur_or_best=0, slicer=None, areacol=None, axinput=None,
                               rename_iteration=None, smoothen=False, special_colors=None):
    temp = df

    if rename_iteration is not None:
        temp = temp.rename(columns={"iteration": rename_iteration})
        iter_identifier = rename_iteration
    else:
        iter_identifier = "iteration"
    wololo = pad_iterations(temp, iter_identifier)

    temp = wololo.groupby([iter_identifier, "identifier"]).mean()
    temp = temp.groupby("identifier")
    if axinput is None:
        fig, ax = plt.subplots(figsize=(8, 6))
    else:
        ax = axinput
    if areacol is not None:
        ax.axhspan(0, areacol, facecolor="green", alpha=0.2)

    # ax.axhline(y=159548)
    for i, (label, df) in enumerate(temp):
        df = df.droplevel("identifier")
        if legend_cols is not None:
            df.columns = legend_cols
        else:
            pass
            # df = df.rename(columns={columns_list[0]: label})
        print(f"{i} {label}")
        if slicer is not None:
            df = df.iloc[slicer, :]
        if smoothen:
            df = df.rolling(5, center=True, min_periods=1).mean()

        if make_both_best_and_current:
            values1 = get_stochastic_tests(test_set_num, None, metric_num, 0)

            plot_series1 = get_p_row_analysis(df, values1)

            values2 = get_stochastic_tests(test_set_num, None, metric_num, 1)

            plot_series2 = get_p_row_analysis(df, values2)
            plot_df = pandas.DataFrame({label + "_opt": plot_series1, label + "": plot_series2})

            styles = ["-", "--"]
            if special_colors is not None:
                colors = [special_colors[i], special_colors[i]]
            else:
                colors = [COLORS[i], COLORS[i]]
        else:
            values = get_stochastic_tests(test_set_num, None, metric_num, cur_or_best)
            ks = get_p_row_analysis(df, values)
            plot_df = pandas.DataFrame({label: ks})
            styles = ["-"]
            if special_colors is not None:
                colors = [special_colors[i]]
            else:
                colors = [COLORS[i]]

        plot_df.plot(ax=ax, style=styles, color=colors)

    if hide_legend:
        ax.get_legend().remove()
    if axinput is None:
        fig.suptitle(title)
        fig.show()
        return fig
    return


def plot_param_errors(plot_dir, keyword="", exp_dir="tuningAlphabeforeBeta", identifiers=["BetaBeforeAlpha", "AlphaBeforeBeta"], figsize=(6, 3), supplement="", dirpath="C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\", override_path=None):
    target_seed = "100"
    algo_seed = "42"
    plotx, ploty = get_grid_from_inp_length(len(identifiers))
    fig, ax = plt.subplots(plotx, ploty, sharey=True, figsize=figsize)

    if len(identifiers) == 1:
        ax = [ax]
    else:
        ax = ax.flatten()
    for i, id in enumerate(identifiers):
        if override_path is None:
            path = dirpath + exp_dir + "\\csv\\" + id + supplement + target_seed + "_Algo" + algo_seed + "parameter_list.csv"
        else:
            path = override_path
        df = pandas.read_csv(path)
        plot_main_asc_params(df, ax=ax[i])
        ax[i].set_xlabel(id)
        ax[i].get_legend().remove()

    plt.tight_layout()
    fig.legend(["$\\alpha^{bike}$", "$\\alpha^{car}$", "$\\alpha^{pass}$", "$\\alpha^{ped}$", "$\\alpha^{pub}$"]
                   , bbox_to_anchor=(1, 0.5), loc="center left")
    fig.show()
    fig.savefig("../../plots/"+ plot_dir +"/AlphaComparison" + keyword + ".svg", format="svg", bbox_inches="tight")
    plotx, ploty = get_grid_from_inp_length(len(identifiers))
    fig, ax = plt.subplots(plotx, ploty, sharey=True, figsize=figsize)

    if len(identifiers) == 1:
        ax = [ax]
    else:
        ax = ax.flatten()
    for i, id in enumerate(identifiers):
        if override_path is None:
            path = dirpath + exp_dir + "\\csv\\" + id + supplement + target_seed + "_Algo" + algo_seed + "parameter_list.csv"
        else:
            path = override_path
        df = pandas.read_csv(path)
        plot_main_beta_params(df, ax=ax[i])
        ax[i].set_xlabel(id)
        ax[i].get_legend().remove()
    plt.tight_layout()
    fig.legend(["$\\beta^{bike}$", "$\\beta^{car}$", "$\\beta^{pass}$", "$\\beta^{ped}$", "$\\beta^{pub}$"]
                , bbox_to_anchor=(1, 0.5), loc="center left")
    fig.show()
    fig.savefig("../../plots/" + plot_dir +"/BetaComparison"+ keyword +".svg", format="svg", bbox_inches="tight")


def plot_special_iteration():
    params = ["asc_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "asc_bike_mu", "b_tt_car_p_mu",
              "b_tt_car_d_mu", "b_tt_put_mu", "b_tt_bike_mu", "b_tt_ped"]
    d = Individual(seed=42, param_list=params)
    d.run()
    data = d.data
    path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\tuningAlphabeforeBeta\\csv\\AlphaBeforeBeta100_Algo42parameter_list.csv"

    a, b, c = plot_iteration(path, name, 423, reference=data)


def plot_multi(csv_name, plot_dir, legend=None, plot_cur=True, special_colors=None):
    x = csv_name

    for name, set_number in [("All", None), ("Distance", 1), ("Time", 0)]:
        fig, ax = plt.subplots(1, 2, figsize=(6, 3))
        plot_multiplicative_per_id(x, test_set_num=set_number, axinput=ax[0], make_both_best_and_current=plot_cur,
                                   rename_iteration="K-S", special_colors=special_colors)
        plot_multiplicative_per_id(x, test_set_num=set_number, axinput=ax[1], metric_num=2,
                                   make_both_best_and_current=plot_cur, rename_iteration="Wilcoxon", special_colors=special_colors)
        ax[0].get_legend().remove()
        ax[1].get_legend().remove()
        handles, labels = ax[1].get_legend_handles_labels()
        plt.tight_layout()
        #plt.tight_layout(rect=[0, 0.0, 0.85, 1])
        print(f"Legend {labels}")
        if legend is not None:
            labels = legend
        fig.legend(handles, labels, bbox_to_anchor=(1, 0.5), loc="center left")
        fig.show()
        fig.savefig("../../plots/" + plot_dir + "/Stochastic_Test_" + name + ".svg", format="svg", bbox_inches="tight")
    return
    plot_multiplicative_per_id(x, cur_or_best=0, rename_iteration="K-S Best-Metric")
    plot_multiplicative_per_id(x, cur_or_best=1, rename_iteration="K-S Current")
    plot_multiplicative_per_id(x, metric_num=2, cur_or_best=0, rename_iteration="Wilcoxon Best-Metric")
    plot_multiplicative_per_id(x, metric_num=2, cur_or_best=1, rename_iteration="Wilcoxon Current")


def int_to_metric_name(num):
    d = {
        0: "Sum of squared error",
        1: "mean_absolute_error",
        2: "mean_average_error",
        3: "mean_average_error",
        4: "Theils Inequality",
        5: "sum_squared_percent_error",
        6: "Mean Sum Squared error",
        7: "Sum Cubed error",
    }
    return d[num]

def get_grid_from_inp_length(num):
    a = math.ceil(math.sqrt(num))
    b = math.ceil(num / a)
    print(a)
    return b, a

def __help_plots(x, refs, values, metric_tuple, plot_dir, savestring, string_addendum, figsize,
                 optional_names=None, no_area_col=False, special_colors=None, legend=None, override_grid=None):
    metrics = values
    if override_grid is None:
        plotx, ploty = get_grid_from_inp_length(len(metrics))
    else:
        plotx, ploty = override_grid
    fig, ax = plt.subplots(plotx, ploty, figsize=figsize)
    if optional_names is not None:
        names = optional_names
    else:
        names = [int_to_metric_name(x) for x in metric_tuple[2]]
    if special_colors is not None:
        colors = special_colors
    else:
        colors = COLORS[:len(x.columns)]


    if len(metrics) == 1:
        ax = [ax]
    else:
        ax = ax.flatten()
    for a, metric, name in zip(ax, metrics, names):
        reference = "_".join(metric.split("_")[:-1])
        print(reference)
        areacol = refs[reference]["max"]
        # metric_current = "TravelTime_All_" + metric + "_current"

        if metric.__contains__("_All_") or metric.__contains__("_Detailed_") or no_area_col:
            plot_subset(x, [metric], axinput=a, rename_iteration=name, color=colors)
        else:
            plot_subset(x, [metric], areacol=areacol, axinput=a, rename_iteration=name, color=colors)
    plt.tight_layout()
    handles, labels = ax[0].get_legend_handles_labels()
    print(f"Legend {labels}")
    for a in ax:
        if a.get_legend() is not None:
            a.get_legend().remove()
    if legend is not None:
        labels = legend
    fig.legend(handles, labels, bbox_to_anchor=(1, 0.5), loc="center left")




    fig.show()
    fig.savefig("../../plots/" + plot_dir + "/" + savestring + "_MetricEvaluation" + string_addendum + ".svg", format="svg", bbox_inches="tight")


def alpha_before_beta(csv_name, plot_dir, metric_tuple=(0, 0, [0, 4]), func=get_metrics, savestring="", figsize=(6,3),
                      opt_names=None, special_colors=None, legend=None, override_grid=None):
    # path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\tuningAlphabeforeBeta\\"
    # make_directory_of_csvs_into_one_big_csv(path, "AlphaBeforeBeta", "Before")

    x = csv_name

    refs = pandas.read_csv(SPECS.EXP_PATH_LOCAL + "TargetArea002.csv", index_col=0)
    print(refs)
    values = func(metric_tuple[0], metric_tuple[1], metric_tuple[2], 0)
    __help_plots(x, refs, values, metric_tuple, plot_dir, savestring, "Best", figsize=figsize,
                 optional_names=opt_names, special_colors=special_colors, legend=legend, override_grid=override_grid)
    values = func(metric_tuple[0], metric_tuple[1], metric_tuple[2], 1)
    __help_plots(x, refs, values, metric_tuple, plot_dir, savestring, "Current", figsize=figsize,
                 optional_names=opt_names, special_colors=special_colors, legend=legend, override_grid=override_grid)
    print(values)
    # metrics = ["sum_squared_error", "theils_inequality"]



def get_csv(csv_name):
    path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\CSV_CONCATENATED\\"
    if type(csv_name) is list:
        df_list = []
        for file in csv_name:
            df_list.append(pandas.read_csv(path + file))
        df = pandas.concat(df_list)
        return df
    else:
        df = pandas.read_csv(path + csv_name)
        return df


def plot_convenience(csv_name, plot_dir, legend):
    csv = get_csv(csv_name)
    plot_multi(csv, plot_dir, legend)

    alpha_before_beta(csv, plot_dir)


def plot_dest(csv_name, plot_dir, legend):
    csv = get_csv(csv_name)
    plot_multi(csv, plot_dir, legend, plot_cur=False)

    #alpha_before_beta(csv, plot_dir, metric_tuple=(5, 0, [0, 4]))
    alpha_before_beta(csv, plot_dir, metric_tuple=(0, 1, [0, 4]), savestring="TravelTime")
    alpha_before_beta(csv, plot_dir, metric_tuple=(1, 1, [0, 4]), savestring="Demand")
    alpha_before_beta(csv, plot_dir, metric_tuple=(4, 1, [0, 4]), savestring="Demand60")
    alpha_before_beta(csv, plot_dir, metric_tuple=(0, 0, [0, 4]), func=get_modal_metrics)


def make_csvs(int_list):
    csv_ids = {
        0: "pygad_10_parameters_target_has_same_seed.csv",
        1: "pygad_10_parameters_target_has_same_seed_time_metric.csv",
        2: "pygad_main_destination_same_seed.csv",
        3: "pygad_main_destination_same_seed_plus_all.csv",
        4: "pygad_main_destination_same_seed_plus_business.csv",
        5: "pygad_main_mode_all_parameters.csv",
        6: "pyswarms_10_parameters_target_has_same_seed.csv",
        7: "pyswarms_10_parameters_target_has_same_seed_time_metric.csv",
        8: "pyswarms_main_destination_same_seed.csv",
        9: "pyswarms_main_destination_same_seed_plus_all.csv",
        10: "pyswarms_main_destination_same_seed_plus_business.csv",
        11: "pyswarms_main_mode_all_parameters.csv",
        12: "spsa_10_parameters_target_has_same_seed.csv",
        13: "spsa_main_destination_same_seed.csv",
        14: "spsa_main_destination_same_seed_plus_all.csv",
        15: "spsa_main_destination_same_seed_plus_business.csv",
        16: "spsa_main_mode_all_parameters.csv",
        17: "MyAlgorithmFullMode.csv",
        18: "MyAlgorithmFullTwoPasses.csv",
        19: "MyAlgorithmFullTwoPassesNewSetWithTargetSeed.csv",
        20: "pyswarms_10_parameters_target_has_same_seed_time_metric2.csv",
        21: "pygad_10_parameters_target_has_same_seed_time_metric2.csv",
        22: "spsa_10_parameters_target_has_same_seed_time_metric2.csv",
        23: "AlphaBeforeBeta.csv",
        24: "QuantileDistributionExperiment.csv",
        25: "BetterBoundEstimation.csv",
        26: "MyExperimentVariableQuantilesCostFixedOutput.csv",
        27: "MyExperimentVariableQuantilesFixedOutput.csv",
        28: "MyExperimentVeryHighPrecision.csv",
        29: "RecreatingTuningProcess.csv",
        30: "MyAlgorithmFullTwoPassesNoMinMax.csv"

    }
    csvs = []
    for i in int_list:
        csvs.append(csv_ids[i])
    return csvs

def plot_experiment_compare_full_set_mode():
    csv = get_csv(make_csvs([5, 11, 16, 17]))
    plot_dir = "ModeMain"
    legend = ["Algo", "GA", "SPSA", "Swarm"]
    plot_multi(csv, plot_dir, legend, plot_cur=False)

    #alpha_before_beta(csv, plot_dir, metric_tuple=(5, 0, [0, 4]))
    alpha_before_beta(csv, plot_dir, metric_tuple=(0, 1, [0, 4]), savestring="TravelTime")
    alpha_before_beta(csv, plot_dir, metric_tuple=(0, 0, [0, 4]), savestring="TravelTimeOptimizedMetric")
    alpha_before_beta(csv, plot_dir, metric_tuple=(1, 1, [0, 4]), savestring="Demand")
    alpha_before_beta(csv, plot_dir, metric_tuple=(4, 1, [0, 4]), savestring="Demand60")
    alpha_before_beta(csv, plot_dir, metric_tuple=(0, 0, [0, 4]), func=get_modal_metrics, savestring="Modal")

def plot_comparison_seed_no_seed():
    #csv = get_csv(make_csvs([7, 20])) #Swarms
    #csv = get_csv(make_csvs([12, 22])) # SPSA
    csv = get_csv(make_csvs([1, 21])) # Pygad
    csv = get_csv(make_csvs([1,7, 20, 21]))
    plot_dir = "Temp"
    legend = ["GA+", "GA", "Swarm+", "Swarm"]
    colors = ["#00ff00", "#ff0000", "#000000", "#ffff00"]
    plot_multi(csv, plot_dir, legend, plot_cur=False, special_colors=colors)
    alpha_before_beta(csv, plot_dir, metric_tuple=([0, 1, 2, 3, 4, 5], 1, [4]), savestring="TravelTime", figsize=(9, 6),
                      special_colors=colors,
                      opt_names=["Time", "Demand", "Demand5", "Demand15", "Demand60", "Distance"])
    names = ["All", "Default", "None", "AllC", "DefaultC", "NoneC"]
    alpha_before_beta(csv, plot_dir, metric_tuple=([0, 1], [0, 1, 2], [4]), savestring="TravelTime2", figsize=(6, 4), opt_names=names)

def plot_alpha_before_beta():
    """
    Makes the plots for the Alpha Beta Experiment Evaluation
    """
    csv = get_csv(make_csvs([23]))
    plot_dir = "AlphaBetaNew"
    plot_multi(csv, plot_dir, ["A$_{opt}$", "A", "B$_{opt}$", "B"])
    alpha_before_beta(csv, plot_dir, metric_tuple=(0, 1, [0, 4]), savestring="TravelTime")
    alpha_before_beta(csv, plot_dir, metric_tuple=(0, 0, [0, 4]), func=get_modal_metrics, savestring="ModalSplit")
    plot_param_errors(plot_dir)

def plot_quantiles_experiment():
    csv = get_csv(make_csvs([24]))
    plot_dir = "QuantileExperimentNew"
    legend = ["100", "99+", "50", "25"]
    plot_multi(csv, plot_dir, legend, plot_cur=False)
    alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(0, 1, [0, 4]), savestring="TravelTime")
    alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(0, 0, [0, 4]), func=get_modal_metrics, savestring="ModalSplit")
    plot_param_errors(plot_dir, "", exp_dir="MyExperimentQuantiles", identifiers=list(set(csv["identifier"])))

def plot_heuristics_mode_subset_time():
    csv = get_csv(make_csvs([1, 7]))
    plot_dir = "MetaHeuristicModeSubset"
    legend = ["GA", "Swarm"]
    plot_multi(csv, plot_dir, legend, plot_cur=False)
    alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(0, 1, [0, 4]), savestring="TravelTime")
    alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(0, 0, [0, 4]), func=get_modal_metrics, savestring="ModalSplit")
    #plot_param_errors(plot_dir, "", exp_dir="MyExperimentQuantiles", identifiers=list(set(csv["identifier"])))

def plot_heuristics_mode_subset_time_modal():
    csv = get_csv(make_csvs([0, 6, 12]))
    plot_dir = "MetaHeuristicModeSubsetModal"
    legend = ["GA", "SPSA", "Swarm"]
    plot_multi(csv, plot_dir, legend, plot_cur=False)
    alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(0, 1, [0, 4]), savestring="TravelTime")
    alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(0, 0, [0, 4]), func=get_modal_metrics, savestring="ModalSplit")
    #plot_param_errors(plot_dir, "", exp_dir="MyExperimentQuantiles", identifiers=list(set(csv["identifier"])))

def plot_heuristics_mode_subset_compare_ga():
    csv = get_csv(make_csvs([0, 1]))
    plot_dir = "MetaHeuristicModeSubsetMetricComparison"
    legend = ["GA-Modal", "GA-Time"]
    plot_multi(csv, plot_dir, legend, plot_cur=False)
    alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(0, 1, [0, 4]), savestring="TravelTime")
    alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(0, 0, [0, 4]), func=get_modal_metrics, savestring="ModalSplit")
    #plot_param_errors(plot_dir, "", exp_dir="MyExperimentQuantiles", identifiers=list(set(csv["identifier"])))


def plot_second_meta_heuristic_run():
    csv = get_csv(make_csvs([20, 21, 22]))
    plot_dir = "MetaHeuristicModeSubsetSecondRun"
    legend = ["GA", 'SPSA', 'Swarm']
    #plot_multi(csv, plot_dir, legend, plot_cur=False)


    alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(0, 1, [0, 4]), savestring="TravelTime")
    alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(0, 0, [0, 4]), func=get_modal_metrics,
                      savestring="ModalSplit")

def plot_seed_impact_on_ga():
    csv = get_csv(make_csvs([1, 21]))
    plot_dir = "MetaHeuristicSeedImpactGA"
    legend = ["GA+R", "GA"]
    plot_multi(csv, plot_dir, legend, plot_cur=False)
    alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(0, 1, [0, 4]), savestring="TravelTime")
    alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(0, 0, [0, 4]), func=get_modal_metrics,
                      savestring="ModalSplit")
    optnames = ["Time", "Demand", "Demand 5", "Demand 15", "Demand 60", "Distance"]
    alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=([0, 1, 2, 3, 4, 5], 1, [4]),
                      savestring="AllDfs", opt_names=optnames, figsize=(9, 6))

def plot_destination_main_only():
    csv = get_csv(make_csvs([2, 8, 13]))
    plot_dir = "DestinationMain"
    legend = ["GA", 'SPSA', 'Swarm']
    plot_multi(csv, plot_dir, legend, plot_cur=False)



    #alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(0, 1, [0, 4]), savestring="TravelTime")
    #alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(1, 1, [0, 4]), savestring="Demand")
    #alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(4, 1, [0, 4]), savestring="Demand60")
    #alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(0, 0, [0, 4]), func=get_modal_metrics, savestring="ModalSplit")
    optnames = ["All", "m", "$\emptyset$"]
    alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(5, [0, 1, 2], [4]),
                      savestring="DistanceAll", opt_names=optnames, override_grid=(1, 3), figsize=(9, 3))

def plot_destination_main_plus_business():
    csv = get_csv(make_csvs([4, 10, 15]))
    plot_dir = "DestinationMainBusiness"
    legend = ["GA", 'SPSA', 'Swarm']
    plot_multi(csv, plot_dir, legend, plot_cur=False)



    #alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(0, 1, [0, 4]), savestring="TravelTime")
    #alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(1, 1, [0, 4]), savestring="Demand")
    #alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(4, 1, [0, 4]), savestring="Demand60")
    #alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(0, 0, [0, 4]), func=get_modal_metrics, savestring="ModalSplit")
    optnames = ["All", "m", "$\emptyset$"]
    alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(5, [0, 1, 2], [4]),
                      savestring="DistanceAll", opt_names=optnames, override_grid=(1, 3), figsize=(9, 3))

def plot_destination_main_plus_all():
    csv = get_csv(make_csvs([3, 9, 14]))
    plot_dir = "DestinationMainAll"
    legend = ["GA", 'SPSA', 'Swarm']
    plot_multi(csv, plot_dir, legend, plot_cur=False)



    #alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(0, 1, [0, 4]), savestring="TravelTime")
    #alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(1, 1, [0, 4]), savestring="Demand")
    #alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(4, 1, [0, 4]), savestring="Demand60")
    #alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(0, 0, [0, 4]), func=get_modal_metrics, savestring="ModalSplit")
    optnames = ["All", "m", "$\emptyset$"]
    alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(5, [0, 1, 2], [4]),
                      savestring="DistanceAll", opt_names=optnames, override_grid=(1, 3), figsize=(9, 3))

def plot_destination_main_comparison():
    csv = get_csv(make_csvs([2, 3, 4]))
    plot_dir = "DestinationMainComparison"
    legend = ["GA", 'GA+A', 'GA+B']
    plot_multi(csv, plot_dir, legend, plot_cur=False)
    #alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(0, 1, [0, 4]), savestring="TravelTime")
    #alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(1, 1, [0, 4]), savestring="Demand")
    #alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(4, 1, [0, 4]), savestring="Demand60")
    #alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(0, 0, [0, 4]), func=get_modal_metrics, savestring="ModalSplit")
    optnames = ["All", "m", "$\emptyset$"]
    alpha_before_beta(csv, plot_dir, legend=legend, metric_tuple=(5, [0, 1, 2], [4]),
                      savestring="DistanceAll", opt_names=optnames, override_grid=(1, 3), figsize=(9, 3))


def plot_mode_subset_comparison():
    plot_dir = "ModeSubset"
    legend = ["GA", "Algo", "Swarm"]
    csv = get_csv(make_csvs([28, 20, 21]))
    colors = ["#ff0000", "#00ff00", "#0000ff"]
    plot_multi(csv, plot_dir, legend, plot_cur=False, special_colors=colors)
    legend = ["GA", "Algo", "SPSA", "Swarm"]
    colors = ["#ff0000", "#00ff00", "#000000", "#0000ff"]
    csv = get_csv(make_csvs([28, 20, 21, 22]))


    #plot_multi(csv, plot_dir, legend, plot_cur=False)

    #alpha_before_beta(csv, plot_dir, metric_tuple=(5, 0, [0, 4]))
    alpha_before_beta(csv, plot_dir, special_colors=colors, legend=legend,  metric_tuple=(0, 1, [0, 4]), savestring="TravelTime")
    alpha_before_beta(csv, plot_dir, special_colors=colors, legend=legend, metric_tuple=(0, 0, [0, 4]), savestring="TravelTimeOptimizedMetric")
    alpha_before_beta(csv, plot_dir, special_colors=colors,legend=legend,  metric_tuple=(1, 1, [0, 4]), savestring="Demand")
    alpha_before_beta(csv, plot_dir, special_colors=colors,legend=legend,  metric_tuple=(4, 1, [0, 4]), savestring="Demand60")
    alpha_before_beta(csv, plot_dir, special_colors=colors,legend=legend,  metric_tuple=(0, 0, [0, 4]), func=get_modal_metrics, savestring="Modal")

def __plot_my_component(num, plot_dir, legend, expdir, supplement, skip_param_errors=False):
    csv = get_csv(make_csvs([num]))

    plot_multi(csv, plot_dir, legend)
    alpha_before_beta(csv, plot_dir, metric_tuple=(0, 1, [0, 4]), savestring="TravelTime")
    alpha_before_beta(csv, plot_dir, metric_tuple=(0, 0, [0, 4]), func=get_modal_metrics, savestring="ModalSplit")
    if not skip_param_errors:
        plot_param_errors(plot_dir, exp_dir=expdir, identifiers=list(set(csv["identifier"])), supplement=supplement)

def plot_component_test_minmax():
    __plot_my_component(25, "ComponentMinmax", ["?", "!"], "MyExperimentBetterErrorGuessing", "BetterBounds")

def plot_component_quantiles_cost():
    __plot_my_component(26, "ComponentVarQuantilesCost", ["?", "!"], "MyExperimentVariableQuantilesCostFixedOutput", "", skip_param_errors=True)

def plot_component_quantiles():
    __plot_my_component(27, "ComponentVarQuantiles", ["?", "!"], "MyExperimentVariableQuantilesFixedOutput", "")


def plot_mode_main_my_algorithm_comparison():
    csv = get_csv(make_csvs([17, 19, 30]))
    plot_dir = "MyAlgorithmComparison"
    legend = ['Algo', 'Algo2Passes', 'Algo2PassesNoMinMax']
    plot_multi(csv, plot_dir, legend, plot_cur=False)

    #alpha_before_beta(csv, plot_dir, metric_tuple=(5, 0, [0, 4]))
    alpha_before_beta(csv, plot_dir, legend=legend,  metric_tuple=(0, 1, [0, 4]), savestring="TravelTime")
    alpha_before_beta(csv, plot_dir,legend=legend, metric_tuple=(0, 0, [0, 4]), savestring="TravelTimeOptimizedMetric")
    alpha_before_beta(csv, plot_dir,legend=legend, metric_tuple=(1, 1, [0, 4]), savestring="Demand")
    alpha_before_beta(csv, plot_dir,legend=legend, metric_tuple=(4, 1, [0, 4]), savestring="Demand60")
    alpha_before_beta(csv, plot_dir,legend=legend, metric_tuple=(0, 0, [0, 4]), func=get_modal_metrics, savestring="Modal")


def plot_only_mine():
    csv = get_csv(make_csvs([17]))
    plot_dir = "Temp"
    legend = ["Algo"]
    plot_multi(csv, plot_dir, legend, plot_cur=True)
    plot_param_errors("Temp", override_path=r"\\ifv-fs\User\Abschlussarbeiten\Robin.Andre"
                                            r"\Experimente\Ergebnisse\MyAlgorithmFullTwoPasses\csv\ImprovedDetailPasses100_Algo42parameter_list")


def plot_external_errors():
    plot_param_errors("Temp", identifiers=["MAIN"], override_path=r"\\ifv-fs\User\Abschlussarbeiten\Robin.Andre"
                                            r"\Experimente\Ergebnisse\MyAlgorithmFullTwoPasses\csv\ImprovedDetailPasses100_Algo42parameter_list.csv")

def plot_recreation_experiment():
    csv = get_csv(make_csvs([17, 29]))
    plot_dir = "Recreation"
    legend = ["Default Start", "BrokenStartAll", "BrokenStartOnlySubset"]
    plot_multi(csv, plot_dir, legend, plot_cur=False)
    alpha_before_beta(csv, plot_dir, legend=legend,  metric_tuple=(0, 1, [0, 4]), savestring="TravelTime")
    alpha_before_beta(csv, plot_dir,legend=legend, metric_tuple=(0, 0, [0, 4]), savestring="TravelTimeOptimizedMetric")
    alpha_before_beta(csv, plot_dir,legend=legend, metric_tuple=(1, 1, [0, 4]), savestring="Demand")
    alpha_before_beta(csv, plot_dir,legend=legend, metric_tuple=(4, 1, [0, 4]), savestring="Demand60")
    alpha_before_beta(csv, plot_dir,legend=legend, metric_tuple=(0, 0, [0, 4]), func=get_modal_metrics, savestring="Modal")

if __name__ == "__main__":
    #plot_external_errors()
    #plot_recreation_experiment()
    #plot_alpha_before_beta()
    #plot_quantiles_experiment()
    #plot_component_test_minmax()
    #plot_component_quantiles_cost()
    #plot_component_quantiles()

    """This section is the evaluation of my own algorithmic components"""

    plot_mode_main_my_algorithm_comparison()

    #plot_heuristics_mode_subset_time()
    #plot_heuristics_mode_subset_time_modal()
    #plot_heuristics_mode_subset_compare_ga()
    #plot_seed_impact_on_ga()
    #plot_second_meta_heuristic_run()
    #plot_experiment_compare_full_set_mode()
    #plot_destination_main_only()
    #plot_destination_main_plus_business()
    #plot_destination_main_plus_all()
    #plot_destination_main_comparison()
    #plot_mode_subset_comparison()
    exit(0)
    #    plot_dest(["pyswarms_main_destination_same_seed.csv", "spsa_main_destination_same_seed.csv", "pygad_main_destination_same_seed.csv"], "Temp", ["?", "?", "?", "?"])

    #plot_dest(make_csvs([4, 10, 15]), "Temp", ["GA", "SPSA", "Swarm"])
    #plot_dest(make_csvs([2, 8, 13]), "Temp", ["GA", "SPSA", "Swarm"])
    #plot_dest(make_csvs([3, 9, 14]), "Temp", ["?", "?", "?", "?"])
    #plot_dest(make_csvs([17, 18, 19]), "Temp", ["Algo", "Algo2PassesOld", "Algo2Passes"])
    #plot_only_mine()
    #plot_experiment_compare_full_set_mode()
    plot_comparison_seed_no_seed()
    exit(0)
    plot_dest(make_csvs([5, 11, 16, 17]), "Temp", ["Algo", "GA", "SPSA", "Swarm"])
    exit(0)
    plot_dest(["pygad_main_destination_same_seed_plus_all.csv", "pygad_main_destination_same_seed_plus_business.csv",
               "pygad_main_destination_same_seed.csv"], "Temp", ["?", "?", "?", "?"])
    plot_dest(["pygad_main_destination_same_seed_plus_all.csv", "pygad_main_destination_same_seed_plus_business.csv",
               "pygad_main_destination_same_seed.csv"], "Temp", ["?", "?", "?", "?"])
    # alpha_before_beta("AlphaBeforeBeta.csv", "AlphaBeta")
    # exit(0)
    # plot_param_errors()
    # plot_multi("AlphaBeforeBeta.csv", "AlphaBeta", ["A$_{opt}$", "A", "B$_{opt}$", "B"])#
    # plot_multi("QuantileDistributionExperiment.csv", "QuantileExperiment", ["100", "+99", "50", "3"], plot_cur=False)
    # alpha_before_beta("QuantileDistributionExperiment.csv", "QuantileExperiment")
    # plot_convenience("QuantileDistributionExperiment.csv", "QuantileExperiment")
    # plot_convenience("BetterBoundEstimation.csv", "BoundEstimation", ["Fix", "FixCur", "Vari", "VariCur"])
    # plot_convenience("MyExperimentVariableQuantilesCostFixedOutput.csv", "VariableQuantilesCostFixed", ["?", "?", "?", "?"])
    # plot_convenience("MyExperimentVariableQuantilesFixedOutput.csv", "VariableQuantilesFixed",
    #                 ["?", "?", "?", "?"])

    # plot_convenience("MyExperimentVeryHighPrecision.csv", "HighPrecision",
    #                 ["?", "?", "?", "?"])
    # alpha_before_beta("AlphaBeforeBeta.csv", "AlphaBeta")
    plot_param_errors("Temp", "gettabot")
    plot_param_errors("Temp", "", exp_dir="MyExperimentQuantiles", identifiers=["HundredQuantiles", "QuantilesFocusOnLong", "SimpleQuantile", "ThreeQuantiles"], figsize=(6,6))