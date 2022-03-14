import unittest

import visualization
from calibration import tuning, my_algorithm
from calibration.evolutionary.individual import Individual
from calibration.evolutionary.population import Population
from configurations.parameter import Parameter
from metrics.data import Data


def helper(data, title, ref=None):
    visualization.draw_grouped_modal_split(data.get_grouped_modal_split(["gender", "age"]), title)
    visualization.draw_grouped_modal_split(data.get_grouped_modal_split(), title)
    data.travel_time.draw(reference=ref).show()


class MyTestCase(unittest.TestCase):

    def test_tuning_algo(self):
        individual = Individual(param_list=["asc_car_d_mu", "female_on_asc_car_d"])
        individual.randomize_active_parameters()
        print(individual)
        individual.run()
        data = individual.data
        p_list = ["asc_car_d_mu", "female_on_asc_car_d"]
        my_algorithm.tune(p_list, data, "Lolcat")

    #@unittest.skip("Not a test but a convenience run")
    def test_something(self):
        individual = Individual(42, ["asc_car_d_mu", "female_on_asc_car_d"])
        individual.set_requirements(["tripMode", "gender", "age"])
        individual.make_basic(nullify_exponential_b_tt=True)
        individual.run()


        data = Data()
        data.load("resources/even_more_detailed_individual/results/")
        helper(individual.data, "iteration1", ref=data.travel_time)
        pop = Population(param_vector=["asc_car_d_mu", "female_on_asc_car_d"])
        pop.set_target(data)

        helper(individual.data, "comparison", ref=data.travel_time)

        p = Parameter("asc_car_d_mu")
        individual = tuning.tune(individual, data, p)#, population=pop)
        helper(individual.data, "iteration2", ref=data.travel_time)

        p = Parameter("female_on_asc_car_d")
        individual = tuning.tune(individual, data, p)#, population=pop)
        helper(individual.data, "iteration3", ref=data.travel_time)

    @unittest.skip("Visualization Test")
    def test_weekday_works(self):
        individual = Individual(42, ["b_arbwo_car_d"])
        self.assertAlmostEqual(individual["b_arbwo_car_d"].value, 3.6962)
        self.assertEqual(individual.requirements, {"workday", "tripMode"})
        #individual.make_basic(nullify_exponential_b_tt=True)
        individual.run()
        individual.data.traffic_demand.draw_smooth().show()
        temp = individual.copy()
        temp["b_arbwo_car_d"].set(-20)
        temp.run()
        temp.data.traffic_demand.draw_smooth(reference=individual.data.traffic_demand).show()



if __name__ == '__main__':
    unittest.main()
