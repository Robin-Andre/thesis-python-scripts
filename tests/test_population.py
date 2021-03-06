import random
import unittest

import mobitopp_execution as simulation
from calibration.evolutionary import initialization, evo_strategies, selection, replace, individual, combine
from calibration.evolutionary.individual import Individual, DestinationIndividual, ShoppingDestinationIndividual
from calibration.evolutionary.population import Population


class MyTestCase(unittest.TestCase):
    @unittest.skip("Building test data  is not always required")
    def test_setup(self):
        population = Population()
        population.initialize(10)
        population.save("resources/test_population")
        target_individual = individual.Individual()
        self.assertAlmostEqual(target_individual.yaml.mode_config().parameters["asc_car_d_mu"].value, 7.4)
        target_individual.run()
        target_individual.save("resources/compare_individual")

    @unittest.skip("Data creation, not needed for tests")
    def test_setup2(self):
        population = Population(initialize_func=initialization.initialize_generous)
        population.initialize(size=5)
        population.save("resources/test_population")
        target_individual = Individual()
        self.assertAlmostEqual(target_individual.yaml.mode_config().parameters["asc_car_d_mu"].value, 7.4)
        target_individual.run()
        target_individual.save("resources/compare_individual")

    def test_different_metrics_from_load(self):
        population = Population(individual_constructor=individual.Individual)
        population2 = Population(individual_constructor=individual.TravelTimeIndividual)

        _, data = simulation.load("resources/compare_individual")
        population.set_target(data)
        population2.set_target(data)

        population.load("resources/test_population")
        population2.load("resources/test_population")

        self.assertNotEqual(population, population2)

    def test_active_parameters_is_working(self):
        c = simulation.default_yaml().mode_config().get_main_parameters_name_only()
        _, data = simulation.load("resources/compare_individual")
        population = Population(param_vector=["asc_car_d_mu"])
        population.set_target(data)
        random_config = population.random_individual().yaml.mode_config()
        default_config = simulation.default_yaml().mode_config()
        for param in c:
            # Since the parameter asc_car_d_mu is in the parameter vector it should be randomized, and therefore it
            # is impossible to track which value it should be assigned. It would be possible to test that asc_car_d is
            # changed, but it could theoretically be assigned the same value as before.
            if param == "asc_car_d_mu":
                continue
            # However, the important part of the test is to ensure that all the other parameters are not changed.
            self.assertAlmostEqual(random_config.parameters[param].value, default_config.parameters[param].value)

    def test_detailed_data_from_population(self):
        population = Population(param_vector=["asc_car_d_mu", "female_on_asc_car_d"])
        self.assertEqual(population.data_requirements(), {"tripMode", "gender"})
        population = Population(param_vector=["asc_car_d_mu", "female_on_asc_car_d", "student_on_asc_bike", "inc_low_on_asc_put"])
        self.assertEqual(population.data_requirements(), {"tripMode", "gender", "employment", "economicalStatus"})

    def test_individual_takes_proper_data(self):
        population = Population(
            param_vector=["asc_car_d_mu", "female_on_asc_car_d", "student_on_asc_bike", "inc_low_on_asc_put"])
        population.set_random_individual_as_target()
        self.assertEqual(population.data_requirements(), population.target.columns())

    @unittest.skip("not a test but just an execution")
    def test_population_can_combine_appropriately(self):
        random.seed(42)
        population = Population(param_vector=simulation.default_yaml().activity_destination_config("shopping").parameters.keys(), individual_constructor=ShoppingDestinationIndividual,
                                replace_func=replace.fancy_replace, combine_func=combine.average_or_parent_combine)
        population.set_random_individual_as_target()
        for i in range(10):
            population.append(population.random_individual())
            print(population)
        for i in range(50):
            evo_strategies.simple_combine(population)
            print(population)
        print(population)

    @unittest.skip("not a test but just an execution")
    def test_proempfel(self):
        d = DestinationIndividual()
        d.run()
        c = DestinationIndividual()
        #random.seed(42)
        c.randomize_special_config("leisure")
        c.run()
        print(f"Current fitness: {c.evaluate_fitness(d.data)}")

        c["leisure", "b_attr"].set(0.1)
        c.run()
        print(f"Current fitness: {c.evaluate_fitness(d.data)}")
        c["leisure", "b_attr"].set(1)
        c.run()
        print(f"Current fitness: {c.evaluate_fitness(d.data)}")

        c["leisure", "b_attr"].set(0.5)
        c.run()
        print(f"Current fitness: {c.evaluate_fitness(d.data)}")

        c["leisure", "b_attr"].set(0.7)
        c.run()
        print(f"Current fitness: {c.evaluate_fitness(d.data)}")


if __name__ == '__main__':
    unittest.main()
