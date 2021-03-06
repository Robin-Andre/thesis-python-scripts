from pathlib import Path
from calibration import pygad_genetic_algorithm, stochastic_perturbation_algorithm, pyswarms_algorithm, my_algorithm
from calibration.evolutionary.individual import Individual, DestinationIndividual
from configurations import SPECS
import random
import mobitopp_execution as simulation


def write(result, experiment, folder):
    with open(SPECS.EXP_PATH + folder + f"/{experiment}.csv", "w+") as file:
        file.write(result)


def build_folders(folder):
    folder_path = Path(SPECS.EXP_PATH + folder)
    csv_path = Path(SPECS.EXP_PATH + folder + "/csv")
    data_path = Path(SPECS.EXP_PATH + folder + "/data")
    for x in [folder_path, csv_path, data_path]:
        if not x.exists():
            print(f"{x} does not exist:...creating")
            x.mkdir()



def _help_launcher(param_list, seed, exname, descriptor, metric, individual_seed, d, algorithm, ind_constructor=Individual):
    build_folders(exname)
    if d is None:
        d = ind_constructor(seed=individual_seed, param_list=param_list)
        d.run()
    data = d.data
    p, result = algorithm(param_list, data, metric, seed, experiment_name=exname, descriptor=descriptor, individual_constructor=ind_constructor)
    write_helper(result, seed, exname, descriptor)

def launch_pygad(param_list, seed, exname="genetic_Unnamed", descriptor=None, metric="ModalSplit_Default_Splits_sum_squared_error", individual_seed=-1, d=None, individual_constructor=Individual):
    algorithm = pygad_genetic_algorithm.tune
    _help_launcher(param_list, seed, exname, descriptor, metric, individual_seed, d, algorithm=algorithm, ind_constructor=individual_constructor)



def launch_spsa(param_list, seed, exname="spsa_Unnamed", descriptor=None, metric="ModalSplit_Default_Splits_sum_squared_error", individual_seed=-1, d=None, individual_constructor=Individual):
    algorithm = stochastic_perturbation_algorithm.tune
    _help_launcher(param_list, seed, exname, descriptor, metric, individual_seed, d, algorithm=algorithm, ind_constructor=individual_constructor)



def launch_pyswarms(param_list, seed, exname="pyswarms_Unnamed", descriptor=None, metric="ModalSplit_Default_Splits_sum_squared_error", individual_seed=-1, d=None, individual_constructor=Individual):
    algorithm = pyswarms_algorithm.tune
    _help_launcher(param_list, seed, exname, descriptor, metric, individual_seed, d, algorithm=algorithm, ind_constructor=individual_constructor)


def launch_pygad_destination(param_list, seed, exname="genetic_Unnamed_destination", descriptor=None, metric="TravelDistance_Default_sum_squared_error", individual_seed=-1, d=None):
    launch_pygad(param_list, seed, exname, descriptor, metric, individual_seed, d, individual_constructor=DestinationIndividual)


def launch_spsa_destination(param_list, seed, exname="spsa_Unnamed_destination", descriptor=None, metric="TravelDistance_Default_sum_squared_error", individual_seed=-1, d=None):
    launch_spsa(param_list, seed, exname, descriptor, metric, individual_seed, d, individual_constructor=DestinationIndividual)


def launch_pyswarms_destination(param_list, seed, exname="pyswarms_Unnamed_destination", descriptor=None, metric="TravelDistance_Default_sum_squared_error", individual_seed=-1, d=None):
    launch_pyswarms(param_list, seed, exname, descriptor, metric, individual_seed, d, individual_constructor=DestinationIndividual)


def launch_my_algorithm(param_list, seed, exname="myalgorithm_Unnamed", descriptor=None, individual_seed=-1, d=None):
    random.seed(seed)
    build_folders(exname)
    if d is None:
        d = Individual(seed=individual_seed, param_list=param_list)
        d.run()
    data = d.data
    pop, result = my_algorithm.tune(param_list, data, "ModalSplit_Default_Splits_sum_squared_error")
    pop_save_helper(pop, seed, exname, descriptor)
    print(pop.best())
    write_helper(result, seed, exname, descriptor)


