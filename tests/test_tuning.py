import unittest

import visualization
from calibration import tuning
from calibration.evolutionary.individual import Individual
from calibration.evolutionary.population import Population
from configurations.parameter import Parameter
from metrics.data import Data


class MyTestCase(unittest.TestCase):

    def test_something(self):
        individual = Individual(42, ["asc_car_d_mu", "female_on_asc_car_d"])
        individual.make_basic(nullify_exponential_b_tt=True)
        individual.run()
        visualization.draw_grouped_modal_split(individual.data.get_grouped_modal_split(["gender"]))
        data = Data()
        data.load("resources/even_more_detailed_individual/results/")

        pop = Population(param_vector=["asc_car_d_mu", "female_on_asc_car_d"])
        pop.set_target(data)

        visualization.draw_grouped_modal_split(data.get_grouped_modal_split(["gender"]))
        p = Parameter("asc_car_d_mu")
        individual = tuning.tune(individual, data, p, population=pop)
        visualization.draw_grouped_modal_split(individual.data.get_grouped_modal_split(["gender"]))
        p = Parameter("female_on_asc_car_d")
        individual = tuning.tune(individual, data, p, population=pop)
        visualization.draw_grouped_modal_split(individual.data.get_grouped_modal_split(["gender"]))


if __name__ == '__main__':
    unittest.main()
