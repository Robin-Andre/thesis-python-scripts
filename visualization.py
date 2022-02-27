import math
from ast import literal_eval

import numpy
import pandas
import scipy
from matplotlib import pyplot as plt

from configurations import SPECS


def label_modes(s):
    d = {
        -1: "All",
        0: "Bike",
        1: "Car",
        2: "Passenger",
        3: "Pedestrian",
        4: "Public Transport"
    }
    if s in d.keys():
        return d[s]
    return "Unknown Label"

def color_modes(s):
    d = {
        -1: "#888888",
        0: "#e41a1c",
        1: "#377eb8",
        2: "#4daf4a",
        3: "#984ea3",
        4: "#ff7f00"
    }
    if s in d.keys():
        return d[s]
    return "#000000"


def color_age(s):
    d = {
        0: "#888888",
        18: "#e41a1c",
        30: "#377eb8",
        50: "#4daf4a",
        60: "#984ea3",
        70: "#ff7f00",
        100: "#11efff"
    }
    if s in d.keys():
        return d[s]
    return "#000000"




# Gives unnamed Dataframes a name
def identify_yourself(data_frame_list):
    for index, frame in enumerate(data_frame_list):
        if not "identifier" in frame:
            frame["identifier"] = "Dataframe_" + str(index)
            #print(f"Setting index for element {index}")
    return pandas.concat(data_frame_list)


#TODO cleanup after work
def draw_travel_demand(data_series, color_num=-1, title=""):

    #temp = temp.ewm(com=1).mean()
    plt.plot(data_series, color=color_modes(color_num))
    plt.title(title)
    #plt.plot(temp, color=color_modes(color_num))
    plt.show()


