import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_line, ggsave


def make_unique_df(raw_data, selection_vector):
    # This method should only be invoked on tripBegin / tripEnd
    assert selection_vector == "tripBegin" or selection_vector == "tripEnd"
    temp_df = raw_data[selection_vector].to_frame()
    temp_df = temp_df.rename(columns={selection_vector: "time"})
    temp_df["value"] = 1 if selection_vector == "tripBegin" else -1
    # Sometimes multiple trips start at the same time frame, we need to group them
    temp_df = temp_df.groupby(["time"]).sum()
    return temp_df


def create_plot_data(raw_data):
    begin = make_unique_df(raw_data, "tripBegin")
    end = make_unique_df(raw_data, "tripEnd")
    temp = pd.concat([begin, end], axis=1)
    temp.columns = ["start", "end"]
    temp = temp.fillna(0)
    temp["sum"] = temp["start"] + temp["end"]
    temp = temp.drop(columns=["start", "end"])
    temp["active_trips"] = temp["sum"].cumsum()
    temp = temp.drop(columns=["sum"])
    last_index = temp.index[-1]
    temp = temp.reindex(np.arange(0, last_index), method="pad")
    temp = temp.fillna(0)
    temp = temp.reset_index()
    return temp


def evaluate_modal(path):
    df = pd.read_csv(path, sep=";", usecols=["tripBegin", "tripEnd", "tripMode"]).groupby("tripMode")
    temp = df.apply(lambda x: create_plot_data(x))
    return temp


def evaluate(path):
    df = pd.read_csv(path, sep=";", usecols=["tripBegin", "tripEnd", "tripMode"])
    plot_data = create_plot_data(df)
    return plot_data


def make_plot(data_frame, precision, path="", show=True):
    temp = data_frame.iloc[::precision]
    plot = ggplot(temp, aes(x='time', y='active_trips')) + geom_line()
    if show:
        print(plot)
    if path != "":
        ggsave(plot, file=path)


def make_modal_plot(data_frame, precision, path="", show=True):
    temp = data_frame.iloc[::precision]
    temp = temp.reset_index(level="tripMode")
    plot = ggplot(temp, aes(x='time', y='active_trips', color="factor(tripMode)")) + geom_line()
    if show:
        print(plot)
    if path != "":
        ggsave(plot, file=path)


def compare_dataframes(df1, df2):
    NotImplemented
