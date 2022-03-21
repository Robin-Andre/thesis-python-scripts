from pathlib import Path

from calibration.evolutionary.individual import Individual
from calibration.evolutionary.population import Population
from configurations import SPECS


def plot(x):
    a, b, c = x.draw()
    a.show()


def run(frac_of_pop, name):
    foldername = "different_ascs_not_basic_simulation"
    ind = Individual(fraction_of_pop=frac_of_pop)
    ind.set_seed(1)
    ind.run()
    #ind.make_basic(nullify_exponential_b_tt=True)


    #ind.set_requirements(["tripMode"])
    p_vector = ["asc_bike_mu", "asc_car_d_mu", "asc_car_p_mu", "asc_ped_mu", "asc_put_mu"]
    val_deltas = range(-25, 26)

    main_pop_path = Path(SPECS.EXP_PATH + foldername + "/population/")
    main_pop_path.mkdir(exist_ok=True)
    sub_pop_path = Path(SPECS.EXP_PATH + foldername + "/population/" + name + "/")
    sub_pop_path.mkdir(exist_ok=True)

    for param in p_vector:
        pop_path = Path(SPECS.EXP_PATH + foldername + "/population/" + param + "/")

        p = Population(param_vector=[param], fraction_of_pop_size=frac_of_pop)
        p.set_target(ind.data)

        original_value = ind[param].value
        for i in val_deltas:

            ind[param].set(original_value + i)
            print(f"Running parameter: {ind[param]}")
            ind.run()
            p.append(ind)
            ind.save(SPECS.EXP_PATH + foldername + "/data/" + param + "/" + name + "/" + str(i))
        ind[param].set(original_value)

        pop_path = Path(SPECS.EXP_PATH + foldername + "/population/" + name + "/" + param + "/")
        pop_path.mkdir(exist_ok=True)
        p.save(SPECS.EXP_PATH + foldername + "/population/" + name + "/" + param + "/")




def main():
    run(0.02, "fraction_of_population_002")
    run(0.05, "fraction_of_population_005")


def write(result, experiment, folder):
    folder_path = Path(SPECS.EXP_PATH + folder)
    csv_path = Path(SPECS.EXP_PATH + folder + "/csv")
    data_path = Path(SPECS.EXP_PATH + folder + "/data")
    for x in [folder_path, csv_path, data_path]:
        if not x.exists():
            print(f"{x} does not exist:...creating")
            x.mkdir()


    with open(SPECS.EXP_PATH + folder + "/csv" + f"/{experiment}.csv", "w+") as file:
        file.write(result)


if __name__ == "__main__":
    main()
