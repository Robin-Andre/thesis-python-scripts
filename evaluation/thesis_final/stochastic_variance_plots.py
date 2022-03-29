import numpy
import pandas
from matplotlib import pyplot as plt

from configurations import SPECS

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
    #stat_csv = get_subset_on_identifier(stat_csv, idf)
    fig, ax = plt.subplots()
    ax.boxplot(stat_csv,  showfliers=False)
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
    #make_distribution_box_plot(csv, "_ranksums_")
    #make_distribution_box_plot(csv, "_ttest_")

def make_all_box_plots(csv):
    make_statistic_box_plot(csv, "_ks_")
    #make_statistic_box_plot(csv, "_wilcoxon_")
    #make_statistic_box_plot(csv, "_ttest_")


def temp_box_plot_of_ordered_frame(df, title="E", subspace=(3, 2)):

    fig, ax = plt.subplots(subspace[0], subspace[1], sharex=True, sharey=True)
    fig.suptitle(title)
    plt.tight_layout()
    axes = ax.flatten()

    for i, a in enumerate(axes):
        a.set_xticks([2.5, 6.5, 10.5])
        a.set_xticklabels(["KS-Test", "Wilcoxon", "T-Test"],  rotation=0)
        a.axvline(x=4.5, linestyle="--", alpha=0.4, color="gray")
        a.axvline(x=8.5, linestyle="--", alpha=0.4, color="gray")
        a.boxplot(df.iloc[:, i * 12: (i + 1) * 12], manage_ticks=False,  showfliers=False, medianprops=dict(color="red"))
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
    travel_time_plot = temp_box_plot_of_ordered_frame(temp.iloc[:, :72], title="Travel Time Distribution")
    travel_time_plot.show()
    travel_time_plot.savefig("../../plots/travel_time_plot.svg", format="svg")
    travel_dist_plot = temp_box_plot_of_ordered_frame(temp.iloc[:, 72:], title="Travel Distance Distribution")
    travel_dist_plot.show()
    travel_dist_plot.savefig("../../plots/travel_dist_plot.svg", format="svg")



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
        sort_vector = sort_vector + [i + j * 36 for j in range(4)] # Group by ascending csvs
    temp = test.iloc[:, sort_vector] # REorder the large dataframe to be more suited to the application
    sort_vector = []
    for j in range(12): # Restructure so that the tests are in order of ks wilx ttest
        i = j * 12
        sort_vector = sort_vector + list(range(i + 8, i + 12)) + list(range(i + 0, i + 4)) + list(range(i + 4, i + 8))
    temp = temp.iloc[:, sort_vector]

    sort_vector = []
    for j in range(4): # Drop the last 12 data elements because the test data is weird
        i = j * 36
        sort_vector = sort_vector + list(range(i, i + 24))
    temp = temp.iloc[:, sort_vector]


    travel_time_plot = temp_box_plot_of_ordered_frame(temp, title="Sample Stochastic Tests", subspace=(4,2))
    travel_time_plot.show()

    travel_time_plot.savefig("../../plots/count_stochastics.svg", format="svg")
    #travel_dist_plot = temp_box_plot_of_ordered_frame(temp.iloc[:, 72:], title="Travel Distance Ea", subspace=(4,2))
    #travel_dist_plot.show()
    #travel_dist_plot.savefig("../../plots/travel_dist_plot.svg", format="svg")



def main():
    csv = pandas.read_csv(SPECS.EXP_PATH + "data_random/002.csv")
    csv_5 = pandas.read_csv(SPECS.EXP_PATH + "data_random/005.csv")
    csv_25 = pandas.read_csv(SPECS.EXP_PATH + "data_random/025.csv")
    csv_full = pandas.read_csv(SPECS.EXP_PATH + "data_random/100.csv")
    x = csv.describe()
    y = csv_full.describe()
    test = csv.mean()
    statistics = y.iloc[:, 202:]
    count_statistics = statistics.loc[:, :"CountComparisonStatisticTest_Destinations_ks_all"]
    dist_statistics = statistics.iloc[:, 36:]
    #make_all_box_plots(csv)
    #make_all_box_plots(csv_5)
    #make_all_box_plots(csv_25)
    #make_all_box_plots(csv_full)

    make_count_plots(csv, csv_5, csv_25, csv_full)
    #make_dist_plots(csv, csv_5, csv_25, csv_full)
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
    #plt.plot(statistics.T["mean"])
    #plt.show()
    z = y.iloc[:, 2:26]
    default = z.iloc[:, :8]
    all = z.iloc[:, 8:16]
    none = z.iloc[:, 16:]
    print(csv)
    print(test)


if __name__ == "__main__":
    main()