import re

import pandas


def extract_values_of_iteration(config, iteration):
    lines = config._text.split("\n")
    results = []
    for line in lines:
        test = re.sub("=\s*([-+])", "= \\1", line)
        test = re.split("(?<!=\s)([-+])", test)
        temp = 2 * iteration + 1
        results.append(" ".join(test[0:temp]))
    return "\n".join(results)

def making_test_data_smaller():
    raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
    raw_dat_house = pandas.read_csv("resources/household.csv", sep=";")
    print(len(set(raw_dat_house.householdId)))

    raw_dat_person = pandas.read_csv("resources/person.csv", sep=";")
    print(list(set(raw_dat_person.personId)))
    hId = list(set(raw_data.householdOid))
    pId = list(set(raw_data.personOid))
    print(pId)

    x = raw_dat_house[raw_dat_house.householdId.isin(hId)]
    y = raw_dat_person[raw_dat_person.personId.isin(pId)]
    y.to_csv("resources/person.csv", sep=";")
    x.to_csv("resources/household.csv", sep=";")
    print(len(set(raw_dat_house.householdId)))
    print(len(set(x.householdId)))