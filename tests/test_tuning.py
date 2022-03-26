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
        my_algorithm.tune(p_list, data, "TravelTime_Default_sum_squared_error")

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

    @unittest.skip("THis is a manual test")
    def test_why_algo_fails(self):
        PARAMS = ["asc_car_d_mu", "asc_car_p_mu", "asc_put_mu", "asc_ped_mu", "asc_bike_mu", "b_tt_car_p_mu", "b_tt_car_d_mu", "b_tt_put_mu", "b_tt_bike_mu", "b_tt_ped"]
        d = Individual(param_list=PARAMS)
        d.run()
        data = d.data

        individual = Individual(-1, PARAMS)
        start_values = individual.average_value_list()
        individual.set_list(start_values)
        individual.run()

        p = "b_tt_bike_mu"
        tuning.tune(individual, data, individual[p])
        """print(individual[p])
        b = individual.data.travel_time.draw(reference=data.travel_time)
        for x in ["b_tt_car_p_mu", "b_tt_car_d_mu", "b_tt_put_mu", "b_tt_bike_mu", "b_tt_ped"]:
            print(x)
            individual[x].observe(individual, data)
        b.show()
        individual[p].set(-0.5)
        individual.run()
        individual[p].observe(individual, data)
        individual[p].error(individual, data)
        b = individual.data.travel_time.draw(reference=data.travel_time)
        b.show()
        individual[p].set(-0.75)
        individual.run()
        individual[p].observe(individual, data)
        individual[p].error(individual, data)
        b = individual.data.travel_time.draw(reference=data.travel_time)
        b.show()
        individual[p].set(-0)
        individual.run()
        individual[p].observe(individual, data)
        individual[p].error(individual, data)
        b = individual.data.travel_time.draw(reference=data.travel_time)
        b.show()
        individual[p].set(-10)
        individual.run()
        individual[p].observe(individual, data)
        individual[p].error(individual, data)
        b = individual.data.travel_time.draw(reference=data.travel_time)
        b.show()"""






if __name__ == '__main__':
    unittest.main()
