from pathlib import Path

import pandas as pd
import numpy as np


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


def save_compressed_output(param_name, input_path, output_path, identifier):
    Path(output_path).mkdir(parents=True, exist_ok=True)

    temp = evaluate_modal(input_path)
    temp.to_csv(output_path + param_name + identifier + "MODAL")
    temp = evaluate(input_path)
    temp.to_csv(output_path + param_name + identifier)


def compare_dataframes(df1, df2):
    NotImplemented
