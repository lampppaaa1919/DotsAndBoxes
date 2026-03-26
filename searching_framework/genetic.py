import random
import pygad
from game import play_game

num_generations = 3
num_genomes = 10
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

fitness_cache = {}

def fitness_func(ga_instance, solution, solution_idx):
    alpha, beta, depth = solution
    depth = max(1, int(depth))
    key = (round(alpha, 3), round(beta, 3), depth)
    if key in fitness_cache:
        return fitness_cache[key]
    score = 0
    for _ in range(games_per_fitness):
        score += play_game(alpha, beta, depth)
    fitness = score / games_per_fitness
    fitness_cache[key] = fitness

    return fitness


def on_generation(ga_instance):
    best_solution, best_fitness, _ = ga_instance.best_solution()
    print(f"Generation {ga_instance.generations_completed}: "
          f"Best fitness = {best_fitness:.2f}, "
          f"Params = {best_solution}")


if __name__ == "__main__":
    initial_population = generate_pop(num_genomes)

    ga_instance = pygad.GA(
        num_generations=num_generations,
        num_parents_mating=2,
        initial_population=initial_population,
        fitness_func=fitness_func,
        sol_per_pop=num_genomes,
        num_genes=3,
        mutation_num_genes=1,
        parent_selection_type="sss",
        crossover_type="single_point",
        on_generation=on_generation,
        save_solutions=True,
        parallel_processing=["thread",None]
    )

    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()

    ga_instance.plot_fitness(plot_type="scatter")
    ga_instance.plot_genes()
        # plot_type="scatter", xlabel="alpha, beta and depth", ylabel="fitness score")
    ga_instance.plot_new_solution_rate(plot_type="scatter")

    print("\nBest parameters found:")
    print("alpha:", solution[0])
    print("beta:", solution[1])
    print("depth:", int(solution[2]))
    print("fitness:", solution_fitness)
