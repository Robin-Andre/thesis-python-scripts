import unittest

import mobitopp_execution as simulation
from calibration.evolutionary import initialization, evo_strategies, selection, replace, individual
from calibration.evolutionary.population import Population


class MyTestCase(unittest.TestCase):

    def test_setup(self):
        population = Population()
        population.initialize(10)
        population.save("resources/test_population")
        target_individual = individual.Individual()
        self.assertAlmostEqual(target_individual.yaml.mode_config().parameters["asc_car_d_mu"].value, 7.4)
        target_individual.run()
        target_individual.save("resources/compare_individual")

    def test_setup2(self):
        population = Population(initialize_func=initialization.initialize_generous)
        population.initialize(size=5)
        population.save("resources/test_population")
        target_individual = Individual()
        self.assertAlmostEqual(target_individual.yaml.mode_config().parameters["asc_car_d_mu"].value, 7.4)
        target_individual.run()
        target_individual.save("resources/compare_individual")

    def test_load(self):
        population = Population()
        population.load("resources/test_population")


    def test_equality(self):
        population = Population()
        population.load("resources/test_population")
        _, data = simulation.load("resources/compare_individual")
        population.set_target(data)
        population.fitness_for_all_individuals()
        print(population)

    def test_tournament_selection(self):
        population = Population(select_func=selection.double_tournament_selection, replace_func=replace.fancy_replace, seed=101)
        population.individual_constructor = individual.ModalSplitIndividual
        population.load("resources/test_population")
        _, data = simulation.load("resources/compare_individual")
        population.set_target(data)
        population.fitness_for_all_individuals()
        #population.draw_boundaries()
        #population.draw_boundaries_traveltime()
        population.draw_boundaries_modal_split()
        for i in range(20):
            print(f"Iteration {i}: {population}")
            evo_strategies.simple_combine(population)
            #population.draw_boundaries()
            #population.draw_boundaries_traveltime()
            population.draw_boundaries_modal_split()
        print(population.best().yaml.mode_config())
        population.logger.print_csv()


    def test_different_metrics_from_load(self):
        population = Population(individual_constructor=individual.Individual)
        population2 = Population(individual_constructor=individual.TravelTimeIndividual)
        population.load("resources/test_population")
        population2.load("resources/test_population")
        _, data = simulation.load("resources/compare_individual")
        population.set_target(data)
        population2.set_target(data)
        population.fitness_for_all_individuals()
        population2.fitness_for_all_individuals()
        self.assertNotEqual(population, population2)


    def test_active_parameters_is_working(self):
        c = simulation.default_yaml().mode_config().get_main_parameters_name_only()
        _, data = simulation.load("resources/compare_individual")
        population = Population(param_vector=["asc_car_d_mu"])
        population.set_target(data)
        random_config = population.random_individual().yaml.mode_config()
        default_config = simulation.default_yaml().mode_config()
        for param in c:
            if param == "asc_car_d_mu":
                continue
            self.assertAlmostEqual(random_config.parameters[param].value, default_config.parameters[param].value)

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

if __name__ == '__main__':
    unittest.main()