def launch_my_algorithm_new(param_list, seed, exname="myalgorithm_Unnamed", descriptor=None, individual_seed=-1, d=None,
                            algorithm_seed=-1, sub_r=my_algorithm.subroutine_default, metric="TravelTime_Default_sum_squared_error", use_existing_config=False):
    random.seed(seed)
    build_folders(exname)
    if d is None:
        d = Individual(seed=individual_seed, param_list=param_list)
        d.run()
    data = d.data
    pop, result, error_log = my_algorithm.tune_new(param_list, data, metric,
                                                   algorithm_seed, subroutine=sub_r, ex_name=exname, descriptor=descriptor, use_existing_config=use_existing_config)
    pop_save_helper(pop, seed, exname, descriptor)
    print(pop.best())
    write_helper(result, seed, exname, descriptor)
    write_error_log_helper(error_log, seed, exname, descriptor)



"""def launch_my_other_algorithm(param_list, seed, exname="myalgorithm_Unnamed", descriptor=None, individual_seed=-1, d=None):
    random.seed(seed)
    build_folders(exname)
    if d is None:
        d = Individual(seed=individual_seed, param_list=param_list)
        d.run()
    data = d.data
    pop, result = my_algorithm.temp2tune(param_list, data, "ModalSplit_Default_Splits_sum_squared_error")
    pop_save_helper(pop, seed, exname, descriptor)
    print(pop.best())
    write_helper(result, seed, exname, descriptor)"""

def pop_save_helper(pop, seed, exname, descriptor):
    if descriptor is None:
        pop.save(SPECS.EXP_PATH + exname + "/data/seed" + str(seed) + "/")
    else:
        pop.save(SPECS.EXP_PATH + exname + "/data/" + descriptor + "/")

def write_error_log_helper(result, seed, exname, descriptor):
    if descriptor is None:
        write(result, "seed" + str(seed) + "_errors", exname)
    else:
        write(result, descriptor + "_errors", exname)


def write_helper(result, seed, exname, descriptor):
    if descriptor is None:
        write(result, "seed" + str(seed), exname)
    else:
        write(result, descriptor, exname)


def experiment_spsa_target_has_same_seed(params):
    for i in range(101, 106):
        launch_spsa(params, i, "spsa_10_parameters_target_has_same_seed")


def experiment_spsa_target_has_same_seed_time_metric(params):
    for i in range(108, 109):
        launch_spsa(params, i, "spsa_10_parameters_target_has_same_seed_time_metric2", metric="TravelTime_Default_sum_squared_error", individual_seed=i)


def experiment_pygad_target_has_same_seed(params):
    for i in range(106, 111):
        launch_pygad(params, i, "pygad_10_parameters_target_has_same_seed")

def experiment_pygad_target_has_same_seed_time_metric(params):
    for i in range(106, 109):
        launch_pygad(params, i, "pygad_10_parameters_target_has_same_seed_time_metric2", metric="TravelTime_Default_sum_squared_error", individual_seed=i)

def experiment_pyswarms_target_has_same_seed(params):
    for i in range(106, 109):
        launch_pyswarms(params, i, "pyswarms_10_parameters_target_has_same_seed2", individual_seed=i)

def experiment_pyswarms_target_has_same_seed_time_metric(params):
    for i in range(106, 109):
        launch_pyswarms(params, i, "pyswarms_10_parameters_target_has_same_seed_time_metric2", metric="TravelTime_Default_sum_squared_error", individual_seed=i)


def experiment_meta_heuristics_destination_same_seed():
    params = simulation.default_yaml().get_all_dest_parameters_name([])
    params.remove('b_cost')
    params.remove('b_tt_acc_put')
    for i in [108, 109, 110]:

        launch_pygad_destination(params, i, "pygad_main_destination_same_seed")

        launch_pyswarms_destination(params, i, "pyswarms_main_destination_same_seed")
    for i in [107, 108,109, 110]:
        launch_spsa_destination(params, i, "spsa_main_destination_same_seed")


def experiment_meta_heuristics_destination_same_seed_with_business():
    params = simulation.default_yaml().get_all_dest_parameters_name(["business"])
    params.remove('b_cost')
    params.remove('b_tt_acc_put')
    print(params)
    metrict = "TravelDistance_All_sum_squared_error"

    for i in [106, 107, 108]: #, 109, 110]:
        launch_pyswarms_destination(params, i, "pyswarms_main_destination_same_seed_plus_business", metric=metrict)
        launch_pygad_destination(params, i, "pygad_main_destination_same_seed_plus_business", metric=metrict)


    for i in [106, 107, 108]:
        launch_spsa_destination(params, i, "spsa_main_destination_same_seed_plus_business", metric=metrict)


