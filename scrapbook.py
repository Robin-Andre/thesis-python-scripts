import math
import unittest
from configurations.parameter import Parameter
from calibration.evolutionary.individual import Individual
from calibration.evolutionary.population import Population
import mobitopp_execution as simulation
from configurations import SPECS


class MyTestCase(unittest.TestCase):
    @unittest.skip
    def test_random(self):
        for string_val in ["asc_car_d_mu", "asc_car_p_mu", "asc_bike_mu", "asc_put_mu"]:
            p = Population()
            _, target = simulation.load("tests/resources/compare_individual")
            p.set_target(target)

            vals = []
            modal_split_df = target._get_modal_split()
            for i in range(25, 75):
                x = Individual(9001, [string_val])

                x.make_basic()
                # Approximately getting a fair distribution
                x["asc_ped_mu"].set(-15)
                x["asc_car_p_mu"].set(-2)
                x["asc_car_d_mu"].set(-1)
                x["asc_put_mu"].set(1)
                print(x[string_val].value)
                x[string_val].set(x[string_val].value + i / 2)
                print(x[string_val].value)
                x.run()
                x.set_fitness(target)
                y = x.data._get_modal_split().loc[3, "count"]
                cur_modal_split = x.data._get_modal_split()
                cur_modal_split.rename(columns={"count": "count" + str(i)}, inplace=True)
                modal_split_df = modal_split_df.join(cur_modal_split, how="left")
                p.append(x)

                vals.append((i, y))
            p.draw_boundaries_modal_split(sort=False)
            modal_split_df.to_csv(SPECS.EXP_PATH + string_val + "Addendum.csv")

    def __helper(self, text_vals, func, i_values, bonus_append="", fraction_of_pop=0.02, broken_asc="", broken_val=0):
        for string_val in text_vals:
            parameter = Parameter(string_val)
            p = Population()
            default_ind = Individual(9001, [string_val], fraction_of_pop=fraction_of_pop)
            default_ind.make_basic(nullify_exponential_b_tt=True)
            default_ind.run()
            target = default_ind.data
            p.set_target(target)

            modal_split_df = target._get_modal_split()
            for i in i_values:
                x = Individual(9001, [string_val], fraction_of_pop)

                x.make_basic(nullify_exponential_b_tt=True)
                # Approximately getting a fair distribution
                print(x[string_val].value)
                x[string_val].set(func(i))

                if broken_asc is not "":
                    x[broken_asc].set(broken_val)

                print(x[string_val].value)
                x.run()
                x.set_fitness(target)

                cur_modal_split = x.data._get_modal_split()
                cur_modal_split.rename(columns={"count": "count" + str(i)}, inplace=True)
                modal_split_df = modal_split_df.join(cur_modal_split, how="left")
                p.append(x)

            p.draw_boundaries_modal_split(sort=False)
            big = p.draw_all_traveltime(parameter.requirements["tripMode"])
            big_dist = p.draw_all_traveldistance(parameter.requirements["tripMode"])
            #print(big_dist)
            big.to_csv(SPECS.EXP_PATH + "b_tt_csvs/" + string_val + bonus_append + "time.csv")
            big_dist.to_csv(SPECS.EXP_PATH + "b_tt_csvs/" + string_val + bonus_append + "dist.csv")
            modal_split_df.to_csv(SPECS.EXP_PATH + string_val + "othernullmethod.csv")

    @unittest.skip
    def test_make_basic2(self):
        values = ["asc_car_d_mu", "asc_car_p_mu", "asc_ped_mu", "asc_bike_mu", "asc_put_mu"]
        i_values = range(-50, 50)
        self.__helper(values, lambda x: x / 2, i_values)

    @unittest.skip
    def test_make_basic3(self):
        values = ["b_tt_car_d_mu", "b_tt_car_p_mu", "b_tt_put_mu", "b_tt_bike_mu"]
        i_values = [-x / 50 for x in range(1, 51)]
        self.__helper(values, lambda x: math.log(-x), i_values)

    @unittest.skip
    def test_detailed_time_plots(self):
        values = ["b_tt_car_d_mu", "b_tt_car_p_mu", "b_tt_put_mu", "b_tt_bike_mu"]
        i_values = [-x / 50 for x in range(1, 11)]
        self.__helper(values, lambda x: math.log(-x), i_values, bonus_append="FullPopbonus", fraction_of_pop=1)

    @unittest.skip
    def test_bad_b_tt_but_good_asc(self):
        values = ["b_tt_car_d_mu"]
        i_values = [-x / 50 for x in range(1, 5)] # -1/50 -2/50 -3/50 -4/50
        self.__helper(values, lambda x: math.log(-x), i_values, bonus_append="SmallBrokenAsc", broken_asc="asc_car_d_mu")

    @unittest.skip
    def test_bad_b_tt_but_multiple_asc(self):
        values = ["b_tt_car_d_mu"]
        i_values = [-x / 50 for x in range(2, 3)]
        for i in [-2, -1, 0, 1, 2]:
            self.__helper(values, lambda x: math.log(-x), i_values, bonus_append="Weird" + str(i), broken_asc="asc_car_d_mu", broken_val=i)

    @unittest.skip
    def test_make_basic4(self):
        values = ["b_cost", "b_cost_put", "b_u_put", "b_park_car_d", "b_logsum_acc_put"]
        i_values = [x / 50 for x in range(1, 51)]
        self.__helper(values, lambda x: x / 2, i_values, bonus_append="WhatdoIwritehere")