"""
Repeatedly running a simulation with random parameters is the simplest form
of calibration. This method creates a population with size 1 and keeps generating
a random individual.
"""
import random
import time
from pathlib import Path

from calibration.evolutionary import selection, replace, individual, evo_strategies, combine, mutate
from calibration.evolutionary.population import Population
import mobitopp_execution as simulation
from configurations import SPECS
from experiments.evolutionary.default_experiment import run_experiment, write


def helper(seed, repetitions, FOLDER, func):
    population = Population(replace_func=replace.fancy_replace, mutation_func=func, seed=101)
    result = run_experiment(seed, population, repetitions, strategy=evo_strategies.simple_repeated_mutation, load=False)
    write(result, func.__name__, seed, FOLDER)

def main():
    FOLDER = "MutateExperiment"
    Path(SPECS.EXP_PATH + FOLDER).mkdir(exist_ok=True)
    output = []
    repetitions = 1
    for seed in range(42, 47):
        helper(seed, repetitions, FOLDER, mutate.mutate)
        helper(seed, repetitions, FOLDER, mutate.mutate2)
        helper(seed, repetitions, FOLDER, mutate.mutate3)

    csv = "\n".join(output)
    print(csv)
    with open(SPECS.EXP_PATH + FOLDER + ".csv", "w+") as file:
        file.write(csv)


if __name__ == '__main__':
    main()
