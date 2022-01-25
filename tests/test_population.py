import unittest
from calibration.population import Population, Individual
import mobitopp_execution as simulation

class MyTestCase(unittest.TestCase):

    def test_setup(self):
        population = Population()
        population.initialize(10)
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
        population = Population()
        population.load("resources/test_population")
        _, data = simulation.load("resources/compare_individual")
        population.set_target(data)
        population.fitness_for_all_individuals()
        population.draw_boundaries()
        for i in range(50):
            print(f"Iteration {i}: {population}")
            population.temp_rename()
            population.draw_boundaries()

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
            population.temp_rename2()
            population.draw_boundaries()


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

if __name__ == '__main__':
    unittest.main()
