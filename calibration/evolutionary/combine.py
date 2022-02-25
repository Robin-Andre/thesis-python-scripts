import random

import numpy

from calibration.evolutionary.individual import Individual


def basic_combine(ind1, ind2, child, target, parameter_list):
    for param in parameter_list:
        a = ind1[param].value
        b = ind2[param].value
        c = random.uniform(min(a, b), max(a, b))

        child[param].set(c)
    return child


def __helper(ind1, ind2, child, target, parameter_list, respect_same_sign=True):
    parent1_bounds = ind1.evaluate_fitness_by_group(target)
    parent2_bounds = ind2.evaluate_fitness_by_group(target)
    for param in parameter_list:
        a = ind1[param]
        b = ind2[param]
        y1 = parent1_bounds.iloc[a.requirements['tripMode']]['active_trips']
        x1 = a.value
        y2 = parent2_bounds.iloc[b.requirements['tripMode']]['active_trips']
        x2 = b.value
        if x1 - x2 < 0.1 or (numpy.sign(y1) == numpy.sign(y2) and respect_same_sign):
            set_val = a.value if ind1.fitness > ind2.fitness else b.value
            child[param].set(set_val)
            continue
        assert x1 - x2 != 0
        m = (y2 - y1) / (x2 - x1)
        c = y1 - m * x1
        target = -c / m
        target = min(a.upper_bound, max(a.lower_bound, target))
        #print(f"[{a.lower_bound},{a.upper_bound}] {target}")
        assert a.upper_bound >= target >= a.lower_bound
        #print(f"{param} {x1} {y1}|{x2} {y2} {target} [{a.lower_bound},{a.upper_bound}]")
        child[param].set(target)
    return child


def mathematical_combine(ind1, ind2, child, target, parameter_list):
    return __helper(ind1, ind2, child, target, parameter_list)


def mathematical_combine_without_sign_limit(ind1, ind2, child, target, parameter_list):
    return __helper(ind1, ind2, child, target, parameter_list, respect_same_sign=False)


def average_or_parent_combine(ind1, ind2, child, target, parameter_list):
    for param in parameter_list:
        a = ind1[param].value
        b = ind2[param].value
        c = (a + b) / 2
        val = random.randint(0, 3)
        if val == 3:
            child[param].set(a)
        elif val == 2:
            child[param].set(b)
        else:
            child[param].set(c)

    return child

def classic_combine(ind1, ind2, child, target, parameter_list):
    for param in parameter_list:
        a = ind1[param]
        b = ind2[param]
        parent_flag = random.randint(0, 1)
        if parent_flag:
            set_value = a.value
        else:
            set_value = b.value

        child[param].set(set_value)
    return child