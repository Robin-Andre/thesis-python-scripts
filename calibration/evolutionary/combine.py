import random

import numpy

from calibration.evolutionary.individual import Individual


def basic_combine(ind1, ind2, child, target, parameter_list):
    for param in parameter_list:
        a = ind1.yaml.mode_config().parameters[param].value
        b = ind2.yaml.mode_config().parameters[param].value
        c = random.uniform(min(a, b), max(a, b))

        child.yaml.mode_config().parameters[param].set(c)
    return child


def mathematical_combine(ind1, ind2, child, target, parameter_list):
    parent1_bounds = ind1.evaluate_fitness_by_group(target)
    parent2_bounds = ind2.evaluate_fitness_by_group(target)
    print("----")
    print(parent1_bounds)
    print(parent2_bounds)
    print("----")
    for param in parameter_list:
        a = ind1.yaml.mode_config().parameters[param]
        b = ind2.yaml.mode_config().parameters[param]
        y1 = parent1_bounds.iloc[a.requirements['tripMode']]['active_trips']
        x1 = a.value
        y2 = parent2_bounds.iloc[b.requirements['tripMode']]['active_trips']
        x2 = b.value
        if x1 - x2 < 0.1 or numpy.sign(y1) == numpy.sign(y2):
            set_val = a.value if ind1.fitness > ind2.fitness else b.value
            child.yaml.mode_config().parameters[param].set(set_val)
            continue
        assert x1 - x2 != 0
        m = (y2 - y1) / (x2 - x1)
        c = y1 - m * x1
        target = -c / m
        target = min(a.upper_bound, max(a.lower_bound, target))
        print(f"[{a.lower_bound},{a.upper_bound}] {target}")
        assert a.upper_bound >= target >= a.lower_bound
        print(f"{param} {x1} {y1}|{x2} {y2} {target} [{a.lower_bound},{a.upper_bound}]")
        child.yaml.mode_config().parameters[param].set(target)
    return child


def classic_combine(ind1, ind2, child, target, parameter_list):
    for param in parameter_list:
        a = ind1.yaml.mode_config().parameters[param]
        b = ind2.yaml.mode_config().parameters[param]
        parent_flag = random.randint(0, 1)
        if parent_flag:
            set_value = a.value
        else:
            set_value = b.value

        child.yaml.mode_config().parameters[param].set(set_value)
    return child