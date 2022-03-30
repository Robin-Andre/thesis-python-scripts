from pathlib import Path

from calibration.evolutionary.individual import Individual
from calibration.evolutionary.population import Population
from configurations import SPECS


def plot(x):
    a, b, c = x.draw()
    a.show()


def run(frac_of_pop, name):
    build_folders("random_seeds_final")
    ind = Individual(fraction_of_pop=frac_of_pop)
    ind.set_seed(1)
    ind.set_requirements(["tripMode"])
    ind.run()
    ind.save(SPECS.EXP_PATH + "random_seeds_final/data/" + name + "/" + str(1))
    p = Population(param_vector=["asc_car_d_mu"], fraction_of_pop_size=frac_of_pop)
    p.set_target(ind.data)

    for i in range(49, 51):
        ind = p.seed_individual(i)
        ind.save(SPECS.EXP_PATH + "random_seeds_final/data/" + name + "/" + str(i))
    result = p.logger.print_csv()
    write(result, name, "random_seeds_final")

def main():
    #run(0.02, "fraction_of_population_002")
    #run(0.05, "fraction_of_population_005")
    #run(0.25, "fraction_of_population_025")
    run(1, "fraction_of_population_100")


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
