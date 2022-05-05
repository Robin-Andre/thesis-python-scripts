import difflib
import math

import numpy
import pandas
from matplotlib import pyplot as plt

from configurations import SPECS

METRICS = ["sum_squared_error", "mean_absolute_error", "mean_average_error",
           "root_mean_squared_error", "theils_inequality", "sum_squared_percent_error",
           "mean_sum_squared_error", "sum_cubed_error"]
DATAFRAMES = ["TravelTime", "TrafficDemand", "TrafficDemand5min", "TrafficDemand15min", "TrafficDemand60min",
              "TravelDistance", "ZoneDemand"]
SPECIALIZATIONS = ["All", "Default", "None"]
MODAL_SPLIT_DFS = ["ModalSplit_Default", "ModalSplit_Detailed"]
MODAL_SPLIT_SPECS = ["Splits", "Counts"]

COUNTS_STATS = ["Destinations", "TravelDistance", "TrafficDemand", "TravelTime"]
COUNT_STAT_SPECS = ["default", "aggegated_none", "all"]
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
        if x in name_list:
            return [x]
        else:
            return difflib.get_close_matches(x, name_list)
    return list(name_list[i] for i in x)


def get_metrics(dfname=None, spec=None, funcs=None):
    dfname = get_vals(dfname, DATAFRAMES)
    spec = get_vals(spec, SPECIALIZATIONS)
    funcs = get_vals(funcs, METRICS)
    ret_list = []
    for df in dfname:
        for s in spec:
            for func in funcs:
                ret_list.append(df + "_" + s + "_" + func)

    return ret_list


def get_modal_metrics(dfname=None, spec=None, funcs=None):
    dfname = get_vals(dfname, MODAL_SPLIT_DFS)
    spec = get_vals(spec, MODAL_SPLIT_SPECS)
    funcs = get_vals(funcs, METRICS)

    ret_list = []
    for df in dfname:
        for s in spec:
            for func in funcs:
                ret_list.append(df + "_" + s + "_" + func)

    return ret_list


"""Copied because import failed and it annoyed me """


def get_subset_on_identifier(df, idf):
    appropriate_test = df.columns.str.contains(idf)
    appropriate_non = ~df.columns.str.contains("TrafficDemand")

    a = df.columns[numpy.logical_and(appropriate_test, appropriate_non)]
    return df[a]


def make_statistic_box_plot(csv, idf):
    __helper(csv, idf, slice(None, 36, None))


def make_distribution_box_plot(csv, idf):
    __helper(csv, idf, slice(36, None, None))


def __helper(csv, idf, slice):
    stat_csv = csv.iloc[:, 202:]
    stat_csv = stat_csv.iloc[:, slice]
    # stat_csv = get_subset_on_identifier(stat_csv, idf)
    fig, ax = plt.subplots()
    ax.boxplot(stat_csv, showfliers=False)
    fig.show()


def get_subset_with_stats(csv, slice):
    temp = csv.iloc[:, 202:]
    return temp.iloc[:, slice]


def subset_count_stats(csv):
    return get_subset_with_stats(csv, slice(None, 36, None))


def subset_dist_stats(csv):
    return get_subset_with_stats(csv, slice(36, None, None))


def make_all_distri_plots(csv):
    make_distribution_box_plot(csv, "_ks_")
    # make_distribution_box_plot(csv, "_ranksums_")
    # make_distribution_box_plot(csv, "_ttest_")


def make_all_box_plots(csv):
    make_statistic_box_plot(csv, "_ks_")
    # make_statistic_box_plot(csv, "_wilcoxon_")
    # make_statistic_box_plot(csv, "_ttest_")


def temp_box_plot_of_ordered_frame(df, title="E", subspace=(3, 2), names=None, shared_y_labels=None, supylabel="Significance", shared_x_labels=None):
    fig, ax = plt.subplots(subspace[0], subspace[1], sharex=True, sharey=True)
    fig.suptitle(title)
    fig.supylabel(supylabel)
    plt.tight_layout()
    if shared_x_labels is not None:
        for a, n in zip(ax[0], shared_x_labels):
            a.set_title(n)
    if shared_y_labels is not None:
        for a, n in zip(ax, shared_y_labels):
            a[0].set_ylabel(n)
    axes = ax.flatten()
    if names is not None:
        for a, n in zip(axes, names):
            a.set_title(n)
    for i, a in enumerate(axes):
        a.set_xticks([2.5, 6.5, 10.5])
        a.set_xticklabels(["KS-Test", "Wilcoxon", "T-Test"], rotation=0)
        a.axvline(x=4.5, linestyle="--", alpha=0.4, color="gray")
        a.axvline(x=8.5, linestyle="--", alpha=0.4, color="gray")
        temp = df.iloc[:, i * 12: (i + 1) * 12]
        a.boxplot(temp, manage_ticks=False, showfliers=False, medianprops=dict(color="red"))
    return fig


