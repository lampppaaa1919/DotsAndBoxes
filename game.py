from random import random

from searching_framework import Problem, astar_search


class DotsAndBoxes(Problem):
    def __init__(self, initial, conquered_lines):
        super().__init__(initial,goal)
        self.conquered_lines = conquered_lines

    def addLine(self, i1, i2, j1, j2):
        lines=list(self.conquered_lines)
        new_line=( (i1,j1) , (i2,j2) )
        if new_line not in lines:
            lines.append(new_line)
        return tuple(lines)

    def conquerSquares(self, line, pts):
        (i1,j1),(i2,j2) = line
        if i1==i2:
            if i1<3:
                if ((i1+1,j1),(i2+1,j2)) in self.conquered_lines and \
                        ((i1,j1),(i1+1,j1)) in self.conquered_lines and \
                        ((i2,j2),(i2+1,j2)) in self.conquered_lines:
                    pts+=1
            elif i1>0:
                if ((i1-1,j1),(i2-1,j2)) in self.conquered_lines and \
                        ((i1,j1),(i1-1,j1)) in self.conquered_lines and \
                        ((i2,j2),(i2-1,j2)) in self.conquered_lines:
                    pts+=1
        elif j1==j2:
            if j1<3:
                if((i1,j1),(i1+1,j1)) in self.conquered_lines and \
                        ((i1,j1),(i1,j1+1)) in self.conquered_lines and \
                        ((i1+1,j1),(i2+1,j2) in self.conquered_lines):
                    pts+=1
            elif j1>0:
                if((i1,j1),(i1-1,j1)) in self.conquered_lines and \
                        ((i2,j2),(i2-1,j2)) in self.conquered_lines and \
                        ((i1-1,j1),(i2-1,j2)) in self.conquered_lines:
                    pts+=1
        return pts



    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def successor(self, state):
        succs = dict()
        # ptsPlr 0 ptsOpp 0 turn agent-a
        plr, opp, turn = state
        #kje se bira od funkciite vo genetic
        new_line = index(int(random()))[-1]
        conquered_lines = self.addLine(new_line)
        if turn == "agent-a":
            self.conquerSquares(new_line, plr)
            succs["Igrachot ja nacrta linijata "+index]=(plr, opp, "agent-b")
        elif turn == "agent-b":
            self.conquerSquares(new_line, opp)
            succs["Protivnikot ja nacrta linijata "+index]=(plr, opp, "agent-a")
        return succs

    def goal_test(self, goal):
        return self.goal == goal

def getAllLines(n,m):
    allLines = list()
    totalLines=0
    for i in range(n):
        for j in range(m):
            if i+1<4:
                allLines.append((totalLines,(i,j),(i+1,j)))
                totalLines+=1
            if j+1<4:
                allLines.append((totalLines,(i,j),(i,j+1)))
                totalLines+=1
    return tuple(allLines)+(allLines,)

if __name__ == "__main__":
    goal=0
    conquered_lines = ()
    gridLines = getAllLines(4,4)
    game=DotsAndBoxes((0,0,"agent-a"),conquered_lines)
    playgame=astar_search(game)
    print(playgame.solve())
    print(playgame.solution())
    # for line in gridLines:
    #     print(line)
