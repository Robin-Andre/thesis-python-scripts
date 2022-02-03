import random
import time

from calibration.evolutionary import selection, replace, individual, evo_strategies
from calibration.evolutionary.population import Population
import mobitopp_execution as simulation
from configurations import SPECS


def run_experiment(seed, population, repetition, pl_key):
    random.seed(seed)

    population.load("../../tests/resources/test_population")
    _, data = simulation.load("../../tests/resources/compare_individual")
    population.set_target(data)
    population.fitness_for_all_individuals()
    for i in range(repetition):
        evo_strategies.simple_combine(population)
    population.logger.append_to_csv(", " + str(seed) + ", " + pl_key)
    return population.logger.print_csv()


def write(result, experiment, seed):
    with open(SPECS.EXP_PATH + f"ParameterExperiment/{experiment}_{seed}.csv", "w+") as file:
        file.write(result)


PL = [("no_elasticity",
       ["asc_car_d_mu", "b_tt_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "b_tt_car_p_mu", "b_tt_put_mu",
        "b_tt_ped", "asc_bike_mu", "b_tt_bike_mu", "b_cost", "b_cost_put", "asc_car_d_sig", "asc_car_p_sig",
        "asc_put_sig",
        "asc_ped_sig", "asc_bike_sig", "b_tt_car_p_sig", "b_tt_car_d_sig", "b_tt_put_sig", "b_tt_bike_sig", "b_u_put",
        "b_logsum_acc_put"]),
      ("no_sig_no_elas",
       ["asc_car_d_mu", "b_tt_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "b_tt_car_p_mu", "b_tt_put_mu",
        "b_tt_ped", "asc_bike_mu", "b_tt_bike_mu", "b_cost", "b_cost_put", "b_u_put",
        "b_logsum_acc_put"]),
      ("no_btt",
       ["asc_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu",
        "asc_bike_mu", "b_tt_bike_mu", "b_cost", "b_cost_put", "asc_car_d_sig", "asc_car_p_sig", "asc_put_sig",
        "asc_ped_sig", "asc_bike_sig", "b_u_put",
        "b_logsum_acc_put", "elasticity_acc_put", "b_park_car_d", "elasticity_parken"]),
      ("no_btt_no_elas",
       ["asc_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu",
        "asc_bike_mu", "b_tt_bike_mu", "b_cost", "b_cost_put", "asc_car_d_sig", "asc_car_p_sig", "asc_put_sig",
        "asc_ped_sig", "asc_bike_sig", "b_u_put",
        "b_logsum_acc_put"]),
      ("full",
       ["asc_car_d_mu", "b_tt_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "b_tt_car_p_mu", "b_tt_put_mu",
        "b_tt_ped", "asc_bike_mu", "b_tt_bike_mu", "b_cost", "b_cost_put", "asc_car_d_sig", "asc_car_p_sig",
        "asc_put_sig",
        "asc_ped_sig", "asc_bike_sig", "b_tt_car_p_sig", "b_tt_car_d_sig", "b_tt_put_sig", "b_tt_bike_sig", "b_u_put",
        "b_logsum_acc_put", "elasticity_acc_put", "b_park_car_d", "elasticity_parken"])
      ]


def main():
    output = []
    repetitions = 50
    for pl_key, pl_value in PL:
        for seed in range(42, 47):

            population = Population(select_func=selection.double_tournament_selection, replace_func=replace.fancy_replace,
                                 individual_constructor=individual.Individual, seed=101, param_vector=pl_value)
            result = run_experiment(seed, population, repetitions, pl_key)
            write(result, pl_key)
            output.append(result)

    csv = "\n".join(output)
    print(csv)
    with open(SPECS.EXP_PATH + "ParameterExperiment.csv", "w+") as file:
        file.write(csv)


if __name__ == '__main__':
    main()
