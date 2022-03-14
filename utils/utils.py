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

    def test_make_cool_tables(self):
        path = Path(SPECS.CWD + "data/rastatt/useable_matrices")
        for p in path.iterdir():
            print(p.parent)
            name = p.name.split(".")[0]
            with open(p, "r") as file, open(str(p.parent) + "/" + name + ".csv", "w+") as outfile:
                print(outfile.name)
                strings = []
                for line in file:
                    if line.startswith(" "):
                        pattern = r"\s+(\S+)\s+(\S+)\s+(\S+)"
                        t = re.match(pattern, line)
                        s = t.group(1) + "," + t.group(2) + "," + t.group(3)
                        strings.append(s)
                cleansified = "\n".join(strings)

                outfile.write(cleansified)
        csv_file = pandas.read_csv(SPECS.CWD + "data/rastatt/zoneproperties/analysis/zoneproperties.csv", sep=";")
        #print(csv_file["zoneId"])

    def test_read_proper_cost_tables(self):
        csv_list = []
        for file in Path(SPECS.CWD + "data/rastatt/useable_matrices").iterdir():
            csv_file = pandas.read_csv(file, sep=",")
            csv_file = csv_file.set_index(["sourceZone", "targetZone"])
            csv_list.append(csv_file)
            print(csv_file)
        #test = reduce(lambda df1, df2: pandas.concat(df1, df2), csv_list)
        #print(test)
        test = pandas.concat(csv_list, axis=1)
        test.to_csv(SPECS.CWD + "data/rastatt/useable_matrices/time_and_costs.csv")
        print(test)