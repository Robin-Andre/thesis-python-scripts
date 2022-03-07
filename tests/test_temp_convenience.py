import unittest

import numpy as np
import pandas
from matplotlib import pyplot as plt

import evaluation
import visualization
from calibration import tuning
from calibration.evolutionary.individual import Individual, DestinationIndividual
from calibration.evolutionary.population import Population
from metrics.data import Data
from metrics.trafficdemand import TrafficDemand


def _helper(x, d):
    x.run()
    a, b, c = x.draw(reference=d.data)
    b.show()
    c.show()
    #x.data.zone_destination.draw(reference=d.data.zone_destination)



"""
Fill this test case with all the convenience clicker tests to speed up the process
"""
#@unittest.skip
class ConvenienceClickToExecute(unittest.TestCase):


    @unittest.skip
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

    @unittest.skip
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

    @unittest.skip
    def test_tuning_strategy2(self):
        x = Individual(21, [])
        y = Individual(13, [])
        x.load("resources/test_population/individual_0")

        y.load("resources/compare_individual")
        improved_ind, best = tuning.tune_strategy2(x, y.data)
        improved_ind.data.draw_modal_split(y.data)

    @unittest.skip
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

    @unittest.skip
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

    @unittest.skip
    def test_tuning_strategy1(self):
        x = Individual(21, [])
        y = Individual(13, [])
        x.load("resources/test_population/individual_0")

        y.load("resources/compare_individual")
        improved_ind, best = tuning.tune_strategy1(x, y.data, epsilon=0.02)
        improved_ind.data.draw_modal_split(y.data)
        best.data.draw_modal_split(y.data)

    @unittest.skip
    def test_tuning(self):
        x = Individual(21, [])
        y = Individual(13, [])
        z = Individual("number", [])
        x.load("resources/test_population/individual_0")

        y.load("resources/compare_individual")
        parameter = x["asc_car_d_mu"]
        improved_ind = tuning.tune(x, y.data, parameter)
        improved_ind.data.draw_modal_split(y.data)

    @unittest.skip
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


    """
    Tests the effect of a specialized parameter and plots the result. Meeting 21.2
    """


    def test_tuning_effect_subset_parameeter_copy(self):
        x_d = Individual(22, [])
        x_d.load("resources/even_more_detailed_individual")
        x_d.set_requirements(["tripMode", "gender", "age"])
        d = x_d.data.get_grouped_modal_split(["age", "gender"])

        visualization.draw_grouped_modal_split(d)
        x_d["age_60_69_on_asc_car_d"].set(-10)
        x_d.run()

        d = x_d.data.get_grouped_modal_split(["age", "gender"])

        visualization.draw_grouped_modal_split(d)
        return

    @unittest.skip("convenience click method, not a test")
    def test_run(self):
        x = Individual(21, [])
        x.load("resources/example_config_load")
        x.yaml.set_fraction_of_population(0.02)
        x.set_requirements(["tripMode", "workday"])
        x.run()
        x.save("resources/workday_individual")


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

    def test_draw(self):
        data = Data()
        data.load("resources/example_config_load/results/")
        data2 = Data()
        data2.load("resources/example_config_load2/results/")
        a, b, c = data.draw(reference=data2)
        a.show()
        b.show()
        c.show()
        a, b, c = data.draw_smooth(reference=data2)
        a.show()
        b.show()
        c.show()

    def test_better_modal_split(self):
        data = Data()
        data.load("resources/example_config_load/results/")
        x = data.get_modal_split_based_by_time(1)
        y = x.unstack(level=1).T
        y.plot()
        plt.show()

    def helper(self, q, string):
        visualization.generic_td_demand(q.accumulate([string]), string)

    def helper2(self, q, string):
        visualization.generic_travel_time(q, string)

    def test_full_extraction(self):
        x = evaluation.default_test_merge()
        q = TrafficDemand.from_raw_data(x)
        all_possible_vals = ["tripMode", "activityType", "age", "employment", "gender", "hasCommuterTicket",
                             "economicalStatus", "totalNumberOfCars", "nominalSize"]

        for x in all_possible_vals:
            self.helper(q, x)
        return

    def test_full_time_extraction(self):
        x = evaluation.default_test_merge()
        q = evaluation.create_travel_time_data_new(x)
        all_possible_vals = ["tripMode", "activityType", "age", "employment", "gender", "hasCommuterTicket",
                             "economicalStatus", "totalNumberOfCars", "nominalSize"]

        for x in all_possible_vals:
            self.helper2(q, x)
        return


    def nontest_geo_plot(self):
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        print(raw_data.iloc[0])
        raw_data = raw_data.iloc[0:4]
        evaluation.check_data(raw_data)

    def nontest_plot_data_rename_pls(self):
        numpy_data = np.array([[1, 4, 0],  # -XXX------
                               [0, 5, 0],  # XXXXX-----
                               [2, 8, 1],  # --XXXXXX--
                               [2, 7, 1]   # --XXXXX---
                               ])
        expected_active_trips = [1, 2, 4, 4, 3, 2, 2, 1]
        df = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]), columns=["tripBegin", "tripEnd", "tripMode"]).groupby("tripMode")
        for key in df.groups:
            print(f"The key is{key}")
        print(df.get_group(1))
        temp_df = df.apply(lambda x: evaluation.create_plot_data(x))
        print(temp_df)
        temp_df = temp_df.droplevel(level=1)  # This is the level I wanna reach
        print(temp_df)
        temp_df = temp_df.groupby("time").sum()
        print(temp_df)


    # TODO this is not a test
    def nontest_broken_data_set(self):
        data = metrics.data.Data()
        data.load("resources/asc_car_d_sig10/results/")
        data.travel_time.draw_distribution(mode=3)
        #data.draw_distributions()
    # TODO this is not a test
    def nontest_difference_on_incomplete_data(self):
        numpy_data = np.array([[1, 0, 4],
                               [2, 0, 1],
                               ])
        df1 = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]), columns=["distanceInKm", "tripMode", "amount"])
        td1 = metrics.traveldistance.TravelDistance()
        td1.data_frame = df1
        numpy_data = np.array([[1, 0, 3],
                               [3, 0, 2],
                               ])
        df2 = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]),
                               columns=["distanceInKm", "tripMode", "amount"])
        td2 = metrics.traveldistance.TravelDistance()
        td2.data_frame = df2
        result = td.difference(td1, td2, lambda x, y: np.abs(x - y))
        print(result)

    #TODO make test or remove
    def nontest_normalization(self):
        numpy_data = np.array([[1, 0, 4],
                               [2, 0, 1],
                               [1, 1, 1]
                               ])
        df1 = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]), columns=["distanceInKm", "tripMode", "amount"])
        td1 = metrics.traveldistance.TravelDistance()
        td1.data_frame = df1
        numpy_data = np.array([[1, 0, 3],
                               [3, 0, 2],
                               ])
        df2 = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]),
                               columns=["distanceInKm", "tripMode", "amount"])
        td2 = metrics.traveldistance.TravelDistance()
        td2.data_frame = df2
        result = td.difference(td1, td2, lambda x, y: np.abs(x - y), normalize=True)
        print(result.describe())
        print(result)
        result = td.difference(td1, td2, lambda x, y: np.abs(x - y), normalize=True)
        res = pandas.concat([result, result], axis=1)
        res = pandas.DataFrame(np.outer(result, result), index=result.index, columns=result.index)
        res = result.to_frame()
        print(res)
        res = res.reset_index()
        print(res)
        rest = pandas.merge(res, res, how="cross")
        print(rest)
        print(result.describe())

    #TODO make test or move somewhere else
    def nontest_sklearn_mean_squared_error(self):
        data = metrics.data.Data()
        data2 = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        data2.load("resources/example_config_load2/results/")
        modal_split = data._get_modal_split()
        modal_split2 = data2._get_modal_split()
        modal_split = modal_split / modal_split.sum()
        modal_split2 = modal_split2 / modal_split2.sum()
        print(sklearn.metrics.mean_squared_error(modal_split, modal_split2))

        modal_split = data._get_modal_split()
        modal_split2 = data2._get_modal_split()
        modal_split = modal_split * 1000
        modal_split = modal_split / modal_split.sum()
        modal_split2 = modal_split2 / modal_split2.sum()
        print(sklearn.metrics.mean_squared_error(modal_split, modal_split2))

    # TODO not a test
    def nontest_fitting_of_distribution(self):
        data = metrics.data.Data()
        data2 = metrics.data.Data()
        data.load("resources/example_config_load/results/")
        data2.load("resources/example_config_load2/results/")
        temp = data.travel_distance._data_frame
        temp = temp[temp["tripMode"] == 1]
        temp = metric.aggregate(temp, 2, "distanceInKm").reset_index()
        print(temp)
        temp["amount"] = temp["amount"] / temp["amount"].sum()
        print(temp)
        print(plot.draw_travel_distance(temp))
        nmpyaray = temp["amount"].values
        f = Fitter(nmpyaray)
        f.fit()
        print(f.summary())


    # TODO make test
    def nontest_full_write(self):
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        dat = metrics.data.Data(raw_data)
        dat.write()

    # TODO make test
    def nontest_full_read(self):
        numpy_data = np.array([[1, 4, 0, 5, 1],  # -XXX------
                               [0, 5, 0, 5, 1],  # XXXXX-----
                               [2, 8, 1, 5, 1],  # --XXXXXX--
                               [2, 7, 1, 5, 1]   # --XXXXX---
                               ])
        df = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]), columns=["tripBegin", "tripEnd", "tripMode", "durationTrip", "distanceInKm"])
        data = metrics.data.Data(df)

        data.load()
        data.print()
        data.write()
        data.load()
        data.print()

    #TODO make test
    def nontest_something(self):

        numpy_data = np.array([[1, 4, 0],  # -XXX------
                               [0, 5, 0],  # XXXXX-----
                               [2, 8, 1],  # --XXXXXX--
                               [2, 7, 1]   # --XXXXX---
                               ])
        df = pandas.DataFrame(data=numpy_data, index=range(numpy_data.shape[0]), columns=["tripBegin", "tripEnd", "tripMode"])
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        t = metrics.trafficdemand.TrafficDemand.from_raw_data(df)
        print(t._data_frame)
        t.draw()
        t.print()
        t.write("dump\\lolfile")


    #TODO make test
    def nontest_traveltime(self):
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        t = metrics.traveltime.TravelTime(raw_data)
        print(t._data_frame)
        t.draw()
    #TODO make test
    def nontest_traveldistance(self):
        raw_data = pandas.read_csv("resources/demandsimulationResult.csv", sep=";")
        t = metrics.traveldistance.TravelDistance(raw_data)
        print(t.data_frame)
        t.draw()


    def refactortest_something(self):
        experiment = 'neural_network_mode_choice-b_only_one_zero'
        expected_input_data = numpy.load(SPECS.NUMPY + experiment +"_input_data.npy")
        expected_output_data = numpy.load(SPECS.NUMPY + experiment +"_expected_data.npy")

        path = Path(SPECS.EXP_PATH + experiment)
        #yaml_list, data_list = zip(*[simulation.load(file) for file in path.iterdir() if file.name.endswith("00")])
        yaml_list, data_list = zip(*[simulation.load(file) for file in path.iterdir()])
        inp, exp = calibration.neural_network_data_generator.convert_mode(yaml_list, data_list)
        numpy.save(Path(SPECS.NUMPY + experiment + "result_input_data"), inp)
        numpy.save(Path(SPECS.NUMPY + experiment + "result_expected_data"), exp)
        self.assertTrue(numpy.array_equal(expected_input_data, inp))
        self.assertTrue(numpy.array_equal(expected_output_data, exp))

    def test_something_else(self):
        yaml_list, data_list = zip(*[simulation.load("resources/example_config_load"),
                                     simulation.load("resources/example_config_load2")])
        inp, exp = calibration.neural_network_data_generator.convert_dest(yaml_list, data_list)
        dc = yaml_list[0].destination_config()
        expected_params = dc.get_main_parameters_name_only()
        expected_values = [values for key, values in dc.parameters.items() if key in expected_params]
        self.assertEqual(list(exp[0]), expected_values)


    def test_setting_to_value_results(self):
        p = ["asc_car_d_mu", "b_tt_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "b_tt_car_p_mu",
             "b_tt_put_mu", "b_tt_ped", "asc_bike_mu", "b_tt_bike_mu", "b_cost", "b_cost_put",
             "asc_car_d_sig", "asc_car_p_sig", "asc_put_sig", "asc_ped_sig", "asc_bike_sig", "b_tt_car_p_sig",
             "b_tt_car_d_sig", "b_tt_put_sig", "b_tt_bike_sig",
             "b_u_put",  "b_logsum_acc_put",
             "elasticity_acc_put", "b_park_car_d", "elasticity_parken"]
        _, data = simulation.load("resources/compare_individual")
        population = Population(param_vector=p)
        population.set_target(data)


    def test_double_tournament_selection(self):
        population = Population()
        population.load("resources/test_population")
        _, data = simulation.load("resources/compare_individual")
        population.set_target(data)
        population.fitness_for_all_individuals()
        population.double_tournament_selection()

    def test_draw_boundaries(self):
        population = Population()
        population.load("resources/test_population")
        _, data = simulation.load("resources/compare_individual")
        population.set_target(data)
        population.draw_boundaries()

    def test_fancy_combine(self):
        population = Population()
        population.load("resources/test_population")
        _, data = simulation.load("resources/compare_individual")

        population.set_target(data)
        population.fitness_for_all_individuals()
        population.draw_boundaries()
        for i in range(50):
            print(f"Iteration {i}: {population}")
            population.desired_partner_selection()
            #population.draw_boundaries()


    def test_random_generation(self):
        population = Population()
        population.initialize(1)
        _, data = simulation.load("resources/compare_individual")

        population.set_target(data)
        population.fitness_for_all_individuals()

        for i in range(500):
            print(f"Iteration {i}: {population}")
            population.random_individual()
            population.draw_boundaries()


    def test_reiterative_mutation(self):
        population = Population()
        population.initialize(1)
        _, data = simulation.load("resources/compare_individual")
        population.set_target(data)
        population.fitness_for_all_individuals()

        for i in range(5):
            print(f"Iteration IP {i}: {population}")
            population.random_individual()
            population.draw_boundaries()

        for i in range(45):
            print(f"Iteration Mutation: {i}: {population}")
            print(population.best())
            population.mutate_best()
            population.draw_boundaries()

    def test_reiterative_mutation2(self):
        population = Population()
        population.initialize(1)
        _, data = simulation.load("resources/compare_individual")
        population.set_target(data)
        population.fitness_for_all_individuals()

        for i in range(5):
            print(f"Iteration IP {i}: {population}")
            population.random_individual()
            population.draw_boundaries()

        for i in range(45):
            print(f"Iteration Mutation: {i}: {population}")
            print(population.best())
            population.mutate_best2()
            population.draw_boundaries()


    def test_reiterative_mutation3(self):
        population = Population()
        population.initialize(1)
        _, data = simulation.load("resources/compare_individual")
        population.set_target(data)
        population.fitness_for_all_individuals()

        for i in range(5):
            print(f"Iteration IP {i}: {population}")
            population.random_individual()
            population.draw_boundaries()

        for i in range(45):
            print(f"Iteration Mutation: {i}: {population}")
            print(population.best())
            population.mutate_best3()
            population.draw_boundaries()



    def test_run_destination(self):
        d = DestinationIndividual()
        d.set_requirements(["tripMode"])
        d.load("resources/destination_individual")


        x = d.copy()

        x["b_tt_car_d"].set(-0.05)
        _helper(x, d)
        x["b_tt_car_d"].set(-0.2)
        _helper(x, d)
        x["b_tt_car_d"].set(-100)
        _helper(x, d)
        return
        print(x["b_tt_car_d"])

        x.tune_b_tt(0.05)
        print(x["b_tt_car_d"])
        _helper(x, d)
        x.tune_b_tt(-1)
        print(x["b_tt_car_d"])
        _helper(x, d)
        x.tune_b_tt(-1)
        print(x["b_tt_car_d"])
        _helper(x, d)



    def test_run_destination_and_check_for_difference_in_travel_distance(self):
        d = DestinationIndividual()
        d.set_requirements(["tripMode"])
        d.run()
        x = d.copy()
        #x.tune_asc(0)
        #x["asc_ped"].set(25)
        for i in range(10):
            x.tune_b_tt(-0.01)
            print(x["b_tt_car_d"])
            x.run()
            a, b, c = x.draw(reference=d.data)
            c.show()
            print(x.evaluate_fitness(d.data))



if __name__ == '__main__':
    unittest.main()
