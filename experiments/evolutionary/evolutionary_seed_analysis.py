from pathlib import Path

from calibration.evolutionary.individual import Individual
from calibration.evolutionary.population import Population
from configurations import SPECS


def plot(x):
    a, b, c = x.draw()
    a.show()

def main():
    ind = Individual()
    ind.set_seed(1)
    ind.set_requirements(["tripMode"])
    ind.run()
    p = Population(param_vector=["asc_car_d_mu"])
    p.set_target(ind.data)
    #plot(p.seed_individual(1))
    #plot(p.seed_individual(2))
    p.seed_individual(2)
    p.seed_individual(3)
    p.seed_individual(4)
    p.seed_individual(5)
    p.seed_individual(6)
    p.seed_individual(7)
    p.seed_individual(8)
    p.seed_individual(9)

    result = p.logger.print_csv()
    write(result, "small_fraction_of_population", "random_seeds_final")

def write(result, experiment, folder):
    folder_path = Path(SPECS.EXP_PATH + folder)
    if not folder_path.exists():
        print(f"{folder_path} does not exist:...creating")
        folder_path.mkdir()

    with open(SPECS.EXP_PATH + folder + f"/{experiment}.csv", "w+") as file:
        file.write(result)

if __name__ == "__main__":
    main()