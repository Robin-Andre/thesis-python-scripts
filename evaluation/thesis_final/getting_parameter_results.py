from pathlib import Path

import pandas

from calibration.evolutionary.individual import Individual
import mobitopp_execution as simulation

def get_df_from_file(path, params):
    ind = Individual(param_list=params)
    if path is not None:
        ind.load(path)
    df = pandas.DataFrame(ind.active_values(), columns=["Parameter Name", "Value"])
    df = df.set_index("Parameter Name")
    return df


def main():
    read_path = r"\\ifv-fs\User\Abschlussarbeiten\Robin.Andre\Experimente\Ergebnisse\MyAlgorithmFullTwoPassesNoMinMax\data\ImprovedDetailPasses100_Algo42\individual_1588"
    read_path2 = r"\\ifv-fs\User\Abschlussarbeiten\Robin.Andre\Experimente\Ergebnisse\MyAlgorithmFullTwoPassesNoMinMax\data\ImprovedDetailPasses101_Algo42\individual_1681"
    read_path3 = r"\\ifv-fs\User\Abschlussarbeiten\Robin.Andre\Experimente\Ergebnisse\MyAlgorithmFullTwoPassesNoMinMax\data\ImprovedDetailPasses102_Algo42\individual_1600"

    reqs = ['workday', 'gender', 'employment', 'age', 'activityType',
            'tripMode', 'previousMode', 'economicalStatus', 'nominalSize', 'totalNumberOfCars']
    params = simulation.default_yaml().mode_config().get_all_parameter_names_on_requirements(reqs)
    df1 = get_df_from_file(read_path, params)
    df2 = get_df_from_file(read_path2, params)
    df3 = get_df_from_file(read_path3, params)
    df_blank =get_df_from_file(None, params)
    print(df1)
    print(df2)
    df_concated = df1.join(df2, lsuffix="", rsuffix="2")
    df_concated = df_concated.join(df3, lsuffix="", rsuffix="3")
    df_concated = df_concated.join(df_blank, lsuffix="", rsuffix="Target")

    temp = df_concated.sub(df_concated["ValueTarget"], axis=0)
    temp = temp.iloc[:, :3]
    temp = temp.T
    des = temp.describe()
    des = des.loc[["min", "mean", "max"], :]
    des = des.T

    out = des.join(df_blank)
    out = out.loc[:, ["Value", "min", "mean", "max"]]
    out.columns = ["Original", "Dmin", "Dmean", "Dmax"]
    rounded = out.round(2)
    print(rounded.to_latex(index=True, longtable=True))
    print(df_concated)

if __name__ == "__main__":
    main()
