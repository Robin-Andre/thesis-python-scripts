import unittest

import mobitopp_execution as simulation
from calibration.evolutionary import initialization, evo_strategies, selection, replace, individual
from calibration.evolutionary.individual import Individual
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

if __name__ == '__main__':
    unittest.main()