def experiment_meta_heuristics_for_all_mode_parameters():
    reqs = ['workday', 'gender', 'employment', 'age', 'activityType',
            'tripMode', 'previousMode', 'economicalStatus', 'nominalSize', 'totalNumberOfCars']
    params = simulation.default_yaml().mode_config().get_all_parameter_names_on_requirements(reqs)
    metrict = "TravelTime_All_sum_squared_error"
    target_seed = 9001
    #for i in [106, 107, 108]: #, 109, 110]:
    #    launch_pyswarms(params, i, "pyswarms_main_mode_all_parameters", metric=metrict, individual_seed=target_seed)
    #    launch_pygad(params, i, "pygad_main_mode_all_parameters", metric=metrict, individual_seed=target_seed)


    for i in [106, 107, 108]:
        launch_spsa(params, i, "spsa_main_mode_all_parameters", metric=metrict, individual_seed=target_seed)

def experiment_meta_heuristics_destination_same_seed_with_all_modes():
    params = simulation.default_yaml().get_all_dest_parameters_name(["business", "leisure", "shopping", "service"])
    params.remove('b_cost')
    params.remove('b_tt_acc_put')
    print(params)
    metrict = "TravelDistance_All_sum_squared_error"

    for i in [106, 107, 108]: #, 109, 110]:
        launch_pyswarms_destination(params, i, "pyswarms_main_destination_same_seed_plus_all", metric=metrict)
        launch_pygad_destination(params, i, "pygad_main_destination_same_seed_plus_all", metric=metrict)


    for i in [106, 107, 108]:
        launch_spsa_destination(params, i, "spsa_main_destination_same_seed_plus_all", metric=metrict)


def experiment_misscaled_target():
    params = ["asc_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "asc_bike_mu", "b_tt_car_p_mu",
              "b_tt_car_d_mu", "b_tt_put_mu", "b_tt_bike_mu", "b_tt_ped"]

    target = Individual(seed=9001, param_list=params, fraction_of_pop=0.05)
    target.run()

    metrict = "TravelTime_All_sum_squared_error"
    metric_fair = "ModalSplit_Default_Splits_sum_squared_error"
    for i in [106]:
        launch_pyswarms(params, i, "erroneous_comparison_data", "PYSWARMSFair", metric=metric_fair, d=target)
        launch_pygad(params, i, "erroneous_comparison_data", "PYGADFair", metric=metric_fair, d=target)
        launch_spsa(params, i, "erroneous_comparison_data", "SPSAFair", metric=metric_fair, d=target)

    for i in [107]:
        launch_pyswarms(params, i, "erroneous_comparison_data", "PYSWARMS2", metric=metrict, d=target)
        launch_pygad(params, i, "erroneous_comparison_data", "PYGAD2", metric=metrict, d=target)
        launch_spsa(params, i, "erroneous_comparison_data", "SPSA2", metric=metrict, d=target)
        launch_my_algorithm_new(params, i, "erroneous_comparison_data", "MyAlgorithm2", algorithm_seed=i, sub_r=my_algorithm.subroutine_better_quantiles, d=target)
        launch_pyswarms(params, i, "erroneous_comparison_data", "PYSWARMSFair2", metric=metric_fair, d=target)
    launch_pygad(params, i, "erroneous_comparison_data", "PYGADFair2", metric=metric_fair, d=target)
    launch_spsa(params, i, "erroneous_comparison_data", "SPSAFair2", metric=metric_fair, d=target)



