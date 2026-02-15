import random

from searching_framework import Problem, astar_search

class DotsAndBoxes(Problem):
    def __init__(self, initial, n, m):
        super().__init__(initial)
        self.n=n
        self.m=m

    def get_all_lines(self):
        allLines = dict()
        totalLines = 0
        for i in range(self.n):
            for j in range(self.m):
                if i + 1 < self.n:
                    allLines[totalLines] = ((i, j), (i + 1, j))
                    totalLines += 1
                if j + 1 < self.m:
                    allLines[totalLines] = ((i, j), (i, j + 1))
                    totalLines += 1
        return allLines

    def num_squares(self):
        return (self.n-1) * (self.m-1)

    def get_all_lines_length(self):
        allLines = self.get_all_lines()
        return len(allLines)

    def close_boxes(self, id_line, prev_lines):
        pts=0
        drawn_line=self.get_all_lines()[id_line]
        ((i1,j1),(i2,j2))=drawn_line
        if i1==i2:
            i=i1
            #linijata ja zatvara kutijata nad nea
            if (((i-1,j1),(i-1,j2)) in prev_lines
                and ((i-1,j1),(i,j1)) in prev_lines
                and ((i-1,j2),(i,j2)) in prev_lines
                and i>0): pts+=1
            # linijata ja zatvara kutijata pod nea
            if (((i+1,j1),(i+1,j2)) in prev_lines
                    and ((i+1,j1),(i,j1)) in prev_lines
                    and ((i+1,j2),(i,j2)) in prev_lines
                    and i<self.n-1): pts+=1
        elif j1==j2:
            j=j1
            #linijata ja zatvara levata kutija
            if (((i1,j-1),(i2,j-1)) in prev_lines
                    and ((i1,j-1),(i1,j)) in prev_lines
                    and ((i2,j-1),(i2,j)) in prev_lines
                    and j>0): pts+=1
            #linijata ja zatvara desnata kutija
            if (((i1,j+1),(i2,j+1)) in prev_lines
                    and ((i1,j+1),(i1,j)) in prev_lines
                    and ((i2,j+1),(i2,j)) in prev_lines
                    and j<self.m-1): pts+=1
        return pts


    def actions(self, state):
        _,_,turn,drawn = state
        available = [id_line for id_line in self.get_all_lines() if id_line not in drawn]
        if turn == "agent-a":
            return [f"Plr draws line {i}" for i in available]
        else:
            return [f"Opp draws line {i}" for i in available]

    def result(self, state, action):
        return self.successor(state)[action]

    def successor(self, state):
        succs = dict()
        # ptsPlr 0 ptsOpp 0 turn agent-a conqueredLines ()
        plr, opp, turn, conc_lines = state
        allLines = self.get_all_lines()
        available_lines = set(allLines.keys()) - set(conc_lines)

        for id_line in available_lines:
            # luckyLineId = random.choice(list(available_lines))
            # luckyLine = allLines[luckyLineId]
            new_conquered = conc_lines + (id_line,)
            drawn_set = {allLines[l_id] for l_id in new_conquered}
            newPts = self.close_boxes(id_line, drawn_set)
            if turn == "agent-a":
                succs[f"Plr draws line {id_line}"]=(newPts,opp,"agent-b",new_conquered)
            else:
                succs[f"Opp draws line {id_line}"]=(plr,newPts,"agent-a",new_conquered)
        return succs

    def goal_test(self, state):
        ptsPlr, ptsOpp, turn, drawnLines = state
        return (len(drawnLines) == self.get_all_lines_length()
                or ptsPlr > self.num_squares() / 2
                or ptsOpp > self.num_squares() / 2)

    def h(self,node):
        state=node.state
        ptsPlr, ptsOpp, turn, drawnLines = state
        conqueredBoxes = ptsPlr+ptsOpp
        remainingBoxes = self.num_squares() - conqueredBoxes
        return remainingBoxes


if __name__ == "__main__":
    game=DotsAndBoxes((0,0,"agent-a",()),2,2)
    goal=0
    # gridLines = game.getAllLines()
    # for line in range(len(gridLines)):
    #     print(gridLines[line])
    # print(gridLines)

    #testiranje igra so A* algoritam

    playgame=astar_search(game)
    print(playgame.solve())
    print(playgame.solution())

    state = game.initial
    while not game.goal_test(state):
        available = game.actions(state)
        chosen_line = random.choice(available)
        state = game.result(state, chosen_line)
        print(f"{state[2]} drew line {chosen_line}, scores: Plr={state[0]} Opp={state[1]}")

    plr, opp, _, _ = state
    print(f"Game over! Final scores -> Plr: {plr}, Opp: {opp}")
    winner = "Plr" if plr > opp else "Opp" if opp > plr else "Draw"
    print(f"Winner: {winner}")


