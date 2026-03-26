import random
import pygad
import minimax
from game import DotsAndBoxes as dnb, play_game


num_generations = 5
num_genomes = 6
games_per_fitness = 3
depth_min, depth_max = 1, 3

def generate_pop(num_genomes):
    population = []
    for _ in range(num_genomes):
        alpha = random.uniform(-5, 5)
        beta = random.uniform(-5, 5)
        depth = random.randint(depth_min, depth_max)
        population.append([alpha, beta, depth])
    return population

def fitness_func(ga_instance, solution, solution_idx):
    alpha, beta, depth = solution
    depth = max(1, int(depth))
    score = 0
    for _ in range(games_per_fitness):
        score += play_game(alpha, beta, depth)
    return score


def on_generation(ga_instance):
    best_solution, best_fitness, _ = ga_instance.best_solution()
    print(f"Generation {ga_instance.generations_completed}: "
          f"Best fitness = {best_fitness:.2f}, "
          f"Params = {best_solution}")


if __name__ == "__main__":
    initial_population = generate_pop(num_genomes)

    ga_instance = pygad.GA(
        num_generations=num_generations,
        num_parents_mating=4,
        initial_population=initial_population,
        fitness_func=fitness_func,
        num_genes=3,
        mutation_num_genes=1,
        parent_selection_type="sss",
        crossover_type="single_point",
        mutation_type="random",
        on_generation=on_generation
    )

    ga_instance.run()

    solution, solution_fitness, solution_idx = ga_instance.best_solution()

    print("\nBest parameters found:")
    print("alpha:", solution[0])
    print("beta:", solution[1])
    print("depth:", int(solution[2]))
    print("fitness:", solution_fitness)
