import numpy
import pandas
import plotnine
import scipy
from matplotlib import pyplot as plt
from plotnine import ggplot, aes, geom_line, ggsave, ggtitle, scale_linetype_manual, scale_size_manual, \
    scale_alpha_manual, scale_color_manual, facet_wrap, scale_x_continuous, geom_histogram, geom_segment, geom_bar, \
    labs, scale_fill_manual, scale_fill_discrete, theme, ylab, xlab, geom_text, position_stack, facet_grid
from plotnine.themes import theme_bw

import metric


def aggregate_traffic_two_sets(df):
    # TODO useful name for temp
    temp = "factor(identifier)"
    return ggplot(df, aes(x='time', y='active_trips')) \
           + geom_line(aes(size=temp, alpha=temp, color=temp)) \
           + scale_size_manual(values=[1, 1]) + scale_alpha_manual(values=[0.2, 1]) \
           + scale_color_manual(values=["#999999", "#E69F00"]) \
           + scale_x_continuous(breaks=[0, 1440, 2880, 4320, 5760, 7200, 8640], labels=["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"])


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

def aggregate_traffic_modal_two_sets(df_modal):
    return ggplot(df_modal, aes(x='time', y='active_trips')) \
           + geom_line(aes(color="factor(identifier)")) + facet_wrap("tripMode", labeller=label_modes) \
           + scale_x_continuous(breaks=[0, 1440, 2880, 4320, 5760, 7200, 8640], labels=["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"])


def aggregate_traffic(data_frame):
    return ggplot(data_frame, aes(x='time', y='active_trips')) + geom_line()


def aggregate_traffic_modal(data_frame):
    return ggplot(data_frame, aes(x='time', y='active_trips', color="factor(tripMode)")) + geom_line()

# Gives unnamed Dataframes a name
def identify_yourself(data_frame_list):
    for index, frame in enumerate(data_frame_list):
        if not "identifier" in frame:
            frame["identifier"] = "Dataframe_" + str(index)
            print(f"Setting index for element {index}")


def draw_modal_split(data_frame_list):
    identify_yourself(data_frame_list)
    return ggplot(pandas.concat(data_frame_list).reset_index(),
                  aes(x="factor(identifier)", y="amount", fill="factor(tripMode)", label="amount")) + geom_bar(stat="identity") \
        + scale_fill_discrete(name="Mode", labels=["Bike", "Car", "Passenger", "Pedestrian", "Public Transport"]) \
        + theme(subplots_adjust={'right': 0.5}) + ylab("Percentage") + xlab("") \
        + geom_text(size=8, position=position_stack(vjust=0.5), format_string="%s"%("{:,.2f}"))


def draw_travel_time(data_frame, bin_size=1, quantile=0.99):
    count = data_frame["amount"].sum() * quantile
    temp_df = data_frame
    temp_df["cumulative"] = temp_df["amount"].cumsum()
    temp_df = temp_df[temp_df["cumulative"] < count]
    return ggplot(temp_df, aes(x="durationTrip", weight="amount", fill="factor(tripMode)")) + geom_histogram(binwidth=bin_size) # + geom_bar()


def draw_travel_time2(data_frame, bin_size=1, quantile=0.99):
    df_quantile = data_frame["durationTrip"].quantile(quantile)
    temp_df = data_frame[["durationTrip", "tripMode"]]
    sane_data = temp_df[temp_df["durationTrip"] < df_quantile]
    return ggplot(sane_data, aes(x="durationTrip", fill="factor(tripMode)")) + geom_histogram(binwidth=bin_size)


def draw_travel_distance(data_frame, bin_size=1, quantile=0.99):
    df_quantile = data_frame["distanceInKm"].quantile(quantile)
    sane_data = data_frame[data_frame["distanceInKm"] < df_quantile]
    print(sane_data)
    return ggplot(sane_data, aes(x="distanceInKm", weight="amount", fill="factor(tripMode)")) + geom_histogram(binwidth=bin_size)


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
    plt.show()

def draw_travel_distance_per_mode(data_frame, bin_size=1, quantile=0.99):
    fig = plt.figure()
    fig, ax = plt.subplots(3, 2)
    for trip_mode in data_frame["tripMode"].unique():
        temp = data_frame[data_frame["tripMode"] == trip_mode]
        helper(temp, str(trip_mode), ax[trip_mode // 2][trip_mode % 2])
    temp = data_frame.groupby("distanceInKm").sum()
    temp = temp.drop(columns=["tripMode"])
    helper(temp, "All", ax[2][1])
    plt.show()
    return


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
