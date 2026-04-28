from utils import Problem
import random
import pygad
import minimax

num_generations = 10
num_genomes = 10
games_per_fitness = 5
depth_min, depth_max = 2, 5


def generate_pop(num_genomes):
    return [
        [
            int(random.uniform(-10, 10)),
            int(random.uniform(-10, 10)),
            int(random.uniform(depth_min, depth_max))
        ]
        for _ in range(num_genomes)
    ]


def on_generation(ga_instance):
    best_solution, best_fitness, _ = ga_instance.best_solution()
    print(f"Generation {ga_instance.generations_completed}: "
          f"Best fitness = {best_fitness:.2f}, "
          f"Params = {best_solution}")

def fitness_wrapper(n,m,case):
    def fitness_func(ga_instance, solution, solution_idx):
        alpha, beta, depth = solution
        depth = int(max(depth_min, min(depth_max, int(depth))))
        fitness = (sum(play_game(n, m, case, alpha, beta, depth)
                      for _ in range(games_per_fitness)
                       ) / games_per_fitness)
        print(f"Genome #{solution_idx}: {solution} - {fitness:.2f}")
        return fitness
    return fitness_func


def genetic_test(n, m, case):
    initial_population = generate_pop(num_genomes)

    ga_instance = pygad.GA(
        num_generations=num_generations,
        num_parents_mating=2,
        initial_population=initial_population,
        fitness_func=fitness_wrapper(n,m,case),
        sol_per_pop=num_genomes,
        num_genes=3,
        mutation_num_genes=1,
        parent_selection_type="sss",
        crossover_type="single_point",
        on_generation=on_generation,
        parallel_processing=["thread", 4],
        # save_solutions=True,
    )

    ga_instance.run()
    solution, solution_fitness, solution_idx = ga_instance.best_solution()

    # ga_instance.plot_fitness(plot_type="scatter")
    # ga_instance.plot_genes()
    # ga_instance.plot_new_solution_rate(plot_type="scatter")

    print("\nBest parameters found:")
    print("alpha:", solution[0])
    print("beta:", solution[1])
    print("depth:", solution[2])
    print("fitness:", solution_fitness)

    return solution


