import random

from searching_framework import Problem, astar_search, Node


class DotsAndBoxes(Problem):
    def __init__(self, initial, n, m):
        super().__init__(initial)
        self.n = n
        self.m = m

    def get_all_lines(self):
        allLines = dict()
        totalLines = 0
        for i in range(self.n):
            for j in range(self.m+1):
                allLines[totalLines] = ((i, j), (i + 1, j))
                totalLines += 1
        for j in range(self.m):
            for i in range(self.n+1):
                allLines[totalLines] = ((i, j), (i, j + 1))
                totalLines += 1
        return allLines

    def get_all_lines_length(self):
        allLines = self.get_all_lines()
        return len(allLines)

    def num_squares(self):
        return self.n * self.m

    def close_boxes(self, id_line, prev_lines_ids):
        pts = 0
        drawn_line = self.get_all_lines()[id_line]

        prev_lines = {}
        for id in prev_lines_ids:
            prev_lines[id]=self.get_all_lines()[id]
        prev_lines[id_line]=drawn_line

        ((i1, j1), (i2, j2)) = drawn_line
        # print(i1,j1,i2,j2)
        if i1 == i2:
            i = i1
            # linijata ja zatvara kutijata nad nea
            if (((i - 1, j1), (i - 1, j2)) in prev_lines.values()
                    and ((i - 1, j1), (i, j1)) in prev_lines.values()
                    and ((i - 1, j2), (i, j2)) in prev_lines.values()
                    and i>0):
                # print("Box above")
                pts += 1
            # linijata ja zatvara kutijata pod nea
            if (((i + 1, j1), (i + 1, j2)) in prev_lines.values()
                    and ((i, j1), (i + 1, j1)) in prev_lines.values()
                    and ((i, j2), (i + 1, j2)) in prev_lines.values()
                    and i<=self.n):
                # print("Box below")
                pts += 1
        elif j1 == j2:
            j = j1
            # linijata ja zatvara levata kutija
            if (((i1, j - 1), (i2, j - 1)) in prev_lines.values()
                    and ((i1, j - 1), (i1, j)) in prev_lines.values()
                    and ((i2, j - 1), (i2, j)) in prev_lines.values()
                    and j>0):
                # print("Box left")
                pts += 1
            # linijata ja zatvara desnata kutija
            if (((i1, j + 1), (i2, j + 1)) in prev_lines.values()
                    and ((i1, j), (i1, j+1)) in prev_lines.values()
                    and ((i2, j), (i2, j+1)) in prev_lines.values()
                    and j<=self.m):
                # print("Box right")
                pts += 1
        return (pts, prev_lines)

    def actions(self, state):
        plr, opp, turn, drawn = state
        available = [id_line for id_line in self.get_all_lines() if id_line not in drawn]
        if turn == "agent-a":
            return [f"Plr draws line {i}" for i in available]
        else:
            return [f"Opp draws line {i}" for i in available]

    def result(self, state, action):
        return self.successor(state)[action]

    def successor(self, state):
        succs = dict()
        # ptsPlr 0
        # ptsOpp 0
        # turn agent-a
        # conqueredLines ()
        plr, opp, turn, conc_lines = state
        allLines = self.get_all_lines()
        available_lines = frozenset(allLines.keys()) - frozenset(conc_lines)

        for id_line in available_lines:
            # luckyLineId = random.choice(list(available_lines))
            # luckyLine = allLines[luckyLineId]
            # new_conquered = conc_lines | frozenset([id_line])
            # drawn_set = {allLines[l_id] for l_id in new_conquered}
            newPts = self.close_boxes(id_line, frozenset(conc_lines))[0]
            new_conquered = self.close_boxes(id_line, frozenset(conc_lines))[1]
            if turn == "agent-a":
                succs[f"Plr draws line {id_line}"] = (plr + newPts, opp, "agent-b", frozenset(new_conquered))
            else:
                succs[f"Opp draws line {id_line}"] = (plr, opp + newPts, "agent-a", frozenset(new_conquered))
        return succs

    def goal_test(self, state):
        #ptsPlr, ptsOpp, turn, drawnLines = state
        return len(state[3]) == self.get_all_lines_length()

    def h(self, node):
        state = node.state
        ptsPlr, ptsOpp, turn, drawnLinesIds = state
        drawnLines = {}
        for id in drawnLinesIds:
            drawnLines[id]=self.get_all_lines()[id]
        almost = 0
        for i in range(self.n+1):
            for j in range(self.m+1):
                ctr = 0
                if ((i,j),(i,j+1)) in drawnLines.values(): ctr+=1
                if ((i,j),(i+1,j)) in drawnLines.values(): ctr+=1
                if ((i+1,j),(i+1,j+1)) in drawnLines.values(): ctr+=1
                if ((i,j+1),(i+1,j+1)) in drawnLines.values(): ctr+=1
                if ctr == 3: almost+=1

        conqueredBoxes = ptsPlr + ptsOpp
        remainingBoxes = self.num_squares() - conqueredBoxes - almost
        return remainingBoxes


if __name__ == "__main__":
    game = DotsAndBoxes((0, 0, "agent-a", frozenset()), 2, 2)
    print(game.get_all_lines())
    # goal = 0
    # gridLines = game.getAllLines()
    # for line in range(len(gridLines)):
    #     print(gridLines[line])
    # print(gridLines)

    # testiranje igra so A* algoritam

    playgame = astar_search(game)
    print(playgame.solve())
    print(playgame.solution())

    state = game.initial
    while not game.goal_test(state):
        available = game.actions(state)
        chosen_line = random.choice(available)
        curr_agent = state[2]
        state = game.result(state, chosen_line)
        print(f"{curr_agent} drew line {chosen_line}, scores: Plr={state[0]} Opp={state[1]}")

    plr, opp, _, _ = state
    print(f"Game over! Final scores -> Plr: {plr}, Opp: {opp}")
    winner = "Plr" if plr > opp else "Opp" if opp > plr else "Draw"
    print(f"Winner: {winner}")

    # lines_dict = game.get_all_lines()
    # print(f"Lines: {lines_dict}")
    # lines_len = game.get_all_lines_length()
    # print(f"Total lines: {lines_len}")
    # lines_sq = game.num_squares()
    # print(f"Total squares: {lines_sq}")
    # line_scene = game.close_boxes(3,frozenset({0,1,2,4,6}))
    # print(f"Drawing a line: {line_scene}")
    #
    # print("ACTIONS:")
    # a=game.actions((0,0,"agent-b",frozenset({2,4})))
    # print(a)
    # print("RESULTS:")
    # r = game.result((0,0,"agent-b",frozenset({2,4})),a[0])
    # print(r)
    # print("SUCCESSORS:")
    # s = game.successor((0,0,"agent-a",frozenset({2,4})))
    # print(s)
    # print("GOAL")
    # g = game.goal_test((0,0,"agent-a",frozenset({2,4})))
    # print(g)
    # print("HEURISTIC")
    # h = game.h(Node((0,0,"agent-a",frozenset({2,4}))))
    # print(h)
    # game_test_case=game.close_boxes(7,frozenset({3,4,8}))
    # print(game_test_case[0])