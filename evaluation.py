from math import radians, cos, sin, asin, sqrt
from pathlib import Path

import pandas
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

def aggregate_traffic_demand(data, attribute_list):
    return _cumulate_traffic_demand(_merge_traffic_demand(data, attribute_list))

def _merge_traffic_demand(clean_data, keeper_list):
    assert "time" not in keeper_list
    temp = clean_data.copy()
    temp = temp.reset_index()
    temp = temp.groupby(keeper_list + ["time"]).sum()
    temp = temp.reset_index()
    temp = temp[keeper_list + ["time", "active_trips_delta"]]
    temp = temp.set_index(keeper_list + ["time"])
    #temp = temp.sort_values("time", kind="mergesort").sort_index()
    temp = temp.sort_index()
    temp = temp.reset_index(level="time")
    return temp

def _cumulate_traffic_demand(data):
    temp = data.copy()
    temp = temp.drop(columns=["active_trips_delta"])
    data = data.drop(columns="time")
    data = data.groupby(data.index).cumsum()
    data["time"] = temp["time"]
    data = data.rename(columns={"active_trips_delta": "active_trips"})
    return data

def create_traffic_demand_data(almost_raw_data):
    temp = almost_raw_data[["tripBegin", "tripMode", "activityType", "age",
                             "employment", "gender", "hasCommuterTicket", "economicalStatus", "totalNumberOfCars",
                             "nominalSize"]].copy()
    temp["counts_begin"] = 1
    x = temp.groupby(["tripMode", "activityType", "age", "employment", "gender", "hasCommuterTicket", "economicalStatus",
                  "totalNumberOfCars", "nominalSize", "tripBegin"]).sum()
    x = x.reset_index(level="tripBegin")
    x = x.rename(columns={"tripBegin": "time"})

    temp2 = almost_raw_data[["tripEnd", "tripMode", "activityType", "age",
                             "employment", "gender", "hasCommuterTicket", "economicalStatus", "totalNumberOfCars",
                             "nominalSize"]].copy()
    temp2["counts_end"] = -1
    y = temp2.groupby(["tripMode", "activityType", "age", "employment", "gender", "hasCommuterTicket", "economicalStatus",
                  "totalNumberOfCars", "nominalSize", "tripEnd"]).sum()
    y = y.reset_index(level="tripEnd")
    y = y.rename(columns={"tripEnd": "time"})
    z = pandas.concat([x, y])
    z = z.fillna(0)
    z["active_trips_delta"] = z["counts_begin"] + z["counts_end"]
    z = z.sort_values("time", kind="mergesort").sort_index()
    z = z.drop(columns=["counts_begin", "counts_end"])

    return z

def create_travel_time_data(raw_data):
    temp_df = raw_data[["durationTrip", "tripMode"]]
    temp2_df = temp_df.groupby(["durationTrip", "tripMode"]).size().reset_index()
    temp2_df.columns = ["durationTrip", "tripMode", "amount"]
    return temp2_df


# TODO fix that there are journeys with distance 0
def create_travel_distance_data(raw_data):
    temp_df = raw_data[["distanceInKm", "tripMode"]]
    temp_df["distanceInKm"] = round(temp_df["distanceInKm"] * 1000)  # MobiTopp has an incorrect column
    temp_df = temp_df.groupby(["distanceInKm", "tripMode"]).size()
    temp_df = temp_df.reset_index()
    temp_df.columns = ["distanceInKm", "tripMode", "amount"]
    return temp_df


def create_travel_distance_with_activity_type(raw_data):
    temp_df = raw_data[["distanceInKm", "tripMode", "activityType", "previousActivityType"]].copy()
    temp_df.loc[temp_df["activityType"] == 7, "activityType"] = temp_df[temp_df["activityType"] == 7]["previousActivityType"]
    temp_df.loc[:, "distanceInKm"] = round(temp_df["distanceInKm"] * 1000)

    print(temp_df[temp_df["activityType"] == 7])
    temp_df["actual_activity"] = temp_df["activityType"]


    temp_df["distanceInKm"] = round(temp_df["distanceInKm"] * 1000)  # MobiTopp has an incorrect column
    temp_df = temp_df.groupby(["distanceInKm", "tripMode", "activityType"]).size()
    temp_df = temp_df.reset_index()
    temp_df.columns = ["distanceInKm", "tripMode", "activityType", "amount"]
    return temp_df

def extract_person_data(raw_data):
    raw_data


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
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r
