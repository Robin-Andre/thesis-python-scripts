import math
import unittest

from matplotlib import pyplot as plt

import visualization
from calibration.evolutionary.individual import Individual
import mobitopp_execution as simulation
from calibration.evolutionary.population import Population
from configurations import SPECS
from configurations.parameter import Parameter


class MyTestCase(unittest.TestCase):

    def test_make_basic(self):
        for string_val in ["asc_car_d_mu", "asc_car_p_mu", "asc_bike_mu", "asc_put_mu"]:
            p = Population()
            _, target = simulation.load("resources/compare_individual")
            p.set_target(target)

            vals = []
            modal_split_df = target.get_modal_split()
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
                y = x.data.get_modal_split().loc[3, "count"]
                cur_modal_split = x.data.get_modal_split()
                cur_modal_split.rename(columns={"count": "count" + str(i)}, inplace=True)
                modal_split_df = modal_split_df.join(cur_modal_split, how="left")
                p.append(x)

                vals.append((i, y))
            p.draw_boundaries_modal_split(sort=False)
            modal_split_df.to_csv(SPECS.EXP_PATH + string_val + "Addendum.csv")

    def __helper(self, text_vals, func, i_values, bonus_append="", fraction_of_pop=0.02):
        for string_val in text_vals:
            parameter = Parameter(string_val)
            p = Population()
            default_ind = Individual(9001, [string_val], fraction_of_pop=fraction_of_pop)
            default_ind.make_basic(nullify_exponential_b_tt=True)
            default_ind.run()
            target = default_ind.data
            p.set_target(target)

            modal_split_df = target.get_modal_split()
            for i in i_values:
                x = Individual(9001, [string_val])

                x.make_basic(nullify_exponential_b_tt=True)
                # Approximately getting a fair distribution
                print(x[string_val].value)
                x[string_val].set(func(i))

                print(x[string_val].value)
                x.run()
                x.set_fitness(target)

                cur_modal_split = x.data.get_modal_split()
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

    def test_make_basic2(self):
        values = ["asc_car_d_mu", "asc_car_p_mu", "asc_ped_mu", "asc_bike_mu", "asc_put_mu"]
        i_values = range(-50, 50)
        self.__helper(values, lambda x: x / 2, i_values)


    def test_make_basic3(self):
        values = ["b_tt_car_d_mu", "b_tt_car_p_mu", "b_tt_put_mu", "b_tt_bike_mu"]
        i_values = [-x / 50 for x in range(1, 51)]
        self.__helper(values, lambda x: math.log(-x), i_values)

    def test_detailed_time_plots(self):
        values = ["b_tt_car_d_mu", "b_tt_car_p_mu", "b_tt_put_mu", "b_tt_bike_mu"]
        i_values = [-x / 10 for x in range(1, 5)]
        self.__helper(values, lambda x: math.log(-x), i_values, bonus_append="FullPop", fraction_of_pop=1)


    def test_make_basic4(self):
        values = ["b_cost", "b_cost_put", "b_u_put", "b_park_car_d", "b_logsum_acc_put"]
        i_values = [x / 50 for x in range(1, 51)]
        self.__helper(values, lambda x: x / 2, i_values, bonus_append="WhatdoIwritehere")

    def test_change_value(self):
        x = Individual(9001, [])
        x["asc_car_d_mu"].set(34)
        self.assertEqual(x["asc_car_d_mu"].value, 34)

    def test_rand_remove(self):
        vals = [(-50, -0.1055588731090511), (-49, -0.10105606281604453), (-48, -0.09659328044872587),
                (-47, -0.09063301164965534), (-46, -0.08573078137780653), (-45, -0.0786214593470943),
                (-44, -0.07190629643369892), (-43, -0.0639742150109478), (-42, -0.05560301312839265),
                (-41, -0.047302338964356386), (-40, -0.0387642249663962), (-39, -0.029654135323851055),
                (-38, -0.021000110074182093), (-37, -0.012062072454837341), (-36, -0.0023845289375048206),
                (-35, 0.009279992778086998), (-34, 0.021488983428429476), (-33, 0.03238680434018362),
                (-32, 0.04419208524382906), (-31, 0.058342618330341434), (-30, 0.07333362655709419),
                (-29, 0.09080529599444007), (-28, 0.10945539857127087), (-27, 0.12953135640203667),
                (-26, 0.15165422857932015), (-25, 0.17559332308262166), (-24, 0.20055412637309789),
                (-23, 0.2269145705046684), (-22, 0.2547639886358702), (-21, 0.28320639207498904),
                (-20, 0.3120378699151829), (-19, 0.34060209736424624), (-18, 0.3713509248765564),
                (-17, 0.40179253456234754), (-16, 0.43333440079657615), (-15, 0.46526448005159415),
                (-14, 0.4983041279443816), (-13, 0.5316456804213257), (-12, 0.5674272882938287),
                (-11, 0.6009209354992449), (-10, 0.6348026366892188), (-9, 0.6703529804172932),
                (-8, 0.7048766505028343), (-7, 0.7358209083796837), (-6, 0.7647411154304709), (-5, 0.7900792727914896),
                (-4, 0.8094454083670605), (-3, 0.8255203561749637), (-2, 0.8381373354827308), (-1, 0.8471489029792936)]
        xva = [x[0] for x in vals]
        yva = [x[1] for x in vals]
        plt.plot(xva, yva)
        plt.show()


if __name__ == '__main__':
    unittest.main()
