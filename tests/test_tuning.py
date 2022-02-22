import unittest

import visualization
from calibration import tuning
from calibration.evolutionary.individual import Individual
from calibration.evolutionary.population import Population
from configurations.parameter import Parameter
from metrics.data import Data


def helper(data, title):
    visualization.draw_grouped_modal_split(data.get_grouped_modal_split(["gender", "age"]), title)
    visualization.draw_grouped_modal_split(data.get_grouped_modal_split(), title)


class MyTestCase(unittest.TestCase):

    def test_something(self):
        individual = Individual(42, ["asc_car_d_mu", "female_on_asc_car_d"])
        individual.set_requirements(["tripMode", "gender", "age"])
        individual.make_basic(nullify_exponential_b_tt=True)
        individual.run()

        helper(individual.data, "iteration1")
        data = Data()
        data.load("resources/even_more_detailed_individual/results/")

        pop = Population(param_vector=["asc_car_d_mu", "female_on_asc_car_d"])
        pop.set_target(data)

        helper(data, "comparison")

        p = Parameter("asc_car_d_mu")
        individual = tuning.tune(individual, data, p)#, population=pop)
        helper(individual.data, "iteration2")

        p = Parameter("female_on_asc_car_d")
        individual = tuning.tune(individual, data, p)#, population=pop)
        helper(individual.data, "iteration3")


if __name__ == '__main__':
    unittest.main()
