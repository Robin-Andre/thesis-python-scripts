import math

import numpy
import pandas
import scipy
from matplotlib import pyplot as plt

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


# Gives unnamed Dataframes a name
def identify_yourself(data_frame_list):
    for index, frame in enumerate(data_frame_list):
        if not "identifier" in frame:
            frame["identifier"] = "Dataframe_" + str(index)
            print(f"Setting index for element {index}")
    return pandas.concat(data_frame_list)


#TODO cleanup after work
def draw_travel_demand(data_series, color_num=-1, title=""):

    #temp = temp.ewm(com=1).mean()
    plt.plot(data_series, color=color_modes(color_num))
    plt.title(title)
    #plt.plot(temp, color=color_modes(color_num))
    plt.show()


def draw_travel_demand_by_mode(data_frame, mode_list=[-1, 0, 1, 2, 3, 4], title="Active Trips", reference_df=None):

    fig, ax = plt.subplots(3, 2, sharex=True)
    fig.suptitle(title)
    for i, element in enumerate(mode_list):
        df = data_frame.get_mode_specific_data(element)
        ax[i // 2][i % 2].plot(df, color=color_modes(element))
        ax[i // 2][i % 2].set_xticks([0, 1440, 2880, 4320, 5760, 7200, 8640, 10080])
        ax[i // 2][i % 2].set_xticklabels(["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So", "Mo"])
        if reference_df is not None:
            ref = reference_df.get_mode_specific_data(element)
            ax[i // 2][i % 2].plot(ref, color="black", alpha=0.2)
        #ax[i // 2][i % 2].scatter(*zip(*data_frame.get_week_peaks(element)), color=color_modes(element))
    return fig
    #plt.show()


def generic_td_demand(data_frame, agg_list):
    generic_plot(data_frame, agg_list, "active_trips")


def generic_travel_time(data_frame, agg_list):
    temp = data_frame.reset_index()
    temp = temp.groupby(agg_list + ["durationTrip"]).count().reset_index()
    print(temp)
    generic_plot(temp, agg_list, "durationTrip")


def generic_plot(data_frame, agg_list, keyword):
    inputs = list(set(data_frame[agg_list]))
    square_value = math.ceil(math.sqrt(len(inputs)))
    rest = math.ceil(len(inputs) / square_value)
    print(f"{agg_list} {inputs}")
    print(f"Length{len(inputs)} {square_value} x {rest}")
    fig, ax = plt.subplots(square_value, rest, sharex=True)

    for i, element in enumerate(inputs):
        if rest > 1:
            cur_ax = ax[i // rest][i % rest]
        else:
            cur_ax = ax[i // rest]

        temp = data_frame[data_frame[agg_list] == element]
        cur_ax.plot(temp.time, temp[keyword])
        cur_ax.set_title(element)

    fig.suptitle(agg_list)
    fig.show()



def draw_modal_split(df_list):
    fig, ax = plt.subplots()
    if type(df_list) is not list: df_list = [df_list] # Makes single element entry to a list
    dfl = [x.get_modal_split() for x in df_list]
    y = identify_yourself(dfl)
    y['cumsum'] = y.groupby('identifier')['amount'].transform(pandas.Series.cumsum) - y["amount"]
    y = y.reset_index()
    box = ax.bar(y["identifier"], y["amount"], color=[color_modes(x) for x in y["tripMode"]], bottom=y["cumsum"])
    ax.bar_label(box, label_type="center", fmt='%.2f')
    fig.show()
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

def draw_geographic_travels(data_frame):

    lowerleft = [48.81589706887127, 8.113229703230964]
    upperright = [48.917977211186084, 8.280771208296814]

    # lowerleft = [48, 8.0]
    # upperright = [49, 8.5]
    temp_df = data_frame.loc[(data_frame["fromX"] > upperright[1]) | (data_frame["fromX"] < lowerleft[1])]
    temp_df = temp_df.loc[(temp_df["toX"] > upperright[1]) | (temp_df["toX"] < lowerleft[1])]
    temp_df = temp_df.loc[(temp_df["fromY"] > upperright[0]) | (temp_df["fromY"] < lowerleft[0])]
    temp_df = temp_df.loc[(temp_df["toY"] > upperright[0]) | (temp_df["toY"] < lowerleft[0])]

    x1 = [lowerleft[1], upperright[1], upperright[1], lowerleft[1]]
    x2 = [upperright[1], upperright[1], lowerleft[1], lowerleft[1]]
    y1 = [upperright[0], upperright[0], lowerleft[0], lowerleft[0]]
    y2 = [upperright[0], lowerleft[0], lowerleft[0], upperright[0]]
    d = {"fromX": x1, "fromY": y1, "toX": x2, "toY": y2}
    bounding_box = pandas.DataFrame(data=d)

    return ggplot(temp_df, aes(x="fromX", y="fromY", xend="toX", yend="toY")) + geom_segment() + geom_segment(bounding_box)


def draw_geographic_locations(data_frame):
    from_df = data_frame[["fromX", "fromY"]]
    from_df = from_df.rename(columns={"fromX": "X", "fromY": "Y"})
    to_df = data_frame[["toX", "toY"]]
    to_df = to_df.rename(columns={"toX": "X", "toY": "Y"})
    return ggplot(pandas.concat[from_df, to_df])


def draw(dataframe, function, path="", show=True, modulo=1, title=""):
    assert modulo >= 1 and type(modulo) is int
    df = dataframe[dataframe["time"] % modulo == 0]
    plot_data = function(df) + ggtitle(title)
    if show:
        print(plot_data)
    if path != "":
        ggsave(plot_data, path=path, filename=title)