def make_dist_plots(csv, csv_5, csv_25, csv_full):
    x1 = subset_dist_stats(csv)
    x2 = subset_dist_stats(csv_5)
    x_3 = subset_dist_stats(csv_25)
    x_4 = subset_dist_stats(csv_full)
    test = x1.join(x2, lsuffix="002", rsuffix="005")
    test = test.join(x_3, rsuffix="025")
    test = test.join(x_4, rsuffix="100")
    sort_vector = []
    for i in range(36):
        sort_vector = sort_vector + [i + j * 36 for j in range(4)]

    temp = test.iloc[:, sort_vector]  # REorder the large dataframe to be more suited to the application
    names = ["All", "Bike", "Car", "Passenger", "Pedestrian", "Publ. Transport"]
    travel_time_plot = temp_box_plot_of_ordered_frame(temp.iloc[:, :72], title="Travel Time Distribution", names=names)
    travel_time_plot.show()
    travel_time_plot.savefig("../../plots/travel_time_plot.svg", format="svg", bbox_inches="tight")
    travel_dist_plot = temp_box_plot_of_ordered_frame(temp.iloc[:, 72:], title="Travel Distance Distribution", names=names)
    travel_dist_plot.show()
    travel_dist_plot.savefig("../../plots/travel_dist_plot.svg", format="svg", bbox_inches="tight")


def make_count_plots(csv, csv_5, csv_25, csv_full):
    x1 = subset_count_stats(csv)
    x2 = subset_count_stats(csv_5)
    x_3 = subset_count_stats(csv_25)
    x_4 = subset_count_stats(csv_full)
    test = x1.join(x2, lsuffix="002", rsuffix="005")
    test = test.join(x_3, rsuffix="025")
    test = test.join(x_4, rsuffix="100")
    sort_vector = []
    for i in range(36):
        sort_vector = sort_vector + [i + j * 36 for j in range(4)]  # Group by ascending csvs
    temp = test.iloc[:, sort_vector]  # REorder the large dataframe to be more suited to the application
    sort_vector = []
    for j in range(12):  # Restructure so that the tests are in order of ks wilx ttest
        i = j * 12
        sort_vector = sort_vector + list(range(i + 8, i + 12)) + list(range(i + 0, i + 4)) + list(range(i + 4, i + 8))
    temp = temp.iloc[:, sort_vector]

    sort_vector = []
    for j in range(4):  # Drop the last 12 data elements because the test data is weird
        i = j * 36
        sort_vector = sort_vector + list(range(i, i + 24))
    temp = temp.iloc[:, sort_vector]
    shar = ["Time", "Demand", "Distance", "O-D"]
    shar_x = ["$m$", "$\emptyset$"]
    travel_time_plot = temp_box_plot_of_ordered_frame(temp, title="Sample Statistic Tests", subspace=(4, 2), shared_y_labels=shar, supylabel=None, shared_x_labels=shar_x)
    travel_time_plot.show()

    travel_time_plot.savefig("../../plots/count_stochastics.svg", format="svg", bbox_inches="tight")
    # travel_dist_plot = temp_box_plot_of_ordered_frame(temp.iloc[:, 72:], title="Travel Distance Ea", subspace=(4,2))
    # travel_dist_plot.show()
    # travel_dist_plot.savefig("../../plots/travel_dist_plot.svg", format="svg")


def get_table_contents(df):
    print(df.T["mean"].values)


def make_id_appendix(cols):
    ret = []
    for col in cols:
        ret = ret + [col + x for x in ["", "005", "025", "100"]]
    return ret


def metric_box_plots_demand(big_df):
    for m in METRICS:
        sse = big_df[make_id_appendix(get_metrics(list(range(1, 5)), 1, m))]
        print(sse.columns)
        sse.plot(kind="box", title=m)
        plt.show()