def experiment_random_target_individual(params):

    for seed in [43, 45, 47]:

        random.seed(seed)
        target = Individual(seed=seed, param_list=params)
        target.randomize_active_parameters()

        target.run()

        exp_name = "random_target_10_parameters_time_metric"
        build_folders(exp_name)
        target.save(SPECS.EXP_PATH + exp_name + "/data/target/" + str(seed))

        #launch_pygad(params, seed, exp_name, descriptor="pygad_seed" + str(seed), d=target, metric="TravelTime_Default_sum_squared_error")
        #launch_pyswarms(params, seed, exp_name, descriptor="pyswarms_seed" + str(seed), d=target, metric="TravelTime_Default_sum_squared_error")
        #launch_spsa(params, seed, exp_name, descriptor="spsa_seed" + str(seed), d=target, metric="TravelTime_Default_sum_squared_error")
        launch_my_algorithm(params, seed, exp_name, descriptor="myalgorithm_seed" + str(seed), d=target)


def further_Exp(params):
    for seed in [48, 49, 50]:

        random.seed(seed)
        target = Individual(seed=seed, param_list=params)
        target.randomize_active_parameters()
        target.run()

        exp_name = "random_target_10_parameters_time_metric"
        build_folders(exp_name)
        target.save(SPECS.EXP_PATH + exp_name + "/data/target/")

        launch_pygad(params, seed, exp_name, descriptor="pygad_seed" + str(seed), d=target, metric="TravelTime_Default_sum_squared_error")
        launch_pyswarms(params, seed, exp_name, descriptor="pyswarms_seed" + str(seed), d=target, metric="TravelTime_Default_sum_squared_error")
        launch_spsa(params, seed, exp_name, descriptor="spsa_seed" + str(seed), d=target, metric="TravelTime_Default_sum_squared_error")
        launch_my_algorithm(params, seed, exp_name, descriptor="myalgorithm_seed" + str(seed), d=target)



def _unnamed_launch_for_quantiles(params, name):
    target_seeds = list(range(100, 105))
    algo_seeds = list(range(42, 47))
    for target_seed in target_seeds:
        for algo_seed in algo_seeds:
            launch_my_algorithm_new(params, target_seed, name, "FixedQuantilesTarget"
                                    + str(target_seed) + "_Algo" + str(algo_seed),
                                    algorithm_seed=algo_seed, sub_r=my_algorithm.subroutine_fixed_quantiles)

            launch_my_algorithm_new(params, target_seed, name, "VariableQuantilesTarget"
                                    + str(target_seed) + "_Algo" + str(algo_seed),
                                    algorithm_seed=algo_seed, sub_r=my_algorithm.subroutine_better_quantiles)


def _unnamed_launch_for_better_guessing(params, name):
    target_seeds = list(range(100, 105))
    algo_seeds = list(range(42, 47))
    for target_seed in target_seeds:
        for algo_seed in algo_seeds:
            launch_my_algorithm_new(params, target_seed, name, "FixedQuantilesBetterBounds"
                                    + str(target_seed) + "_Algo" + str(algo_seed),
                                    algorithm_seed=algo_seed, sub_r=my_algorithm.subroutine_fixed_quantiles_better_bounds_guessing)

            launch_my_algorithm_new(params, target_seed, name, "VariableQuantilesBetterBounds"
                                    + str(target_seed) + "_Algo" + str(algo_seed),
                                    algorithm_seed=algo_seed, sub_r=my_algorithm.subroutine_better_quantiles_better_bounds_guessing)


def experiment_different_quantiles():
    params = ["asc_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "asc_bike_mu", "b_tt_car_p_mu",
              "b_tt_car_d_mu", "b_tt_put_mu", "b_tt_bike_mu", "b_tt_ped"]
    target_seeds = list(range(104, 105))
    algo_seeds = list(range(46, 47))
    for target_seed in target_seeds:
        for algo_seed in algo_seeds:
            launch_my_algorithm_new(params, target_seed, "MyExperimentQuantiles", "SimpleQuantile"
                                    + str(target_seed) + "_Algo" + str(algo_seed),
                                    algorithm_seed=algo_seed, sub_r=my_algorithm.subroutine_simple_quantile)
            launch_my_algorithm_new(params, target_seed, "MyExperimentQuantiles", "ThreeQuantiles"
                                    + str(target_seed) + "_Algo" + str(algo_seed),
                                    algorithm_seed=algo_seed, sub_r=my_algorithm.subroutine_medium_precision_quantile)

            launch_my_algorithm_new(params, target_seed, "MyExperimentQuantiles", "QuantilesFocusOnLong"
                                    + str(target_seed) + "_Algo" + str(algo_seed),
                                    algorithm_seed=algo_seed, sub_r=my_algorithm.subroutine_shifted_to_long_travel_precision_quantile)

            launch_my_algorithm_new(params, target_seed, "MyExperimentQuantiles", "HundredQuantiles"
                                    + str(target_seed) + "_Algo" + str(algo_seed),
                                    algorithm_seed=algo_seed, sub_r=my_algorithm.subroutine_high_precision_quantile)
    target_seed = 104
    algo_seed = 45
    launch_my_algorithm_new(params, target_seed, "MyExperimentQuantiles", "QuantilesFocusOnLong"
                                    + str(target_seed) + "_Algo" + str(algo_seed),
                                    algorithm_seed=algo_seed, sub_r=my_algorithm.subroutine_shifted_to_long_travel_precision_quantile)

    launch_my_algorithm_new(params, target_seed, "MyExperimentQuantiles", "HundredQuantiles"
                                    + str(target_seed) + "_Algo" + str(algo_seed),
                                    algorithm_seed=algo_seed, sub_r=my_algorithm.subroutine_high_precision_quantile)
