#TODO https://qiskit.org/documentation/_modules/qiskit/algorithms/optimizers/spsa.html
import numpy as np
from qiskit.algorithms.optimizers import SPSA
import mobitopp_execution as simulation

from calibration.evolutionary.individual import Individual
from metrics.data import Comparison


def loss(x, p_list, m, data):

    ind = Individual(param_list=p_list)
    print(list(x))
    ind.set_list(list(x))
    ind.run()
    c = Comparison(ind.data, data)
    print(1000 * -c.travel_demand)
    return 1000 * -c.travel_demand


if __name__ == "__main__":
    parameter_list = ["asc_car_d_mu", "asc_car_p_mu", "asc_ped_mu", "asc_put_mu", "asc_bike_mu"]
    run_individual = Individual(param_list=parameter_list)
    run_individual.run()
    data = run_individual.data

    spsa = SPSA(maxiter=2, learning_rate=[1.0, 1.0], perturbation=[1.0, 1.0], second_order=True)

    metric = "LolCAt"

    result = spsa.optimize(len(parameter_list), lambda x: loss(x, parameter_list, metric, data), initial_point=[5, 5, 5, 5, 5])
    print(result)
