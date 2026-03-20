import random
import math
import pygad

from searching_framework import Problem, astar_search, minimax
from searching_framework.expectimax import *


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
            if turn == "agent-a":
                new_state = (plr + new_pts, opp, "agent-b", frozenset(new_conq))
                succs[f"Plr draws line {line_id}"] = new_state
            else:
                new_state = (plr, opp + new_pts, "agent-a", frozenset(new_conq))
                succs[f"Opp draws line {line_id}"] = new_state
        return succs

    def goal_test(self, state):
        # ptsPlr, ptsOpp, turn, drawnLines = state
        return len(state[3]) == self.get_all_lines_length()

    def h(self, state):

        ptsPlr, ptsOpp, turn, drawnLinesIds = state
        drawnLines = {}
        for id in drawnLinesIds:
            drawnLines[id] = self.all_lines[id]

        almost = 0
        for i in range(self.n):
            for j in range(self.m):
                ctr = 0
                if ((i, j), (i, j + 1)) in drawnLines.values(): ctr += 1
                if ((i, j), (i + 1, j)) in drawnLines.values(): ctr += 1
                if ((i + 1, j), (i + 1, j + 1)) in drawnLines.values(): ctr += 1
                if ((i, j + 1), (i + 1, j + 1)) in drawnLines.values(): ctr += 1
                if ctr == 3: almost += 1

        return (ptsPlr - ptsOpp) + almost


if __name__ == "__main__":
    game = DotsAndBoxes((0, 0, "agent-a", frozenset()), 3, 3)
    state = game.initial
    plr, opp, turn, drawn_set = state
    while not game.goal_test(state):
        if turn == "agent-a":

            action = minimax.best_move(game, state, depth=3, is_maximizing=True,2)
            # action = random.choice(game.actions(state))
            #genetski - ucenje
        else:
            action = minimax.best_move(game, state, depth=3, is_maximizing=False)
            # action = random.choice(game.actions(state))
            #genetski - testiranje
        state = game.result(state, action)
        plr, opp, turn, drawn_set = state
        print(f"{action}")
        print(f"Plr: {plr} Opp: {opp}")
    winner = "PLR" if plr>opp else "OPP" if opp>plr else "DRAW"
    print(f"WINNER: {winner}")

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