def experiment_very_high_precision():
    params = ["asc_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "asc_bike_mu", "b_tt_car_p_mu",
              "b_tt_car_d_mu", "b_tt_put_mu", "b_tt_bike_mu", "b_tt_ped"]
    target_seeds = list(range(100, 105))
    algo_seeds = list(range(42, 47))
    for target_seed in target_seeds:
        for algo_seed in algo_seeds:
            launch_my_algorithm_new(params, target_seed, "MyExperimentVeryHighPrecision", "PreciseSubroutine"
                                    + str(target_seed) + "_Algo" + str(algo_seed),
                                    algorithm_seed=algo_seed, sub_r=my_algorithm.subroutine_extremely_high_precision)

def experiment_calibration_from_original_values():
    touched_params = ['asc_car_d_mu', 'asc_car_p_mu', 'asc_put_mu', 'asc_ped_mu', 'asc_bike_mu', 'b_tt_car_p_mu', 'b_tt_put_mu',
     'b_tt_bike_mu', 'b_tt_ped', 'female_on_asc_bike', 'female_on_asc_car_d', 'age_0_17_on_asc_car_p',
     'age_0_17_on_asc_bike', 'age_18_29_on_asc_car_d', 'age_18_29_on_asc_put', 'age_50_59_on_asc_ped',
     'age_60_69_on_asc_car_d', 'age_60_69_on_asc_ped', 'age_70_100_on_asc_car_d', 'age_70_100_on_asc_bike',
     'age_70_100_on_asc_put', 'age_70_100_on_asc_ped', 'student_on_asc_bike', 'student_on_asc_ped',
     'student_on_asc_car_d', 'student_on_asc_car_p', 'student_on_asc_put', 'beruft_on_asc_bike', 'beruft_on_asc_car_p',
     'beruft_on_asc_car_d', 'pkw_0_on_asc_ped', 'pkw_0_on_asc_bike', 'pkw_0_on_asc_car_p', 'pkw_0_on_asc_put',
     'pkw_1_on_asc_car_p', 'pkw_1_on_asc_put', 'inc_low_on_asc_bike', 'inc_low_on_asc_put', 'inc_high_on_asc_bike',
     'inc_high_on_asc_put', 'inc_low_on_asc_car_d', 'inc_high_on_asc_car_d', 'b_arbeit_car_d', 'b_arbeit_car_p',
     'b_arbeit_put', 'b_arbeit_bike', 'b_arbeit_ped', 'b_dienst_put', 'b_dienst_car_d', 'b_dienst_car_p',
     'b_dienst_bike', 'b_ausb_car_d', 'b_ausb_bike', 'b_eink_car_d', 'b_eink_car_p', 'b_eink_put', 'b_eink_bike',
     'b_freiz_car_d', 'b_freiz_car_p', 'b_freiz_put', 'b_freiz_bike', 'b_freiz_ped', 'b_service_car_d',
     'b_service_car_p', 'b_service_put', 'b_service_bike', 'b_service_ped', 'b_home_car_p', 'age_0_17_on_b_tt_car_p',
     'age_18_29_on_b_tt_car_p', 'beruft_on_b_tt_car_d', 'beruft_on_b_tt_bike', 'b_tt_ausb_ped', 'b_tt_freiz_ped']
    reqs = ['workday', 'gender', 'employment', 'age', 'activityType',
            'tripMode', 'previousMode', 'economicalStatus', 'nominalSize', 'totalNumberOfCars']
    all_params = simulation.default_yaml().mode_config().get_all_parameter_names_on_requirements(reqs)
    for target_seed in range(106, 108):
        for algo_seed in range(42, 44):

            #launch_my_algorithm_new(touched_params, target_seed, "RecreatingManualTuningProcess", "OnlyChangedParams"
            #                        + str(target_seed) + "_Algo" + str(algo_seed),
            #                        algorithm_seed=algo_seed, individual_seed=target_seed, sub_r=my_algorithm.subroutine_better_quantiles, use_existing_config=True)
            launch_my_algorithm_new(all_params, target_seed, "RecreatingManualTuningProcess", "AllModeParams"
                                    + str(target_seed) + "_Algo" + str(algo_seed),
                                    algorithm_seed=algo_seed, individual_seed=target_seed, sub_r=my_algorithm.subroutine_better_quantiles, use_existing_config=True)



