from calibration.evolutionary.individual import Individual
from calibration.evolutionary.population import Population

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
    plot(p.seed_individual(1))
    plot(p.seed_individual(2))

    p.seed_individual(3)
    p.seed_individual(4)
    p.seed_individual(5)
    p.seed_individual(6)
    p.seed_individual(7)
    p.seed_individual(8)
    p.seed_individual(9)




if __name__ == "__main__":
    main()