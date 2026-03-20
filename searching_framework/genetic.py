import random
import pygad
import numpy as np

#alpha, beta, depth
function_inputs = [4,-2,3.5,5,-11,-4.7]
desired_output = 44

def fitness_func(ga_instance, solution, solution_idx):
    output = np.sum(solution*function_inputs)
    fitness = 1.0 / np.abs(output - desired_output)
    return fitness

fitness_function = fitness_func

num_generations = 50
num_parents_mating = 4

sol_per_pop = 8
num_genes = len(function_inputs)

init_range_low = -2
init_range_high = 5

parent_selection_type = "sss"
keep_parents = 1

crossover_type = "single_point"

mutation_type = "random"
mutation_percent_genes = 10

ga_instance = pygad.GA(num_generations=num_generations,
                       num_parents_mating=num_parents_mating,
                       fitness_func=fitness_function,
                       sol_per_pop=sol_per_pop,
                       num_genes=num_genes,
                       init_range_low=init_range_low,
                       init_range_high=init_range_high,
                       parent_selection_type=parent_selection_type,
                       keep_parents=keep_parents,
                       crossover_type=crossover_type,
                       mutation_type=mutation_type,
                       mutation_percent_genes=mutation_percent_genes)




# def crossover(example1, example2, n):
#     return example1[:n] + example2[n:]
#
#
# def mutate(example, chance, n, m):
#     choose_vals = chance * len(example)
#     for _ in range(choose_vals):
#         mutate_val = int(random.random()) * len(example)
#         if mutate_val % 2 == 0:
#             example[mutate_val] = int(random.random()) * n
#         else:
#             example[mutate_val] = int(random.random()) * m
#
#
# def fitness(example, n, m):
#     (i1, j1), (i2, j2) = example
#     return abs(i1 - n / 2) + abs(j1 - m / 2) + abs(i2 - n / 2) + abs(j2 - m / 2)