def experiment_which_error_correction_method_is_better():
    params = ["asc_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "asc_bike_mu", "b_tt_car_p_mu",
              "b_tt_car_d_mu", "b_tt_put_mu", "b_tt_bike_mu", "b_tt_ped"]
    _unnamed_launch_for_better_guessing(params, "MyExperimentBetterErrorGuessing")

def experiment_are_variable_quantiles_good():
    params = ["asc_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "asc_bike_mu", "b_tt_car_p_mu",
              "b_tt_car_d_mu", "b_tt_put_mu", "b_tt_bike_mu", "b_tt_ped"]
    _unnamed_launch_for_quantiles(params, "MyExperimentVariableQuantilesFixedOutput")

def experiment_are_variable_quantiles_good_for_cost():
    params = ["b_cost", "b_cost_put", "b_inc_high_on_b_cost", "b_inc_high_on_b_cost_put"]
    _unnamed_launch_for_quantiles(params, "MyExperimentVariableQuantilesCostFixedOutput")



def experiment_tuning_alpha_before_beta():
    params = ["asc_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "asc_bike_mu", "b_tt_car_p_mu",
              "b_tt_car_d_mu", "b_tt_put_mu", "b_tt_bike_mu", "b_tt_ped"]
    target_seeds = list(range(100, 105))
    algo_seeds = list(range(42, 47))
    for target_seed in target_seeds:
        for algo_seed in algo_seeds:
            #launch_my_algorithm_new(params, target_seed, "tuningAlphabeforeBeta", "AlphaBeforeBeta"
            #                        + str(target_seed) + "_Algo" + str(algo_seed),
            #                        algorithm_seed=algo_seed, sub_r=my_algorithm.subroutine_alpha_before_beta)

            launch_my_algorithm_new(params, target_seed, "tuningAlphabeforeBeta", "BetaBeforeAlpha"
                                    + str(target_seed) + "_Algo" + str(algo_seed),
                                    algorithm_seed=algo_seed, sub_r=my_algorithm.subroutine_default)

def _full_launch_helper(subroutine, experiment_name, additional_descriptor):
    reqs = ['workday', 'gender', 'employment', 'age', 'activityType',
            'tripMode', 'previousMode', 'economicalStatus', 'nominalSize', 'totalNumberOfCars']
    params = simulation.default_yaml().mode_config().get_all_parameter_names_on_requirements(reqs)
    target_seeds = list(range(100, 102))
    algo_seeds = list(range(42, 44))
    for target_seed in target_seeds:
        for algo_seed in algo_seeds:
            #launch_my_algorithm_new(params, target_seed, "MyAlgorithmFullMode", "FixedQuantilesTarget"
            #                        + str(target_seed) + "_Algo" + str(algo_seed),
            #                        algorithm_seed=algo_seed, sub_r=my_algorithm.subroutine_fixed_quantiles,
            #                        metric="TravelTime_All_sum_squared_error")
            launch_my_algorithm_new(params, target_seed, experiment_name, additional_descriptor
                                    + str(target_seed) + "_Algo" + str(algo_seed),
                                    algorithm_seed=algo_seed, sub_r=subroutine,
                                    metric="TravelTime_All_sum_squared_error")

