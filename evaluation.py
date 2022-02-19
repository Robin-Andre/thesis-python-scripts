import math
import time
from math import radians, cos, sin, asin, sqrt
from pathlib import Path

import pandas
import pandas as pd
import numpy as np

from configurations import parameter, SPECS


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


def create_traffic_demand_data(almost_raw_data, vector=["tripMode", "activityType", "age", "employment", "gender",
                                                        "hasCommuterTicket", "economicalStatus", "totalNumberOfCars",
                                                        "nominalSize"]):
    temp = almost_raw_data[["tripBegin"] + vector].copy()

    temp["counts_begin"] = 1
    x = temp.groupby((vector + ["tripBegin"])).sum()
    x = x.reset_index(level="tripBegin")
    x = x.rename(columns={"tripBegin": "time"})

    temp2 = almost_raw_data[["tripEnd"] + vector].copy()
    temp2["counts_end"] = -1
    y = temp2.groupby((vector + ["tripEnd"])).sum()
    y = y.reset_index(level="tripEnd")
    y = y.rename(columns={"tripEnd": "time"})

    z = pandas.concat([x, y])
    z = z.fillna(0)
    z["active_trips_delta"] = z["counts_begin"] + z["counts_end"]

    z = z.sort_values("time", kind="mergesort").sort_index()
    z = z.drop(columns=["counts_begin", "counts_end"])
    z = z.reset_index()
    return z


def create_travel_time_data_new(almost_raw_data, vector=None):
    if vector is None:
        vector = ["tripMode", "activityType", "age", "employment", "gender",
                  "hasCommuterTicket", "economicalStatus", "totalNumberOfCars",
                  "nominalSize"]
    temp = almost_raw_data[["durationTrip"] + vector].copy()

    temp = temp.groupby(vector + ["durationTrip"]).agg({"durationTrip": "count"})
    temp = temp.rename(columns={"durationTrip": "count"})
    temp = temp.reset_index()
    return temp


def create_travel_distance_data_new(almost_raw_data, vector=["tripMode", "activityType", "age", "employment", "gender",
                                                             "hasCommuterTicket", "economicalStatus", "totalNumberOfCars",
                                                             "nominalSize"]):
    temp = almost_raw_data[["distanceInKm"] + vector].copy()

    temp["distanceInKm"] = 1000 * temp["distanceInKm"]
    temp["distanceInKm"] = temp["distanceInKm"].apply(np.ceil)


    temp = temp.groupby(vector + ["distanceInKm"]).agg({"distanceInKm": "count"})
    temp = temp.rename(columns={"distanceInKm": "count"})
    temp = temp.reset_index()
    return temp


def extract_data(yaml):
    data = pandas.read_csv(SPECS.CWD + yaml.data["resultFolder"] + "/demandsimulationResult.csv", sep=";")
    data_household = pandas.read_csv(SPECS.CWD + yaml.data["dataSource"]["demandDataFolder"] + "/household.csv", sep=";")
    data_person = pandas.read_csv(SPECS.CWD + yaml.data["dataSource"]["demandDataFolder"] + "/person.csv", sep=";")
    return merge_data(data, data_household, data_person)


def default_test_merge():
    data_person = pandas.read_csv("resources/person.csv", sep=";")
    data_household = pandas.read_csv("resources/household.csv", sep=";")
    data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
    return merge_data(data, data_household, data_person)

def group_data2(x):
    """
    Some Values such as age or occupation are only accessed as a group by calibration parameters, this method
    groups the values accordingly
    :param x:
    :return:
    """
    x.age = x.age.apply(parameter.AgeGroup.int_to_group)
    x.employment = x.employment.apply(parameter.Employment.get_employment_from_int)
    x.economicalStatus = x.economicalStatus.apply(parameter.EconomicalGroup.get_eco_group_from_int)
    x.totalNumberOfCars = x.totalNumberOfCars.apply(parameter.NumberOfCars.get_num_cars_from_int)
    x.activityType = x.activityType.apply(parameter.ActivityGroup.activity_int_to_mode)
    x.nominalSize = x.nominalSize.apply(parameter.HouseholdSize.get_hh_size_from_int)
    return x


def group_data(x):
    parameter.group_age(x)
    parameter.group_economical_status(x)
    parameter.group_activity(x)
    parameter.group_employment(x)
    parameter.group_household_size(x)
    parameter.group_number_of_cars(x)

    return x


def merge_data(data, household, person):
    x = data.merge(person, how="left", left_on="personOid", right_on="personId")
    x = x.merge(household, how="left", left_on="householdOid", right_on="householdId")
    x = x[["tripMode", "activityType", "age",
          "employment", "gender", "hasCommuterTicket", "economicalStatus", "totalNumberOfCars",
          "nominalSize", "tripBegin", "tripEnd", "durationTrip", "distanceInKm"]]
    x = group_data(x)
    return x


def create_travel_time_data(raw_data):
    temp_df = raw_data[["durationTrip", "tripMode"]]
    temp2_df = temp_df.groupby(["durationTrip", "tripMode"]).size().reset_index()
    temp2_df.columns = ["durationTrip", "tripMode", "amount"]
    return temp2_df


# TODO fix that there are journeys with distance 0
def create_travel_distance_data(raw_data):
    temp_df = raw_data[["distanceInKm", "tripMode"]].copy()
    temp_df["distanceInKm"] = round(temp_df["distanceInKm"] * 1000)  # MobiTopp has an incorrect column
    temp_df = temp_df.groupby(["distanceInKm", "tripMode"]).size()
    temp_df = temp_df.reset_index()
    temp_df.columns = ["distanceInKm", "tripMode", "amount"]
    return temp_df


def create_travel_distance_with_activity_type(raw_data):
    temp_df = raw_data[["distanceInKm", "tripMode", "activityType", "previousActivityType"]].copy()
    temp_df.loc[temp_df["activityType"] == 7, "activityType"] = temp_df[temp_df["activityType"] == 7]["previousActivityType"]
    temp_df.loc[:, "distanceInKm"] = round(temp_df["distanceInKm"] * 1000)

    temp_df["actual_activity"] = temp_df["activityType"]


    temp_df["distanceInKm"] = round(temp_df["distanceInKm"] * 1000)  # MobiTopp has an incorrect column
    temp_df = temp_df.groupby(["distanceInKm", "tripMode", "activityType"]).size()
    temp_df = temp_df.reset_index()
    temp_df.columns = ["distanceInKm", "tripMode", "activityType", "amount"]
    return temp_df



def check_data(raw_data):  # TODO move to experimental??
    temp = raw_data[["fromX", "fromY", "toX", "toY", "distanceInKm"]]
    temp["haversine"] = temp.apply(haversine, axis=1)
    temp["distanceInKm"] = temp["distanceInKm"] * 1000



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
