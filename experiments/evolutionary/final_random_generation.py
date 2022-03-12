from pathlib import Path
import random

from calibration.evolutionary.individual import Individual
from calibration.evolutionary.population import Population
from configurations import SPECS


def plot(x):
    a, b, c = x.draw()
    a.show()


def run(frac_of_pop, name):
    experiment = "random_seeds_final"
    build_folders(experiment)

    for seed in range(1, 10):
        pop_path = Path(SPECS.EXP_PATH + experiment + "/" + str(seed))
        pop_path.mkdir(exist_ok=True)
        ind = Individual(fraction_of_pop=frac_of_pop)
        ind.set_requirements(["tripMode"])
        ind.set_seed(seed)
        ind.run()
        ind.save(SPECS.EXP_PATH + experiment + "/" + str(seed) + "/data/" + name + "/" + str(0))
        p = Population(param_vector=["asc_car_d_mu"], fraction_of_pop_size=frac_of_pop)
        p.set_target(ind.data)

        for i in range(1, 2):
            ind = p.random_individual()
            ind.save(SPECS.EXP_PATH + experiment + "/" + str(seed) + "/data/" + name + "/" + str(i))
        result = p.logger.print_csv()
        write(result, name, experiment)

def main():
    random.seed(42)
    run(0.02, "fraction_of_population_002")
    run(0.05, "fraction_of_population_005")


def build_folders(folder):
    folder_path = Path(SPECS.EXP_PATH + folder)
    csv_path = Path(SPECS.EXP_PATH + folder + "/csv")
    data_path = Path(SPECS.EXP_PATH + folder + "/data")
    for x in [folder_path, csv_path, data_path]:
        if not x.exists():
            print(f"{x} does not exist:...creating")
            x.mkdir()


def write(result, experiment, folder):

    with open(SPECS.EXP_PATH + folder + f"/{experiment}.csv", "w+") as file:
        file.write(result)


if __name__ == "__main__":
    main()
