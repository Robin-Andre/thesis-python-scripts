from pathlib import Path

import pandas

from calibration.evolutionary.individual import Individual
from configurations import SPECS
from metrics.data import Data, Comparison


def main():
    fractions = ["002", "005", "025", "100"]
    for fraction in fractions:
        data_list = []
        for file in Path(SPECS.EXP_PATH + "data_random/data/fraction_of_population_" + fraction).iterdir():
            #i = Individual()
            data = Data()
            data.load(str(file) + "/results/")
            #i.load(file)
            data_list.append(data)
            temp = data.travel_time.get_data_frame()
            count = temp["count"].sum()
            print(f"Loaded from: {file} {count} trips")
        c = Comparison(data_list[0], data_list[0])
        comp_list = []
        for x in range(len(data_list)):
            for y in range(x + 1, len(data_list)):
                print(f"{x} {y}")
                c = Comparison(data_list[x], data_list[y])
                temp = [x, y] + list(c.mode_metrics.values()) + list(c.destination_metrics.values()) + list(c.statistic_tests.values())
                comp_list.append(temp)

        df = pandas.DataFrame(comp_list, columns=["runID", "secondrunID"] + list(c.mode_metrics.keys()) + list(c.destination_metrics.keys()) + list(c.statistic_tests.keys()))
        df.to_csv(SPECS.EXP_PATH + "data_random/" + fraction + ".csv", index=False)



if __name__ == "__main__":
    main()