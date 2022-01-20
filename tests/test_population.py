import unittest
from calibration.population import Population, Individual
import mobitopp_execution as simulation

class MyTestCase(unittest.TestCase):

    def nonttest_setup(self):
        population = Population()
        population.initialize(10)
        population.save("resources/test_population")
        target_individual = Individual()
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

    def nontest_tournament_selection(self):
        population = Population()
        population.load("resources/test_population")
        _, data = simulation.load("resources/compare_individual")
        population.set_target(data)
        population.fitness_for_all_individuals()

        for i in range(50):
            print(f"Iteration {i}: {population}")
            population.temp_rename()


    def test_double_tournament_selection(self):
        population = Population()
        population.load("resources/test_population")
        _, data = simulation.load("resources/compare_individual")
        population.set_target(data)
        population.fitness_for_all_individuals()
        population.double_tournament_selection()



if __name__ == '__main__':
    unittest.main()