def single_metric_box_plots_demand(big_df, frame_zero=0):
    #for m in METRICS:
    fig, axe = plt.subplots(2, 4, figsize=(6, 2))
    names = ["SSE", "MABSE", "MAVGE", "RMSE", "THEIL", "SSPE", "MSSE", "SCAE"]
    ax = axe.flatten()
    #plt.tight_layout()
    for (i, m), n in zip(enumerate(METRICS), names):
        ax[i].set_yticks([])
        #ax[i].set_yticklabels([])
        ax[i].set_ylabel(n)
        sse = big_df[get_metrics(frame_zero, [2, 1], m)]
        print(sse.columns)
        rename_temp(sse)
        sse.plot(kind='box', ax=ax[i],
             color=dict(boxes='r', whiskers='r', medians='r', caps='r'),
             boxprops=dict(linestyle='-', linewidth=1.5),
             flierprops=dict(linestyle='-', linewidth=1.5),
             medianprops=dict(linestyle='-', linewidth=1.5, color="red"),
             whiskerprops=dict(linestyle='-', linewidth=1.5),
             capprops=dict(linestyle='-', linewidth=1.5),
             showfliers=False, grid=False, rot=0)
    plt.tight_layout()

    #fig.text(0.05, 0.5, 'common ylabel', ha='center', va='center', rotation='vertical')
    fig.show()
    return fig


def rename_temp(df):
    if len(df.columns) == 2:
        df.columns = ["$\emptyset$", "$m$"]
    if len(df.columns) == 4:
        df.columns = ["2", "5", "25", "100"]
    elif len(df.columns) == 8:
        df.columns = ["2+K", "5+K", "25+K", "100+K", "2", "5", "25", "100"]

def metric_modal_box_plots(big_df, title=""):

    for m in METRICS:
        fig, ax = plt.subplots()
        sse = big_df[make_id_appendix(get_modal_metrics(0, [1], m))]
        #sse = sse.iloc[:,[0, 4, 1, 5, 2, 6, 3, 7]]
        rename_temp(sse)
        # ax.set_xticks([1, 2, 3, 4])
        # ax.set_xticklabels(["2", "5", "25", "100"],  rotation=0)
        print(sse.columns)
        sse.plot(kind='box', title=m, ax=ax,
                 color=dict(boxes='r', whiskers='r', medians='r', caps='r'),
                 boxprops=dict(linestyle='-', linewidth=1.5),
                 flierprops=dict(linestyle='-', linewidth=1.5),
                 medianprops=dict(linestyle='-', linewidth=1.5, color="red"),
                 whiskerprops=dict(linestyle='-', linewidth=1.5),
                 capprops=dict(linestyle='-', linewidth=1.5),
                 showfliers=False, grid=False, rot=0)
        ##ax.boxplot(sse, manage_ticks=False, showfliers=True, medianprops=dict(color="red"))

        fig.show()


def metric_box_plots(big_df, title="", resolution=1):

    for m in METRICS:
        fig, ax = plt.subplots()
        sse = big_df[make_id_appendix(get_metrics(0, resolution, m))]
        #sse = sse.iloc[:,[0, 4, 1, 5, 2, 6, 3, 7]]
        rename_temp(sse)
        # ax.set_xticks([1, 2, 3, 4])
        # ax.set_xticklabels(["2", "5", "25", "100"],  rotation=0)
        print(sse.columns)
        sse.plot(kind='box', title=m, ax=ax,
                 color=dict(boxes='r', whiskers='r', medians='r', caps='r'),
                 boxprops=dict(linestyle='-', linewidth=1.5),
                 flierprops=dict(linestyle='-', linewidth=1.5),
                 medianprops=dict(linestyle='-', linewidth=1.5, color="red"),
                 whiskerprops=dict(linestyle='-', linewidth=1.5),
                 capprops=dict(linestyle='-', linewidth=1.5),
                 showfliers=False, grid=False, rot=0)
        ##ax.boxplot(sse, manage_ticks=False, showfliers=True, medianprops=dict(color="red"))

        fig.show()


def make_sse_and_theil_plot(big_df, num_data=0, call=get_metrics, frame=1):
    fig, ax = plt.subplots(1, 2, figsize=(6, 2))
    ax[0].set_xlabel("SSE")
    ax[1].set_xlabel("THEIL")
    plt.tight_layout()
    for i, m in enumerate([0, 4]):
        sse = big_df[make_id_appendix(call(num_data, frame, m))]
        #sse = sse.iloc[:,[0, 4, 1, 5, 2, 6, 3, 7]]
        rename_temp(sse)
        # ax.set_xticks([1, 2, 3, 4])
        # ax.set_xticklabels(["2", "5", "25", "100"],  rotation=0)
        print(sse.columns)
        sse.plot(kind='box', title="", ax=ax[i],
                 color=dict(boxes='r', whiskers='r', medians='r', caps='r'),
                 boxprops=dict(linestyle='-', linewidth=1.5),
                 flierprops=dict(linestyle='-', linewidth=1.5),
                 medianprops=dict(linestyle='-', linewidth=1.5, color="red"),
                 whiskerprops=dict(linestyle='-', linewidth=1.5),
                 capprops=dict(linestyle='-', linewidth=1.5),
                 showfliers=False, grid=False, rot=0)
        ##ax.boxplot(sse, manage_ticks=False, showfliers=True, medianprops=dict(color="red"))

    fig.show()
    return fig

