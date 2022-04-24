import numpy
import pandas
from matplotlib import pyplot as plt


def _interpolate(x_1, y_1, x_2, y_2, y_target):
    assert y_1 != y_2
    a = (y_target - y_1) / (y_2 - y_1)
    return a * (x_2 - x_1) + x_1


def funct(serieseee):
    x = serieseee.cumsum()
    x.dropna(inplace=True)
    quantile_values = x.quantile([.1, .2, .3, .4, .5, .6, .7, .8, .9])
    #return [(numpy.abs(series - i)).argmin() for i in quantile_values]

    x_1_index = [numpy.where(x < i)[0][-1] for i in quantile_values]
    x_2_index = [i + 1 for i in x_1_index]

    t_1 = x.take(x_1_index)
    t_2 = x.take(x_2_index)

    y_1 = t_1.values
    y_2 = t_2.values

    x_1 = t_1.index.get_level_values(-1).values
    x_2 = t_2.index.get_level_values(-1).values

    y_target = quantile_values.values
    better_results = [_interpolate(a, b, c, d, e) for a, b, c, d, e in zip(x_1, y_1, x_2, y_2, y_target)]
    return better_results

def main():
    path = "C:\\Users\\bo5742\\Desktop\\thesis-experiments\\thesis_save-main\\b_tt_csvs\\"
    modes = [("bike", 0), ("car_d", 1), ("car_p", 2), ("put", 4)]
    mode_nums = [0, 1, 2, 3, 4]
    for mode in modes:
        file = pandas.read_csv(path + "b_tt_" + mode[0] + "_mu.csv")
        for modenum in mode_nums:
            temp = file[file["tripMode"] == modenum]
            temp = temp.iloc[:, 2:]
            temp = temp.set_index("durationTrip")

            lol = temp.apply(funct)
            print(temp)
            test = lol.sub(lol['target'], axis=0)
            test = test.iloc[:, 1:-1]

            test = test.append(test.sum(), ignore_index=True)
            test.T.plot(title=f"{mode[0]}  {modenum}")
    plt.show()


if __name__ == "__main__":
    main()
