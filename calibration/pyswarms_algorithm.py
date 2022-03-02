import numpy
from pyswarms.single.global_best import GlobalBestPSO
import mobitopp_execution as simulation
from calibration.evolutionary.individual import ModalSplitIndividual

from pyswarms.utils.functions import single_obj as fx


def rosenbrock_with_args(x, a, b, c=0):
    f = (a - x[:, 0]) ** 2 + b * (x[:, 1] - x[:, 0] ** 2) ** 2 + c
    return f



def test(a):
    yaml, data = simulation.load("../tests/resources/compare_individual")
    p_list = list(yaml.mode_config().get_main_parameters_name_only())

    fitness_vals = []
    for x in a:


        individual = ind_constructor(param_list=p_list)
        individual.set_list(x)
        individual.run()

        #a, b, c = individual.draw(reference=data)
        #a.show()

        fitness = individual.evaluate_fitness(data)
        print(-fitness)
        fitness_vals.append(-fitness) # Pyswarms optimizes towards a minima so the fitness needs to be big if invalid

    return numpy.asarray(fitness_vals)


if __name__ == "__main__":

    yaml, data = simulation.load("../tests/resources/compare_individual")



    p_list = list(yaml.mode_config().get_main_parameters_name_only())
    #p_list = ["asc_car_d_mu"]
    ind_constructor = ModalSplitIndividual
    d = ind_constructor(param_list=p_list)

    d.run()
    data = d.data
    # instatiate the optimizer
    bounds = d.pyswarms_bound_lists()

    print(bounds)


    options = {'c1': 0.5, 'c2': 0.3, 'w': 0.9}
    optimizer = GlobalBestPSO(n_particles=10, dimensions=len(p_list), options=options, bounds=bounds)

    # now run the optimization, pass a=1 and b=100 as a tuple assigned to args

    cost, pos = optimizer.optimize(test, iters=10)
    print(pos)#
    x = d.copy()
    x.set_list(pos)
    x.run()#

    a, b, c = x.draw(reference=data)
    a.show()
    b.show()


