import numpy
from pyswarms.single.global_best import GlobalBestPSO
import mobitopp_execution as simulation
from calibration.evolutionary.individual import ModalSplitIndividual

from pyswarms.utils.functions import single_obj as fx


def rosenbrock_with_args(x, a, b, c=0):
    f = (a - x[:, 0]) ** 2 + b * (x[:, 1] - x[:, 0] ** 2) ** 2 + c
    return f

def fitness(p_list):
    pass

def test(a):
    print(a)
    for x in a:
        print(x)

        individual = ind_constructor(param_list=param_list)
        individual.set_list(solution)
        #for y in x:
        #    print(y)
    return 4 + a[:, 1] ** 2


if __name__ == "__main__":

    yaml, data = simulation.load("../tests/resources/compare_individual")

    p_list = list(yaml.mode_config().get_main_parameters_name_only())

    ind_constructor = ModalSplitIndividual
    d = ind_constructor(param_list=p_list)

    #bounds = d.pyswarms_bound_lists()

    #print(bounds)

    # instatiate the optimizer
    x_max = 10 * numpy.ones(2)

    x_min = -1 * x_max
    bounds = (x_min, x_max)
    options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
    optimizer = GlobalBestPSO(n_particles=3, dimensions=2, options=options)#, bounds=bounds)

    # now run the optimization, pass a=1 and b=100 as a tuple assigned to args

    cost, pos = optimizer.optimize(test, iters=1000)

