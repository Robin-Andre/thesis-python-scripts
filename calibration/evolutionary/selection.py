import random

import numpy


def tournament_selection(self):
    a, b = random.sample(self.population, 2)
    c, d = random.sample(self.population, 2)
    wombo =  a if a.fitness > b.fitness else b
    combo =  c if c.fitness > d.fitness else d
    return wombo, combo

def double_tournament_selection(self):
    x = random.sample(self.population, 4)
    x.sort()
    return x[-2:]

def desired_partner_selection(self):
    ind1 = tournament_selection(self)
    default_error = numpy.sign(ind1.evaluate_fitness_by_group(self.target))
    amount = 0
    for ind in self.population:
        current_error = numpy.sign(ind.evaluate_fitness_by_group(self.target))
        amount_of_differing_trip_modes = (default_error * current_error).lt(0).sum().sum()
        if amount_of_differing_trip_modes >= amount:
            return_ind = ind
            amount = amount_of_differing_trip_modes

    return ind1, return_ind