def experiment_full_launch_my_algorithm():
    _full_launch_helper(my_algorithm.subroutine_better_quantiles, "MyAlgorithmFullMode", "FixedQuantilesTarget")


def experiment_full_launch_two_passes_my_algorithm():
    _full_launch_helper(my_algorithm.subroutine_full_data_two_passes, "MyAlgorithmFullTwoPasses", "ImprovedDetailPasses")
#https://github.com/Robin-Andre/thesis-python-scripts.git
if __name__ == "__main__":
    PARAMS = ["asc_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "asc_bike_mu", "b_tt_car_p_mu",
              "b_tt_car_d_mu", "b_tt_put_mu", "b_tt_bike_mu", "b_tt_ped"]
    #experiment_spsa_target_has_same_seed_time_metric(PARAMS)
    #experiment_pyswarms_target_has_same_seed_time_metric(PARAMS)
    #experiment_pygad_target_has_same_seed_time_metric(PARAMS)
    experiment_calibration_from_original_values()

    #experiment_misscaled_target()
    #experiment_meta_heuristics_for_all_mode_parameters()
    #experiment_different_quantiles()
    #experiment_meta_heuristics_destination_same_seed_with_all_modes()
    #experiment_tuning_alpha_before_beta()

    #experiment_very_high_precision()

    #experiment_which_error_correction_method_is_better()
    #experiment_are_variable_quantiles_good()
    #experiment_are_variable_quantiles_good_for_cost()
    exit()
    launch_my_algorithm_new(PARAMS, 2, "myalgo_test_run", descriptor="Diffseed2_2iters", algorithm_seed=13)
    #experiment_meta_heuristics_destination_same_seed_with_business()
    exit()
    experiment_meta_heuristics_destination_same_seed()

    #PARAMS = ["asc_car_d_mu", "age_0_17_on_b_tt_ped"]
   # PARAMS = ["asc_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "asc_bike_mu", "b_tt_car_p_mu", "b_tt_car_d_mu", "b_tt_put_mu", "b_tt_bike_mu", "b_tt_ped"]
    #PARAMS = ["female_on_asc_ped"]
    #yaml = simulation.default_yaml()
    #print(yaml.mode_config().get_all_parameter_names_on_requirements(["tripMode", "age", "gender"]))

    #print(yaml.destination_config().get_all_parameter_names_on_requirements(["age", "gender"]))
    #launch_my_algorithm_new(PARAMS, 2, "myalgo_test_run", descriptor="Diffseed2_2iters")#
    exit(0)
    PARAMS = ["asc_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "asc_bike_mu", "b_tt_car_p_mu", "b_tt_car_d_mu", "b_tt_put_mu", "b_tt_bike_mu", "b_tt_ped", "female_on_asc_ped", "age_18_29_on_b_tt_car_d"]
    #experiment_pyswarms_target_has_same_seed(PARAMS)
    #experiment_pyswarms_target_has_same_seed_time_metric(PARAMS)
    launch_pyswarms(PARAMS, 52, "Detailed_test", descriptor="pyswarms_seed_detailedtest", metric="TravelTime_Default_sum_squared_error")


#experiment_pygad_target_has_same_seed_time_metric(PARAMS)
    #experiment_pygad_target_has_same_seed(PARAMS)
    exit(0)
#experiment_random_target_individual(PARAMS)
    #further_Exp(PARAMS)
    #exit(0)

    launch_my_algorithm_new(PARAMS, 2, "myalgo_10_parameters", descriptor="Diffseed2_2iters")
    #launch_my_algorithm(PARAMS, 3, "myalgo_10_parameters", descriptor="Diffseed3_2Iters")
    exit(0)

    launch_pyswarms(PARAMS, 103, "pyswarms")
    launch_pyswarms(PARAMS, 103, "pyswarms", descriptor="TEST")
    exit(0)

    launch_spsa(PARAMS, 102, "TE")
    exit(0)
    ex_name = "pygad_10_parameters"
    launch_pygad(PARAMS, 101, ex_name)
    launch_pygad(PARAMS, 102, ex_name)
    launch_pygad(PARAMS, 103, ex_name)
    #experiment_pyswarms_target_has_same_seed(PARAMS)
    #experiment_spsa_target_has_same_seed(PARAMS)


