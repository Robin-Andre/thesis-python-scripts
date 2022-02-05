
def temp_rename2(population):
    ind1, ind2 = self.double_tournament_selection()
    child = self.combine2(ind1, ind2)
    self.fancy_replace(child)


def simple_combine(population):
    ind1, ind2 = population.select()
    child = population.combine(ind1, ind2)
    population.insert(child)
    if child.fitness == population.best().fitness:
        population.draw_boundaries()
        population.draw_boundaries_traveltime()
        population.draw_boundaries_modal_split()


def simple_repeated_mutation(population):

    ind1 = population.random_individual()
    population.append(ind1)


    mutation = population.mutate(ind1)
    while mutation.fitness > ind1.fitness:
        population.insert(mutation)
        ind1 = mutation
        mutation = population.mutate(ind1)



def mutate_best(population):

    self.replace_worst_non_forced(self.mutate(self.best()))

def mutate_best2(population):
    self.replace_worst_non_forced(self.mutate2(self.best()))

def mutate_best3(population):
    self.replace_worst_non_forced(self.mutate3(self.best()))
