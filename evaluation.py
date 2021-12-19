from math import radians, cos, sin, asin, sqrt
from pathlib import Path

import pandas as pd
import numpy as np


def __make_unique_df(raw_data, selection_vector):
    assert selection_vector == "tripBegin" or selection_vector == "tripEnd"
    temp_df = raw_data[selection_vector].to_frame()
    temp_df = temp_df.rename(columns={selection_vector: "time"})
    temp_df["value"] = 1 if selection_vector == "tripBegin" else -1
    # Sometimes multiple trips start at the same time frame, we need to group them
    temp_df = temp_df.groupby(["time"]).sum()
    return temp_df


def create_plot_data(raw_data):
    begin = __make_unique_df(raw_data, "tripBegin")
    end = __make_unique_df(raw_data, "tripEnd")
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


def create_travel_time_data(raw_data):
    temp_df = raw_data[["durationTrip", "tripMode"]]
    temp2_df = temp_df.groupby(["durationTrip", "tripMode"]).size().reset_index()
    temp2_df.columns = ["durationTrip", "tripMode", "amount"]
    return temp2_df

#TODO fix that there are journeys with distance 0
def create_travel_distance_data(raw_data):
    temp_df = raw_data[["distanceInKm", "tripMode"]]
    temp_df["distanceInKm"] = round(temp_df["distanceInKm"] * 1000) # MobiTopp has an incorrect column
    temp_df = temp_df.groupby(["distanceInKm", "tripMode"]).size()
    temp_df = temp_df.reset_index()
    temp_df.columns = ["distanceInKm", "tripMode", "amount"]
    return temp_df


def check_data(raw_data):  # TODO move to experimental??
    temp = raw_data[["fromX", "fromY", "toX", "toY", "distanceInKm"]]
    temp["haversine"] = temp.apply(haversine, axis=1)
    temp["distanceInKm"] = temp["distanceInKm"] * 1000
    print(temp)


def haversine(row):
    return haversine_internal(row.fromX, row.fromY, row.toX, row.toY)


def haversine_internal(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r





