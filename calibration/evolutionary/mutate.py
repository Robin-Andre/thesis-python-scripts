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