import random


def crossover(example1, example2, n):
    return example1[:n] + example2[n:]


def mutate(example, chance, n, m):
    choose_vals = chance * len(example)
    for _ in range(choose_vals):
        mutate_val = int(random.random()) * len(example)
        if mutate_val % 2 == 0:
            example[mutate_val] = int(random.random()) * n
        else:
            example[mutate_val] = int(random.random()) * m


def fitness(example, n, m):
    (i1, j1), (i2, j2) = example
    return abs(i1 - n / 2) + abs(j1 - m / 2) + abs(i2 - n / 2) + abs(j2 - m / 2)
