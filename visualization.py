import pandas
from plotnine import ggplot, aes, geom_line, ggsave, ggtitle, scale_linetype_manual, scale_size_manual, \
    scale_alpha_manual, scale_color_manual, facet_wrap, scale_x_continuous, geom_histogram, geom_segment


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
        "0": "Bike",
        "1": "Car",
        "2": "Passenger",
        "3": "Pedestrian",
        "4": "Public Transport"
    }
    return d[s]


def aggregate_traffic_modal_two_sets(df_modal):
    return ggplot(df_modal, aes(x='time', y='active_trips')) \
           + geom_line(aes(color="factor(identifier)")) + facet_wrap("tripMode", labeller=label_modes) \
           + scale_x_continuous(breaks=[0, 1440, 2880, 4320, 5760, 7200, 8640], labels=["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"])


def aggregate_traffic(data_frame):
    return ggplot(data_frame, aes(x='time', y='active_trips')) + geom_line()


def aggregate_traffic_modal(data_frame):
    return ggplot(data_frame, aes(x='time', y='active_trips', color="factor(tripMode)")) + geom_line()


def draw_travel_time(data_frame, bin_size=1):
    return ggplot(data_frame, aes(x="durationTrip", fill="factor(tripMode)")) + geom_histogram(binwidth=bin_size)


def draw_travel_distance(data_frame, bin_size=1):
    return ggplot(data_frame, aes(x="distanceInKm")) + geom_histogram(binwidth=bin_size)


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
