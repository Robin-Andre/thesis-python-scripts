import pandas
import pandas as pd
import numpy as np
import sys
print(sys.version)
from plotnine import ggplot, aes, geom_line


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
    return temp


def evaluate(path):
    df = pd.read_csv(path, sep=";", usecols=["tripBegin", "tripEnd", "tripMode"])
    plot_data = create_plot_data(df)
    plot_data = plot_data.reset_index()
    print(ggplot(plot_data, aes(x='time', y='active_trips')) + geom_line())
    plot_data = plot_data.iloc[::60]
    print(ggplot(plot_data, aes(x='time', y='active_trips')) + geom_line())
    return



    end = df["tripEnd"].to_frame()
    end = end.rename(columns={"tripEnd": "time"})
    end["value"] = - 1
    mix = pandas.concat([begin, end])
    mix = mix.sort_values("time")
    mix["active_trips"] = mix["value"].cumsum()
    mix = mix.set_index("time")
    print(mix)
    print(mix[mix.index.duplicated()])
   # mix = mix.reindex(np.arange(0, 10116))
   # print(mix)


