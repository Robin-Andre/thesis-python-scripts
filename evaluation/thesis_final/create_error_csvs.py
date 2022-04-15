from pathlib import Path

from calibration.evolutionary.individual import Individual, DestinationIndividual
from configurations import SPECS
import mobitopp_execution as simulation


def write(path, csv):
    with open(path, "w+") as file:
        file.write(csv)


def load_run(path, params, target):
    csv_list = [",".join(params)]
    for file in sorted(path.iterdir(), key=lambda i: int(i.name.split("_")[1])):
        print(file)
        ind = Individual(param_list=params)
        ind.load(file)
        csv_list.append(",".join([str(x[1]) for x in ind.errors(target.data)]))
    csv_string = "\n".join(csv_list)
    write(path.parent.parent / "csv" / (path.name + "parameter_list.csv"), csv_string)


def load_run_competition(path, params, target):
    csv_list = [",".join(params)]
    for file in sorted(path.iterdir(), key=lambda i: int(i.name)):
        print(file)
        ind = Individual(param_list=params)
        ind.load(file)
        csv_list.append(",".join([str(x[1]) for x in ind.errors(target.data)]))
    csv_string = "\n".join(csv_list)
    write(path.parent.parent / "csv" / (path.name + "parameter_list.csv"), csv_string)


def load_run_competition_destination(path, params, target):
    csv_list = [",".join(params)]
    for file in sorted(path.iterdir(), key=lambda i: int(i.name)):
        print(file)
        ind = DestinationIndividual(param_list=params)
        ind.load(file)
        csv_list.append(",".join([str(x[1]) for x in ind.errors(target.data)]))
    csv_string = "\n".join(csv_list)
    write(path.parent.parent / "csv" / (path.name + "parameter_list.csv"), csv_string)


def make_error_tracking_for_experiment(params, path, reference=None):
    for file in (path / "data").iterdir():
        print(file)
        load_run(params, file, reference)

def make_error_tracking_for_experiment_competition(params, path, reference=None):
    for file in (path / "data").iterdir():
        print(file)
        load_run_competition(params, file, reference)

def make_error_tracking_for_experiment_competition_destination(params, path, reference=None):
    for file in (path / "data").iterdir():
        print(file)
        load_run_competition(params, file, reference)

def main():
    params = ["asc_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "asc_bike_mu", "b_tt_car_p_mu",
              "b_tt_car_d_mu", "b_tt_put_mu", "b_tt_bike_mu", "b_tt_ped"]

    ref = Individual(param_list=params)
    ref.run()
    load_run_competition(Path("D:/master_thesis_final_results/pygad_10_parameters_target_has_same_seed/data/101_metric_ModalSplit_Default_Splits_sum_squared_error/"), params, ref)
    return

    make_error_tracking_for_experiment(params, Path(SPECS.EXP_PATH + "/MyExperimentBetterErrorGuessing/"), ref)
    make_error_tracking_for_experiment(params, Path(SPECS.EXP_PATH + "/MyExperimentQuantiles/"), ref)  # MyExperimentQuantiles

    make_error_tracking_for_experiment(params, Path(SPECS.EXP_PATH + "/MyExperimentVeryHighPrecision/"), ref)  # MyExperimentVeryHighPrecision

    make_error_tracking_for_experiment(params, Path(SPECS.EXP_PATH + "/MyExperimentVariableQuantilesFixedOutput/"), ref) # MyExperimentVariableQuantilesFixedOutput
    cost_params = ["b_cost", "b_cost_put", "b_inc_high_on_b_cost", "b_inc_high_on_b_cost_put"]
    make_error_tracking_for_experiment(cost_params, Path(SPECS.EXP_PATH + "/MyExperimentVariableQuantilesCostFixedOutput/"), ref) # MyExperimentVariableQuantilesCostFixedOutput
    make_error_tracking_for_experiment(params, Path(SPECS.EXP_PATH + "/tuningAlphabeforeBeta/"), ref)


    list_of_comp_experiments = ["pygad_10_parameters", "pygad_10_parameters_target_has_same_seed",
                                "pyswarms_10_parameters", "pyswarms_10_parameters_target_has_same_seed",
                                "spsa_10_parameters_target_has_same_seed"]
    for l in list_of_comp_experiments:
        make_error_tracking_for_experiment_competition(params, "/" + l + "/", ref)


    """ individual_seed is set:
spsa_10_parameters_target_has_same_seed_time_metric2
pygad_10_parameters_target_has_same_seed_time_metric2
pyswarms_10_parameters_target_has_same_seed2
pyswarms_10_parameters_target_has_same_seed_time_metric2

RecreatingManualTuningProcess

9001
pyswarms_main_mode_all_parameters
pygad_main_mode_all_parameters
spsa_main_mode_all_parameters

d is set 

erroneous_comparison_data

random_target_10_parameters_time_metric

"""

    reqs = ['workday', 'gender', 'employment', 'age', 'activityType',
            'tripMode', 'previousMode', 'economicalStatus', 'nominalSize', 'totalNumberOfCars']
    all_mode_params = simulation.default_yaml().mode_config().get_all_parameter_names_on_requirements(reqs)

    dest_params = simulation.default_yaml().get_all_dest_parameters_name([])
    dest_params.remove('b_cost')
    dest_params.remove('b_tt_acc_put')

    dest_business_params = simulation.default_yaml().get_all_dest_parameters_name(["business"])
    dest_business_params.remove('b_cost')
    dest_business_params.remove('b_tt_acc_put')

    dest_all_params = simulation.default_yaml().get_all_dest_parameters_name(["business", "leisure", "shopping", "service"])
    dest_all_params.remove('b_cost')
    dest_all_params.remove('b_tt_acc_put')
    algos = ["spsa", "pyswarms", "pygad"]
    appendix = ["", "_plus_all", "_plus_business"]
    p_list = [dest_params, dest_all_params, dest_business_params]

    for a in algos:
        for app, param_li in zip(appendix, p_list):
            make_error_tracking_for_experiment_competition_destination(param_li, Path(SPECS.EXP_PATH + "/" + a + "_main_destination_same_seed" + app + "/"), ref)

    # TODO enable on other machine
    #make_error_tracking_for_experiment(all_mode_params, Path(SPECS.EXP_PATH + "/MyAlgorithmFullMode/"), ref)
    #make_error_tracking_for_experiment(all_mode_params, Path(SPECS.EXP_PATH + "/MyAlgorithmFullTwoPasses/"), ref)

if __name__ == "__main__":
    main()