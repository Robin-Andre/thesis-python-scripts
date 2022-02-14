"""
Repeatedly running a simulation with random parameters is the simplest form
of calibration. This method creates a population with size 1 and keeps generating
a random individual.
"""
import random
import time
from pathlib import Path

from calibration.evolutionary import selection, replace, individual, evo_strategies
from calibration.evolutionary.population import Population
import mobitopp_execution as simulation
from configurations import SPECS
from experiments.evolutionary.default_experiment import run_experiment, write


def main():
    FOLDER = "MetricExperiment"
    Path(SPECS.EXP_PATH + FOLDER).mkdir(exist_ok=True)
    output = []
    repetitions = 50
    for seed in range(42, 47):
        population = Population(select_func=selection.double_tournament_selection, replace_func=replace.fancy_replace,
                                individual_constructor=individual.TravelTimeIndividual, seed=101)

        result = run_experiment(seed, population, repetitions)
        write(result, "traveltime", seed)
        print("---------------------------")
        print(result)
        print("---------------------------")
        population2 = Population(select_func=selection.double_tournament_selection, replace_func=replace.fancy_replace,
                                 individual_constructor=individual.Individual, seed=101)
        result2 = run_experiment(seed, population2, repetitions)
        write(result2, "traveldemand", seed)
        print("---------------------------")
        print(result2)
        print("---------------------------")
        population3 = Population(select_func=selection.double_tournament_selection, replace_func=replace.fancy_replace,
                                 individual_constructor=individual.ModalSplitIndividual, seed=101)
        result3 = run_experiment(seed, population3, repetitions)
        write(result3, "modalsplit", seed)
        print("---------------------------")
        print(result3)
        print("---------------------------")
        output.append(result)
        output.append(result2)
        output.append(result3)

    csv = "\n".join(output)
    print(csv)
    with open(SPECS.EXP_PATH + "MetricExperiment.csv", "w+") as file:
        file.write(csv)


if __name__ == '__main__':
    main()