def insanely_large_table(df):
    for m in METRICS:
        temp = df[make_id_appendix(get_metrics(0, 1, m))]
        temp = temp.describe()
        x = temp.T["mean"].values
        x = [str(numpy.round(i, 2)) for i in x]
        print("& " + "& ".join(x) + "\\\\")


def main():
    csv = pandas.read_csv(SPECS.EXP_PATH_LOCAL + "data_random/002.csv")
    csv_5 = pandas.read_csv(SPECS.EXP_PATH_LOCAL + "data_random/005.csv")
    csv_25 = pandas.read_csv(SPECS.EXP_PATH_LOCAL + "data_random/025.csv")
    csv_full = pandas.read_csv(SPECS.EXP_PATH_LOCAL + "data_random/100.csv")
    x = csv.describe()
    x.to_csv(SPECS.EXP_PATH_LOCAL + "TargetArea002.csv", index=True)
    main_df = csv.join(csv_5, lsuffix="", rsuffix="005")
    main_df = main_df.join(csv_25, rsuffix="025")
    main_df = main_df.join(csv_full, rsuffix="100")
    # single_metric_box_plots_demand(csv)
    # metric_box_plots_demand(main_df)
    insanely_large_table(main_df)

    fig = single_metric_box_plots_demand(csv)
    fig.savefig("../../plots/Default_and_none_comparison_time.svg", format="svg")
    fig.show()

    fig = single_metric_box_plots_demand(csv, frame_zero=5)
    fig.savefig("../../plots/Default_and_none_comparison_destination.svg", format="svg")
    fig.show()

    #metric_box_plots(main_df, resolution=[1,2])

    fig = make_sse_and_theil_plot(main_df)
    fig.savefig("../../plots/SSE-and-Theil-TravelTime.svg", format="svg")
    fig.show()
    fig = make_sse_and_theil_plot(main_df, call=get_modal_metrics, frame=0)
    fig.savefig("../../plots/SSE-and-Theil-ModalSplit.svg", format="svg")
    fig.show()

    metric_modal_box_plots(main_df)
    make_sse_and_theil_plot(main_df, num_data=6)

    sse = main_df[make_id_appendix(get_metrics(0, 1, 0))]
    sse.plot(kind="box")
    plt.show()

    for x in [csv, csv_5, csv_25, csv_full]:
        x = x.rename(columns=lambda col: col.strip())
    x = csv.describe()
    y = csv_full.describe()
    print(y)
    print(get_metrics(0, None, None))
    get_table_contents(x[get_metrics(0, 2, 0)])
    get_table_contents(x[get_metrics(0, 0, None)])

    test = csv.mean()
    statistics = y.iloc[:, 202:]
    count_statistics = statistics.loc[:, :"CountComparisonStatisticTest_Destinations_ks_all"]
    dist_statistics = statistics.iloc[:, 36:]
    # make_all_box_plots(csv)
    # make_all_box_plots(csv_5)
    # make_all_box_plots(csv_25)
    # make_all_box_plots(csv_full)

    make_count_plots(csv, csv_5, csv_25, csv_full)
    make_dist_plots(csv, csv_5, csv_25, csv_full)
    exit()
    make_all_distri_plots(csv)
    make_all_distri_plots(csv_5)
    make_all_distri_plots(csv_25)
    make_all_distri_plots(csv_full)
    exit()
    c_wil = get_subset_on_identifier(count_statistics, "wilcoxon")
    c_ks = get_subset_on_identifier(count_statistics, "_ks_")
    c_tt = get_subset_on_identifier(count_statistics, "ttest")

    plt.boxplot(c_wil.T["mean"])
    plt.plot(c_ks.T["mean"])
    plt.plot(c_tt.T["mean"])
    plt.show()
    # plt.plot(statistics.T["mean"])
    # plt.show()
    z = y.iloc[:, 2:26]
    default = z.iloc[:, :8]
    all = z.iloc[:, 8:16]
    none = z.iloc[:, 16:]
    print(csv)
    print(test)


if __name__ == "__main__":
    main()
