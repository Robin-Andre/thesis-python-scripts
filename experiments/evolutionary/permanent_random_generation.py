
from datetime import time, datetime
from pathlib import Path

from calibration.evolutionary import evo_strategies, replace
from calibration.evolutionary.population import Population
from configurations import SPECS
from experiments.evolutionary.default_experiment import run_experiment, write


def main():
    FOLDER = "BaselineEvoRandomExperiment"
    start_time = datetime.now().strftime("(%m%d%H)")
    Path(SPECS.EXP_PATH + FOLDER).mkdir(exist_ok=True)
    output = []
    repetitions = 50
    for seed in range(42, 52):
        for i in range(repetitions):

            population = Population(replace_func=replace.replace_worst_non_forced, seed=101)
            ind = population.random_individual()
        result = run_experiment(seed, population, repetitions, strategy=evo_strategies.permanent_random_generation, load=False)
        write(result, "base" + start_time, seed, FOLDER)

    csv = "\n".join(output)
    print(csv)
    with open(SPECS.EXP_PATH + FOLDER + ".csv", "w+") as file:
        file.write(csv)


if __name__ == '__main__':
    main()
