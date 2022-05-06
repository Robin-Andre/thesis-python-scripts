import random

"""
A relic from creating an own evolutionary algorithm 
Was intended to list all different mutation options
"""
def mutate(individual, mutation, target):
    temp = individual.evaluate_fitness_by_group(target)
    temp = -(temp / temp.abs().sum())
    alpha = 0.2
    for param in individual.parameter_name_list:
        a = individual[param]
        if a.value > 0:
            target = a.value * (1 + alpha * temp.at[a.requirements["tripMode"], "active_trips"])
            target = max(a.value, target)
        else:
            target = a.value * (1 - alpha * temp.at[a.requirements["tripMode"], "active_trips"])
            target = min(a.value, target)

        mutation[param].set(target)
        #print(f"{param} : {target} ")
    return mutation

def mutate_one_parameter(individual, mutation, target):
    param_name = random.choice(list(individual.parameter_name_list))
    print(f"Chosen Parameter: {param_name}")
    a, lower, upper = individual[param_name].value, individual[param_name].lower_bound, individual[param_name].upper_bound
    alpha = 0.05
    sign = 1 if random.random() < 0.5 else -1
    target = a + alpha * sign * (upper - lower)
    print(f"Original Value: {a} target: {target}")
    mutation[param_name].set(target)
    return mutation


def mutate2(individual, mutation, target):
    temp = individual.evaluate_fitness_by_group(target)
    temp = -(temp / temp.abs().sum())

    alpha = 0.2
    for param in individual.parameter_name_list:

        a = individual[param]
        target = a.value + alpha * temp.at[a.requirements["tripMode"], "active_trips"] * (a.upper_bound - a.lower_bound)

        mutation[param].set(target)
        #print(f"{param} :{a.value} -> {target} ")
    return mutation

def mutate3(individual, mutation, target):
    temp = individual.evaluate_fitness_by_group(target)
    temp = (temp / temp.abs().sum())

    alpha = -0.2
    for param in individual.parameter_name_list:

        a = individual[param]
        x = temp.at[a.requirements["tripMode"], "active_trips"] > 0
        if x > 0:

            target = a.value + alpha * x * (a.upper_bound - a.lower_bound)
        else:
            target = a.value
        mutation.yaml[param].set(target)

        #print(f"{param} :{a.value} -> {target} ")
    return mutation