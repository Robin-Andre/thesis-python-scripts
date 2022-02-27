import random

from calibration.evolutionary import replace, combine, evo_strategies, mutate
from calibration.evolutionary.individual import DestinationIndividual
from calibration.evolutionary.population import Population
import mobitopp_execution as simulation

def main():
    random.seed(42)
    params = simulation.default_yaml().destination_config().parameters.keys()
    print(params)
    population = Population(param_vector=simulation.default_yaml().destination_config().parameters.keys(),
                            individual_constructor=DestinationIndividual,
                            replace_func=replace.fancy_replace, combine_func=combine.average_or_parent_combine,
                            mutation_func=mutate.mutate_one_parameter)
    #population.set_random_individual_as_target()
    _, data = simulation.load("../../tests/resources/destination_individual")
    population.set_target(data)
    population.load("../../tests/resources/test2_population")
    for i in range(50):
        evo_strategies.mutate_random_element(population)
        print(population)


if __name__ == "__main__":
    main()