def draw_travel_demand_by_mode(data_frame, title="Active Trips", reference_df=None, group="tripMode"):
    trip_mode_list = list(set(data_frame[group]))
    fig, ax = plt.subplots(math.ceil(len(trip_mode_list)), 2, sharex=True)
    fig.suptitle(title)

    for i, element in enumerate(trip_mode_list):
        df = data_frame[data_frame[group] == element]
        ax[i // 2][i % 2].plot(df["time"], df["active_trips"], color=color_modes(element))
        ax[i // 2][i % 2].set_xticks([0, 1440, 2880, 4320, 5760, 7200, 8640, 10080])
        ax[i // 2][i % 2].set_xticklabels(["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So", "Mo"])
        if reference_df is not None:
            ref = reference_df[reference_df[group] == element]
            ax[i // 2][i % 2].plot(ref["time"], ref["active_trips"], color="black", alpha=0.2)
        #ax[i // 2][i % 2].scatter(*zip(*data_frame.get_week_peaks(element)), color=color_modes(element))
    return fig

def draw_travel_distance_without_modes(obj, reference=None):
    temp = obj.get_data_frame().groupby("distanceInKm").sum()["count"]
    fig, ax = plt.subplots()
    if reference is not None:
        temp2 = reference.get_data_frame().groupby("distanceInKm").sum()["count"]
        temp2 = temp2.rename("Reference")
        temp = pandas.concat([temp, temp2], axis=1)

    temp.plot(kind="line", ax=ax)
    return fig

def helper(row):
    print("lol")


def draw_zone_demand(obj, reference=None):
    fig, ax = plt.subplots()
    temp = obj.get_data_frame()
    if reference is not None:
        temp = obj - reference
    lol = temp.groupby(level=[0, 1]).sum()
    centroids = pandas.read_csv(SPECS.CWD + "output/rastatt/zone-repository/test_zone.csv", encoding='cp1252', sep=";")[["id", "centroidLocation", "classification"]]



    centroids["centroidLocation"] = centroids["centroidLocation"].apply(lambda x: x.replace(":", ","))
    centroids[["x", "y", "boring", "noidea"]] = centroids["centroidLocation"].str[1:-1].str.split(",", expand=True).astype(float)

    t = centroids[centroids["classification"] == "studyArea"]
    xmin = t["x"].min()
    xmax = t["x"].max()
    ymin = t["y"].min()
    ymax = t["y"].max()


    leonidas = centroids[["id", "x", "y"]]
    lol = lol.reset_index()
    test = pandas.merge(lol, leonidas, left_on="sourceZone", right_on="id")
    test = test.rename(columns={"x": "origin_x", "y": "origin_y"})
    test = pandas.merge(test, leonidas, left_on="targetZone", right_on="id")
    test = test.rename(columns={"x": "target_x", "y": "target_y"})
    test = test[["sourceZone", "targetZone", "traffic", "origin_x", "origin_y", "target_x", "target_y"]]

    for idx, row in test.iterrows():
        col = "red" if row["traffic"] > 0 else "blue"
        if row["sourceZone"] != row["targetZone"] and row["traffic"] != 0:
            ax.plot([row["origin_x"], row["target_x"]], [row["origin_y"], row["target_y"]],
                     linewidth=math.log2(abs(row["traffic"])) - 1, color=col, alpha=math.log10(abs(row["traffic"])) * 0.05)
        elif row["sourceZone"] == row["targetZone"] and row["traffic"] != 0:
            ax.plot(row["origin_x"], row["origin_y"], marker="o", color=col, markersize=math.log2(abs(row["traffic"])) - 1, alpha=math.log10(abs(row["traffic"])) * 0.05)


    #ax.set_xlim([8.15, 8.25])
    #ax.set_ylim([48.825, 48.9])
    #ax.set_xlim([xmin, xmax])
    #ax.set_ylim([ymin, ymax])
    fig.show()




def generic_td_demand(data_frame, agg_list):
    generic_plot(data_frame, agg_list, "active_trips", "time")


def generic_min_max_best(data_frame, agg_list):
    generic_plot(data_frame, agg_list, ["min", "max", "best", "target"], "time")


def generic_min_max_best_travel_time(data_frame, agg_list):
    generic_plot(data_frame, agg_list, ["min", "max", "best", "target"], "durationTrip", sharex=False)


def two_level_travel_time(data_frame, p1, p2="tripMode"):
    p1list = list(set(data_frame[p1]))
    for val in p1list:
        generic_travel_time(data_frame[data_frame[p1] == val], p2)
    print(p1list)


def generic_travel_time(data_frame, agg_list):
    #temp = data_frame.reset_index()
    #temp = data_frame.groupby([agg_list, "durationTrip"]).count().reset_index()
    generic_plot(data_frame, agg_list, "count", "durationTrip")


def generic_travel_distance(data_frame, agg_list):
    temp = data_frame.reset_index()
    temp = temp.groupby([agg_list, "distanceInKm"]).count().reset_index()
    generic_plot(temp, agg_list, "count", "distanceInKm")


def generic_smol_plot(data_frame, agg_list, keyword, x, element):
    fig, ax = plt.subplots()
    temp = data_frame[data_frame[agg_list] == element]
    ax.plot(temp[x], temp[keyword])
    ax.set_title(element)
    fig.show()


def generic_plot(data_frame, split_element_name, keyword, x, color_seperator=None, sharex=True, reference_df=None):
    inputs = list(set(data_frame[split_element_name]))
    inputs.sort()
    square_value = math.ceil(math.sqrt(len(inputs)))
    rest = math.ceil(len(inputs) / square_value)
    fig, ax = plt.subplots(square_value, rest, sharex=sharex)

    for i, element in enumerate(inputs):
        if rest > 1:
            cur_ax = ax[i // rest][i % rest]
        else:
            cur_ax = ax[i // rest]

        temp = data_frame[data_frame[split_element_name] == element]


        if color_seperator is not None:
            tmp = temp.groupby(color_seperator)
            for key, group in tmp:
                cur_ax.plot(group[x], group[keyword], color=color_modes(key), alpha=0.4)
        else:

            cur_ax.plot(temp[x], temp[keyword])

            if reference_df is not None:
                temp2 = reference_df[reference_df[split_element_name] == element]
                cur_ax.plot(temp2[x], temp2[keyword])



        cur_ax.set_title(element)

    fig.suptitle(split_element_name)
    plt.legend(temp[keyword])
    #fig.show()
    return fig


def draw_modal_split(df_list):
    fig, ax = plt.subplots()
    if type(df_list) is not list: df_list = [df_list] # Makes single element entry to a list
    dfl = [x._get_modal_split() for x in df_list]
    y = identify_yourself(dfl)
    y['cumsum'] = y.groupby('identifier')['count'].transform(pandas.Series.cumsum) - y["count"]
    y = y.reset_index()
    box = ax.bar(y["identifier"], y["count"], color=[color_modes(x) for x in y["tripMode"]], bottom=y["cumsum"])
    #ax.bar_label(box, label_type="center", fmt='%.2f')
    fig.show()
    return


def draw_grouped_modal_split(df, title=""):
    x = df.T
    #df.plot(kind="bar", title=[""] * 13, stacked=True, rot=1, subplots=True, layout=(5, 3), legend=False)
    ax = x.plot(kind="bar", title=title, stacked=True, rot=1, legend=True)
    #plt.show()
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.9, box.height])

    # Put a legend to the right of the current axis
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.get_figure().show()
    #fig.show()
    return


def draw_travel_time(df, mode=-1, reference=None):
    temp = df.get_data_frame().groupby("durationTrip").sum()["amount"]

    temp.plot.bar(width=1, color=color_modes(mode))
    if reference is not None:
        r = reference.groupby("durationTrip").sum()["amount"]
        r.plot(color="red", alpha=0.8)
    plt.title(label_modes(mode))
    plt.xticks([0, 5, 10, 15, 20], [0, 5, 10, 15, 20])
    plt.tick_params(bottom=None, labelbottom=True)
    plt.show()


def draw_travel_time_per_mode(data_frame, mode_list=[-1, 0, 1, 2, 3, 4], title="Travel Time (min)", reference_df=None):
    fig, ax = plt.subplots(3, 2)
    fig.suptitle(title)
    for i, element in enumerate(mode_list):
        df = data_frame.get_mode_specific_data(element)
        if i % 2 == 1:
            ax[i // 2][i % 2].set_yticklabels([])
        #ax[i // 2][i % 2].set_yticklabels([])
        #ax[i // 2][i % 2].set_xticklabels([])

        ax[i // 2][i % 2].plot(df, color=color_modes(element))
        if reference_df is not None:
            ref = reference_df.get_mode_specific_data(element)
            ax[i // 2][i % 2].plot(ref, color="black", alpha=0.2)
        #ax[i // 2][i % 2].scatter(*zip(*data_frame.get_week_peaks(element)), color=color_modes(element))
    return fig
    #plt.show()


def draw_travel_distance(df):
    pass


def draw_travel_distance_per_mode(data_frame, mode_list=[-1, 0, 1, 2, 3, 4], title="Travel Distance (km)", reference_df=None):

    fig, ax = plt.subplots(3, 2)
    fig.suptitle(title)
    for i, element in enumerate(mode_list):
        df = data_frame.get_mode_specific_data(element)
        ax[i // 2][i % 2].plot(df, color=color_modes(element))
        if i % 2 == 1:
            ax[i // 2][i % 2].set_yticklabels([])
        if reference_df is not None:
            ref = reference_df.get_mode_specific_data(element)
            ax[i // 2][i % 2].plot(ref, color="black", alpha=0.2)
        #ax[i // 2][i % 2].scatter(*zip(*data_frame.get_week_peaks(element)), color=color_modes(element))
    return fig


def draw_distribution(distribution, mode=-1, approximation=None, ax=None):

    if ax is None:
        distribution.plot.bar(width=1.0, alpha=0.5, color=color_modes(mode))
        plt.plot(numpy.linspace(0, len(approximation) / 10, len(approximation)), approximation, color=color_modes(mode))
        plt.title(label_modes(mode))
        plt.xticks([0, 5, 10, 15, 20], [0, 5, 10, 15, 20])
        plt.tick_params(bottom=None, labelbottom=True)
        plt.show()
    else:
        ax.bar(distribution.index, distribution["amount"], width=1.0, alpha=0.5, color=color_modes(mode))
        ax.plot(numpy.linspace(0, len(approximation) / 10, len(approximation)), approximation, color=color_modes(mode))
        #ax.title(label_modes(mode))
        ax.tick_params(bottom=None, labelbottom=True)
        return ax


def draw_all_distributions(distribution_list, mode_list, approximation_list):
    fig, ax = plt.subplots(3, 2)
    for i, (dist, mode, approx) in enumerate(zip(distribution_list, mode_list, approximation_list)):
        draw_distribution(dist, mode, approx, ax[i // 2][i % 2])
    return fig


#def draw_travel_distance_per_mode(data_frame):
#    fig, ax = plt.subplots(3, 2)
#    for trip_mode in data_frame["tripMode"].unique():
#        temp = data_frame[data_frame["tripMode"] == trip_mode]
#        helper(temp, str(trip_mode), ax[trip_mode // 2][trip_mode % 2])
#    temp = data_frame.groupby("distanceInKm").sum()
#    temp = temp.drop(columns=["tripMode"])
#    helper(temp, "All", ax[2][1])
#    return fig


def helper(data_frame, title_num, ax):
    rounding = 1000
    data_frame["amount"] = data_frame["amount"] // rounding
    temp_ys = data_frame["amount"].values

    x = numpy.arange(len(temp_ys))
    y = temp_ys
    all_points = numpy.repeat(x, y)  # silly solution
    dist_names = ["gamma", "norm", "rayleigh"] #  'pareto' 'gamma''norm', 'rayleigh',
    for dist_name in dist_names:
        dist = getattr(scipy.stats, dist_name)
        params = dist.fit(all_points)

        arg = params[:-2]
        loc = params[-2]
        scale = params[-1]
        print(f"arg: {arg}, loc: {loc}, scale: {scale} : name = {dist_name} | title {title_num}")
        if arg:
            pdf_fitted = dist.pdf(x, *arg, loc=loc, scale=scale) * len(all_points)
        else:
            pdf_fitted = dist.pdf(x, loc=loc, scale=scale) * len(all_points)
        print(pdf_fitted)
        ax.set_ylim(y.max() * 1.2)
        ax.plot(pdf_fitted, label=dist_name, color="black")

    ax.invert_yaxis()
    #plt.legend(loc='upper right')
    #ax.set_title(label_modes(title_num))
    h = ax.hist(all_points, bins=all_points.max(), color=color_modes(str(title_num)))
    return ax

