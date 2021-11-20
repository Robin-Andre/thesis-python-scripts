from plotnine import ggplot, aes, geom_line, ggsave, ggtitle, scale_linetype_manual, scale_size_manual, \
    scale_alpha_manual, scale_color_manual, facet_wrap, scale_x_continuous


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


def draw(dataframe, function, path="", show=True, modulo=1, title=""):
    assert modulo >= 1 and type(modulo) is int
    df = dataframe[dataframe["time"] % modulo == 0]
    plot_data = function(df) + ggtitle(title)
    if show:
        print(plot_data)
    if path != "":
        ggsave(plot_data, path=path, filename=title)
