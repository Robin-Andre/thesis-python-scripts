import os
import pandas
from plotnine import ggplot, aes, geom_line, ggsave, scale_size_manual, ggtitle, geom_ribbon


def range_plot(sub_dir):
    file_path = "/home/paincrash/Desktop/master-thesis/experiment_results_permanent/seed_experiment/"
    #sub_dir = "1"
    data_frames = []
    data_frames_modal = []
    for i in range(1, 11):
        df = pandas.read_csv(file_path + sub_dir + "/" + str(i) + "Seed")
        df_modal = pandas.read_csv(file_path + sub_dir + "/" + str(i) + "SeedMODAL")
        df["identifier"] = i
        df_modal["identifier"] = i
        data_frames.append(df)
        data_frames_modal.append(df_modal)

    frame = pandas.concat(data_frames)
    min_trips = frame.groupby(["time"])["active_trips"].min()
    max_trips = frame.groupby(["time"])["active_trips"].max()
    min_trips = min_trips.rename("min_trips")
    max_trips = max_trips.rename("max_trips")
    frame = pandas.concat([min_trips, max_trips], axis=1)
    frame["diff"] = frame["max_trips"] - frame["min_trips"]
    frame["diff_quotient"] = 1 - frame["diff"] / (frame["max_trips"] + frame["min_trips"])
    frame = frame.reset_index()
    print(frame["diff"].max())
    plot = ggplot(frame, aes(x='time')) + geom_ribbon(aes(ymin='min_trips', ymax ='max_trips'), fill="grey")
    plot = ggplot(frame, aes(x="time", y="diff")) + geom_line()
    plot = ggplot(frame, aes(x="time", y="diff_quotient")) + geom_line()

    frame_modal = pandas.concat(data_frames_modal)
    #evaluation.find_boundaries(data_frames)


if __name__ == '__main__':
    range_plot("0.01")
    range_plot("0.1")
    range_plot("1")



