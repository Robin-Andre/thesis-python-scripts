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
    x1 = subset_dist_stats(csv)
    x2 = subset_dist_stats(csv_5)
    test = x1.join(x2, lsuffix="002", rsuffix="005")
    fig, ax = plt.subplots()
    ax.boxplot(test,  showfliers=False)
    fig.show()
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