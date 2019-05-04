import random
import numpy as np

class City(object):
    def __init__(self, loc):
        self.x = loc[0]
        self.y = loc[1]

    def __sub__(self, other):
        if type(other) == type(self):
            return np.sqrt((self.x - other.x)**2 + (self.y - other.y)**2)

def create_random_route(container):
    return random.sample(container, len(container))

def create_random_population(popsize, container):
    return [create_random_route(container) for _ in range(popsize)]

def create_sample(size=10):
    return [City(loc=(random.randint(-100, 100), random.randint(-100, 100))) for _ in range(size)]

def route_length(cromosome):
    return sum([cromosome[i] - cromosome[i+1] for i in range(len(cromosome)-1)])

def fitness(cromosome):
    return 1 / route_length(cromosome)

def population_fitness(population):
    return sum([fitness(ch) for ch in population]) / len(population)

def fit_and_sort(population):
    sel = [(cr, fitness(cr)) for cr in population]
    return sorted(sel, key=lambda x: x[1], reverse=True)

def _select(population, selection_count):
    mating_pool = fit_and_sort(population)[:selection_count]
    mating_pool = [tup[0] for tup in mating_pool]

    return mating_pool

def _crossover(mating_pool, gen_size):
    offsprings = list()

    for _ in range(gen_size):
        parents = random.sample(mating_pool, 2)

        pivot1 = int(random.random() * len(parents[0]))
        pivot2 = int(random.random() * len(parents[0]))

        pivot1 = min(pivot1, pivot2)
        pivot2 = max(pivot1, pivot2)

        if pivot1 == pivot2:
            if pivot1 != 0:
                pivot1 -= 1
            else:
                pivot2 += 1

        gen_chr = [parents[0][i] for i in range(pivot1, pivot2)]
        rem_genes = [g for g in parents[1] if g not in gen_chr]

        offsprings.append(rem_genes[:pivot1] + gen_chr + rem_genes[pivot1:])

    return offsprings

def _mutate(offsprings, mutation_rate):
    new_gen = list()

    for ch in offsprings:
        if random.random() > mutation_rate:
            swap_genes = random.sample(ch, 2)
            ch[ch.index(swap_genes[0])] = swap_genes[1]
            ch[ch.index(swap_genes[1])] = swap_genes[0]

        new_gen.append(ch)        

    return new_gen

def evaluate_generation(population, population_size, elites, selection_func, crossover_func, mutation_func, mutation_rate):
    mating_pool = selection_func(population, elites)
    offsprings = crossover_func(mating_pool, population_size - elites)
    new_population = mutation_func(offsprings, mutation_rate)

    return new_population + mating_pool

def gen_trainer(genes, generation_size, elite_size, mutation_rate, generations, verbose, verbose_level, plotter=None):
    pop = create_random_population(generation_size, genes)
    
    if plotter is not None:
        max_points = list()
        min_points = list()
        median_points = list()
        ts = list()

    for i in range(1, generations+1):
        if verbose:
            print("[+] Generation", i)
        if verbose_level > 1:
            print("    ==> Fitness:", population_fitness(pop))
            print("    ==> Sample length:", route_length(_select(pop, 1)[0]))

        pop = evaluate_generation(
            population=pop,
            population_size=generation_size,
            elites=elite_size,
            selection_func=_select,
            crossover_func=_crossover,
            mutation_func=_mutate,
            mutation_rate=mutation_rate,
        )

        if plotter is not None and not i % 10:
            ts.append(i)
            sorted_ = fit_and_sort(pop)
            max_points.append(sorted_[0][1])
            min_points.append(sorted_[-1][1])
            median_points.append(sum([cr[1] for cr in sorted_])/len(sorted_))
            plotter.update_multi(ts, min_points, max_points, median_points)

    return (pop, _select(pop, 1)[0])