class DotsAndBoxes(Problem):
    def __init__(self, initial, n, m):
        super().__init__(initial)
        self.n = n
        self.m = m
        self.all_lines = self.get_all_lines()

    def get_all_lines(self):
        allLines = dict()
        totalLines = 0
        for i in range(self.n):
            for j in range(self.m + 1):
                allLines[totalLines] = ((i, j), (i + 1, j))
                totalLines += 1
        for j in range(self.m):
            for i in range(self.n + 1):
                allLines[totalLines] = ((i, j), (i, j + 1))
                totalLines += 1
        return allLines

    def get_all_squares(self):
        allSquares = []
        for i in range(self.n):
            for j in range(self.m):
                allSquares.append((i, j))
        return allSquares

    # def plr_conquers(self, i, j):
    #
    # def opp_conquers(self, i, j):
    #

    def get_all_lines_length(self):
        allLines = self.all_lines
        return len(allLines)

    def num_squares(self):
        return self.n * self.m

    def close_boxes(self, id_line, prev_lines_ids):
        pts = 0
        drawn_line = self.all_lines[id_line]

        prev_lines = {}
        for id in prev_lines_ids:
            prev_lines[id] = self.all_lines[id]
        prev_lines[id_line] = drawn_line

        ((i1, j1), (i2, j2)) = drawn_line
        # print(i1,j1,i2,j2)
        if i1 == i2:
            i = i1
            # linijata ja zatvara kutijata nad nea
            if (((i - 1, j1), (i - 1, j2)) in prev_lines.values()
                    and ((i - 1, j1), (i, j1)) in prev_lines.values()
                    and ((i - 1, j2), (i, j2)) in prev_lines.values()
                    and i > 0):
                # print("Box above")
                pts += 1
            # linijata ja zatvara kutijata pod nea
            if (((i + 1, j1), (i + 1, j2)) in prev_lines.values()
                    and ((i, j1), (i + 1, j1)) in prev_lines.values()
                    and ((i, j2), (i + 1, j2)) in prev_lines.values()
                    and i < self.n):
                # print("Box below")
                pts += 1
        elif j1 == j2:
            j = j1
            # linijata ja zatvara levata kutija
            if (((i1, j - 1), (i2, j - 1)) in prev_lines.values()
                    and ((i1, j - 1), (i1, j)) in prev_lines.values()
                    and ((i2, j - 1), (i2, j)) in prev_lines.values()
                    and j > 0):
                # print("Box left")
                pts += 1
            # linijata ja zatvara desnata kutija
            if (((i1, j + 1), (i2, j + 1)) in prev_lines.values()
                    and ((i1, j), (i1, j + 1)) in prev_lines.values()
                    and ((i2, j), (i2, j + 1)) in prev_lines.values()
                    and j < self.m):
                # print("Box right")
                pts += 1
        return pts, set(prev_lines.keys())

    def num_available_lines(self, box, conq_lines):
        n = 0
        i, j = box
        if ((i, j), (i, j + 1)) in conq_lines.values(): n += 1
        if ((i, j), (i + 1, j)) in conq_lines.values(): n += 1
        if ((i, j + 1), (i + 1, j + 1)) in conq_lines.values(): n += 1
        if ((i + 1, j), (i + 1, j + 1)) in conq_lines.values(): n += 1
        return self.get_all_lines_length() - n

    def get_state(self, state):
        plr, opp, turn, drawn = state
        board = [0] * self.get_all_lines_length()
        for line_id in drawn:
            board[line_id] = 1
        return board

    def actions(self, state):
        plr, opp, turn, drawn = state
        available = [id_line for id_line in self.all_lines if id_line not in drawn]
        if turn == "agent-a":
            return [f"Plr draws line {i}" for i in available]
        else:
            return [f"Opp draws line {i}" for i in available]

    def result(self, state, action):
        return self.successor(state)[action]

    def successor(self, state):
        succs = {}
        plr, opp, turn, conq_lines = state
        allLines = self.all_lines
        available_lines = set(allLines.keys()) - set(conq_lines)
        for line_id in available_lines:

            new_pts, new_conq = self.close_boxes(line_id, conq_lines)

            if new_pts > 0:
                if turn == "agent-a":
                    new_state = (plr + new_pts, opp, "agent-a", frozenset(new_conq))
                    succs[f"Plr draws line {line_id}"] = new_state
                else:
                    new_state = (plr, opp + new_pts, "agent-b", frozenset(new_conq))
                    succs[f"Opp draws line {line_id}"] = new_state
            else:
                if turn == "agent-a":
                    new_state = (plr + new_pts, opp, "agent-b", frozenset(new_conq))
                    succs[f"Plr draws line {line_id}"] = new_state
                else:
                    new_state = (plr, opp + new_pts, "agent-a", frozenset(new_conq))
                    succs[f"Opp draws line {line_id}"] = new_state

            # if turn == "agent-a":
            #     new_state = (plr + new_pts, opp, "agent-b", frozenset(new_conq))
            #     succs[f"Plr draws line {line_id}"] = new_state
            # else:
            #     new_state = (plr, opp + new_pts, "agent-a", frozenset(new_conq))
            #     succs[f"Opp draws line {line_id}"] = new_state

        return succs

    def goal_test(self, state):
        # ptsPlr, ptsOpp, turn, drawnLines = state
        return len(state[3]) == self.get_all_lines_length() \
                or state[0] > self.num_squares()//2 \
                or state[1] > self.num_squares()//2 \


    def get_almost(self, state):
        ptsPlr, ptsOpp, turn, drawnLinesIds = state
        drawnLines = {id: self.all_lines[id] for id in drawnLinesIds}
        almost = 0
        for i in range(self.n):
            for j in range(self.m):
                ctr = 0
                if ((i, j), (i, j + 1)) in drawnLines.values(): ctr += 1
                if ((i, j), (i + 1, j)) in drawnLines.values(): ctr += 1
                if ((i + 1, j), (i + 1, j + 1)) in drawnLines.values(): ctr += 1
                if ((i, j + 1), (i + 1, j + 1)) in drawnLines.values(): ctr += 1
                if ctr == 3: almost += 1
        return almost

    def h(self, state):
        ptsPlr, ptsOpp, turn, drawnLinesIds = state
        drawnLines = {id: self.all_lines[id] for id in drawnLinesIds}
        almost = self.get_almost(state)
        return (ptsPlr - ptsOpp) + almost


def new_game(n, m):
    return DotsAndBoxes((0, 0, "agent-a", frozenset()), n, m)

def play_game(n, m, case,alpha,beta,depth):
    game = DotsAndBoxes((0, 0, "agent-a", frozenset()), n, m)
    state = game.initial

    plr, opp, _, _ = state
    clock = 0

    while not game.goal_test(state):
        plr, opp, turn, drawn = state
        if clock == 3:
            if turn == "agent-a":
                action = minimax.best_move(game, state, depth, is_maximizing=True, case=case)
            else:
                action = minimax.best_move(game, state, depth - 1, is_maximizing=False, case=case)
            state = game.result(state, action)
            clock = 0
        else:
            if turn == "agent-a":
                action = random.choice(game.actions(state))
            else:
                action = random.choice(game.actions(state))
            state = game.result(state, action)
            clock+=1
    plr, opp, _, _ = state
    return plr - opp


def play_full_game(n, m, case, alpha, beta, depth):
    game = new_game(n, m)
    state = game.initial
    plr, opp = 0, 0
    while not game.goal_test(state):
        plr, opp, turn, drawn = state

        if turn == "agent-a":
            # train
            action = minimax.best_move(game, state, depth, is_maximizing=True, case=case)
        else:
            # test
            action = minimax.best_move(game, state, depth, is_maximizing=False, case=case)
            # action = random.choice(game.actions(state))
        state = game.result(state, action)
        plr, opp, turn, drawn = state
        print(f"{action} \n Plr: {plr} Opp: {opp}")

    winner = "PLR" if plr > opp else "OPP" if opp > plr else "DRAW"
    print(f"WINNER: {winner}")


if __name__ == "__main__":
    print("INSERT DIMENSIONS <n> <m> AND CASE <case>")
    n, m, case = int(input()), int(input()), int(input())
    alpha, beta, depth = genetic_test(n,m,case)
    play_full_game(n, m, case, alpha, beta, int(depth))