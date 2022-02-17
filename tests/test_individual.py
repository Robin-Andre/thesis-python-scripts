
import unittest

from matplotlib import pyplot as plt

import visualization
from calibration import tuning
from calibration.evolutionary.individual import Individual

from calibration.evolutionary.population import Population

from configurations.observations import ModalSplitObservation, TimeModeObservation


class MyTestCase(unittest.TestCase):

    def test_load(self):
        x = Individual(0, [])
        try:
            x.load("resources/test_population/individual_0")
        except FileNotFoundError:
            self.fail("Test did not load the individual!")

        self.assertAlmostEqual(x["asc_car_d_mu"].value, 5.352656054767767)
        self.assertAlmostEqual(x["asc_put_sig"].value, -1.5723)
        self.assertAlmostEqual(x["b_tt_car_d_mu"].value, -0.8685707430564293)
        self.assertEqual(x.yaml.get_fraction_of_population(), 1)


    def test_run(self):
        x = Individual(21, [])
        x.load("resources/example_config_load")
        x.yaml.set_fraction_of_population(0.02)
        x.run(["tripMode", "gender", "age"])
        x.save("resources/even_more_detailed_individual")

    def test_detailed_ind(self):
        x = Individual(21, [])
        x_d = Individual(22, [])
        x.load("resources/detailed_individual")
        x_d.load("resources/even_more_detailed_individual")
        #y = x.data.travel_time.get_data_frame()
        #visualization.two_level_travel_time(y, "gender")
        d = x_d.data.get_grouped_modal_split(["age", "gender"])
        visualization.draw_grouped_modal_split(d)
        return
        y = x_d.data.travel_time.get_data_frame()
        visualization.generic_plot(y, "age", "count", "durationTrip", color_seperator="tripMode")

        y = x_d.data.traffic_demand.accumulate(["age", "tripMode"])
        visualization.generic_plot(y, "age", "active_trips", "time", color_seperator="tripMode")
        return
        visualization.two_level_travel_time(y, "gender")
        return
        x.data.reduce(["gender"])
        z = x.data.travel_time.get_data_frame()

        visualization.generic_travel_time(z, "gender")

    def test_tuning_effect_subset_parameter(self):
        x_d = Individual(22, [])
        x_d.load("resources/even_more_detailed_individual")
        d = x_d.data.get_grouped_modal_split(["age", "gender"])


        visualization.draw_grouped_modal_split(d)
        x_d["age_60_69_on_asc_car_d"].set(-10)
        x_d.run(["tripMode", "gender", "age"])

        d = x_d.data.get_grouped_modal_split(["age", "gender"])

        visualization.draw_grouped_modal_split(d)
        return



    def test_column_specification(self):
        x = Individual(21, [])
        x_d = Individual(22, [])
        x.load("resources/detailed_individual")
        x_d.load("resources/even_more_detailed_individual")

        self.assertEqual(x.data.columns().sort(), ["gender", "tripMode"].sort())
        self.assertEqual(x_d.data.columns().sort(), ["gender", "age", "tripMode"].sort())

    def test_subset_selection(self):
        x_d = Individual(22, [])
        x_d.load("resources/even_more_detailed_individual")
        self.assertAlmostEqual(x_d.data.get_modal_split_by_param(x_d["age_0_17_on_asc_bike"]), 0.395593489479)

    def test_subset_selection_invalid(self):
        x_d = Individual(22, [])
        x_d.load("resources/detailed_individual")
        self.assertRaises(AssertionError, x_d.data.get_modal_split_by_param, x_d["age_0_17_on_asc_bike"])



    def test_tuning_b_tt(self):
        x = Individual(21, [])
        y = Individual(13, [])
        z = Individual("number", [])
        x.load("resources/test_population/individual_0")
        y.load("resources/compare_individual")
        parameter = x["b_tt_car_d_mu"]
        z = x.copy()
        z[parameter].set(parameter.observe(x, y.data))
        print(z[parameter])
        z.run()

        new_val = parameter.observe_detailed(x, z, y.data)
        z_new = z.copy()
        z_new[parameter].set(new_val)
        z_new.run()
        #parameter.observe(z_new, y.data)

        new_val = parameter.observe_detailed(z_new, z, y.data)

        z[parameter].set(new_val)
        z.run()
        new_val = parameter.observe_detailed(z_new, z, y.data)
        z_new[parameter].set(new_val)
        z_new.run()
        parameter.observe(z_new, y.data)


    def test_tuning(self):
        x = Individual(21, [])
        y = Individual(13, [])
        z = Individual("number", [])
        x.load("resources/test_population/individual_0")

        y.load("resources/compare_individual")
        parameter = x["asc_car_d_mu"]
        improved_ind = tuning.tune(x, y.data, parameter)
        improved_ind.data.draw_modal_split(y.data)

    def test_tuning_strategy1(self):
        x = Individual(21, [])
        y = Individual(13, [])
        x.load("resources/test_population/individual_0")

        y.load("resources/compare_individual")
        improved_ind, best = tuning.tune_strategy1(x, y.data, epsilon=0.02)
        improved_ind.data.draw_modal_split(y.data)
        best.data.draw_modal_split(y.data)


    def test_tuning_with_new(self):
        p = Population()
        y = p.set_random_individual_as_target()
        a, b, c = y.draw()
        a.show()
        b.show()
        c.show()
        print(y.yaml.mode_config())
        x = p.random_individual()

        x, best = tuning.tune_strategy1(x, y.data, epsilon=0.001)
        a_1, b_1, c_1 = x.data.draw(reference=y.data)
        a_2, b_2, c_2 = best.data.draw(reference=y.data)

        a_1.show()
        a_2.show()

        b_1.show()
        b_2.show()

        c_1.show()
        c_2.show()




    def test_tuning_strategy2(self):
        x = Individual(21, [])
        y = Individual(13, [])
        x.load("resources/test_population/individual_0")

        y.load("resources/compare_individual")
        improved_ind, best = tuning.tune_strategy2(x, y.data)
        improved_ind.data.draw_modal_split(y.data)

    def test_tuning_combination(self):
        x = Individual(21, [])
        y = Individual(13, [])
        x.load("resources/test_population/individual_0")

        y.load("resources/compare_individual")
        improved_ind, best = tuning.tune_strategy2(x, y.data)

        a, b, c = best.data.draw(reference=y.data)
        a.show()
        b.show()
        c.show()

        a, b, c = improved_ind.data.draw(reference=y.data)
        a.show()
        b.show()
        c.show()


        improved_ind.data.draw_modal_split(y.data)
        improved_ind = tuning.tune_strategy1(improved_ind, y.data)

        a, b, c = improved_ind.data.draw(reference=y.data)
        a.show()
        b.show()
        c.show()


    def test_tuning_asc(self):
        x = Individual(21, [])
        y = Individual(13, [])
        z = Individual("number", [])
        x.load("resources/test_population/individual_0")

        y.load("resources/compare_individual")
        parameter = x["asc_car_d_mu"]
        z = x.copy()
        x.data.draw_modal_split(y.data)
        z[parameter].set(parameter.observe(x, y.data))
        print(z[parameter])
        z.run()
        z.data.draw_modal_split(y.data)
        new_val = parameter.observe_detailed(x, z, y.data)
        z_new = z.copy()
        z_new[parameter].set(new_val)
        z_new.run()
        z_new.data.draw_modal_split(y.data)
        #parameter.observe(z_new, y.data)

        new_val = parameter.observe_detailed(z_new, z, y.data)

        z[parameter].set(new_val)
        z.run()
        z.data.draw_modal_split(y.data)
        new_val = parameter.observe_detailed(z_new, z, y.data)
        z_new[parameter].set(new_val)
        z_new.run()
        z_new.data.draw_modal_split(y.data)
        parameter.observe(z_new, y.data)


    def test_bad_observation_function_is_caught(self):
        self.assertRaises(AssertionError, TimeModeObservation, lambda x: x / 2, lambda x: 3 * x)


    def test_access_dict_by_name_or_parameter_object(self):
        x = Individual(21, [])
        y = Individual(13, [])
        x.load("resources/test_population/individual_0")
        y.load("resources/compare_individual")
        p = x["asc_car_d_mu"]

        p2 = y[p]
        self.assertNotEqual(p2.value, p.value)
        p.set(13)
        self.assertEqual(p.value, 13)
        self.assertNotEqual(p2.value, 13)

    def test_copy(self):
        x = Individual(21, [])
        x["asc_car_d_mu"].set(9)
        y = x.copy()
        self.assertEqual(y["asc_car_d_mu"].value, 9)
        y["asc_car_d_mu"].set(2)
        self.assertEqual(x["asc_car_d_mu"].value, 9)

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
