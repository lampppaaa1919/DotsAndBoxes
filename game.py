from searching_framework import Problem

class DotsAndBoxes(Problem):
    def __init__(self, dots, lines, initial):
        super().__init__(initial)
        self.initial=(player,opp)
        self.dots = dots
        self.lines = lines

    def availableDots(self,dots,lines):
        available=0
        for d in dots:
            if d not in lines:
                available+=1
        return available

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def successor(self, state):
        succs = dict()

        pass
        #TODO

        return succs

    def goal_test(self, state):
        return state == self.goal

    def heuristic(self, state):
        return self.availableDots(state,self.dots,self.lines)


class Agent:
    def __init__(self,lines, points):
        self.lines = lines
        self.points = points

    def addLine(self, i1, j1, i2, j2):
        gridLines.append(((i1, j1), (i2, j2)))

    def isSquare(self):
        for line in ():
            if line not in self.lines : return False
        return True

if __name__ == "__main__":
    player = Agent((),0)
    opp = Agent((),0)
    gridDots = list()
    gridLines = list()
    for i in range(4):
        for j in range(4):
            gridDots.append((i, j, "free"))
    game = DotsAndBoxes(gridDots, gridLines, (player,opp))
    print(gridDots)