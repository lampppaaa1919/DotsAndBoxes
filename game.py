from random import random

from searching_framework import Problem, astar_search
from searching_framework.genetic import *

class DotsAndBoxes(Problem):
    def __init__(self, initial, n, m):
        super().__init__(initial,goal)
        self.n=n
        self.m=m

    def getAllLines(self):
        allLines = dict()
        totalLines = 0
        for i in range(self.n):
            for j in range(self.m):
                if i + 1 < 4:
                    allLines[totalLines] = ((i, j), (i + 1, j))
                    totalLines += 1
                if j + 1 < 4:
                    allLines[totalLines] = ((i, j), (i, j + 1))
                    totalLines += 1
        return allLines

    def numSquares(self):
        return (self.n-1) * (self.m-1)

    def getAllLinesLength(self):
        allLines = self.getAllLines()
        return len(allLines)

    def addLine(self, agent, newLineId):
        #((i1,j1),(i2,j2))=newLine
        if newLineId not in self.conquered_lines.vals():
            self.conquered_lines[agent].append(newLineId)

    def closeBoxes(self, drawnLine):
        pts=0
        ((i1,j1),(i2,j2))=drawnLine
        if i1==i2:
            i=i1
            #linijata ja zatvara kutijata nad nea
            if ((i-1,j1),(i-1,j2)) in self.conquered_lines.vals() \
                and ((i-1,j1),(i,j1)) in self.conquered_lines.vals() \
                and ((i-1,j2),(i,j2)) in self.conquered_lines.vals() \
                and i>0: pts+=1
            # linijata ja zatvara kutijata pod nea
            if (((i+1,j1),(i+1,j2)) in self.conquered_lines.vals()
                    and ((i+1,j1),(i,j1)) in self.conquered_lines.vals()
                    and ((i+1,j2),(i,j2)) in self.conquered_lines.vals()
                    and i<self.n-1): pts+=1
        elif j1==j2:
            j=j1
            #linijata ja zatvara levata kutija
            if (((i1,j-1),(i2,j-1)) in self.conquered_lines.vals()
                    and ((i1,j-1),(i1,j)) in self.conquered_lines.vals()
                    and ((i2,j-1),(i2,j)) in self.conquered_lines.vals()
                    and j>0): pts+=1
            #linijata ja zatvara desnata kutija
            if (((i1,j+1),(i2,j+1)) in self.conquered_lines.vals()
                    and ((i1,j+1),(i1,j)) in self.conquered_lines.vals()
                    and ((i2,j+1),(i2,j)) in self.conquered_lines.vals()
                    and j<self.m-1): pts+=1
        return pts


    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def successor(self, state):
        succs = dict()
        # ptsPlr 0 ptsOpp 0 turn agent-a
        plr, opp, turn = state
        luckyLineId = int(random())*self.getAllLinesLength()
        luckyLine = self.getAllLines()[luckyLineId].val()
        newPts = self.closeBoxes(luckyLine)
        if turn == "agent-a":
            succs["Plr draws line "+luckyLineId]=(newPts,opp,"agent-b",conquered_lines)
        else:
            succs["Opp draws line "+luckyLineId]=(plr,newPts,"agent-a",conquered_lines)
        return succs

    def goal_test(self, state):
        ptsPlr, ptsOpp, turn, drawnLines = state
        return (len(drawnLines)==self.getAllLinesLength()
                or ptsPlr>self.numSquares()/2
                or ptsOpp>self.numSquares()/2)

    def h(self,node):
        state=node.state
        ptsPlr, ptsOpp, turn, drawnLines = state
        conqueredBoxes = ptsPlr+ptsOpp
        remainingBoxes = self.numSquares()-conqueredBoxes
        return remainingBoxes


if __name__ == "__main__":
    goal=0
    conquered_lines = {}
    game=DotsAndBoxes((0,0,"agent-a",conquered_lines),conquered_lines,4,4)
    # gridLines = game.getAllLines()
    # for line in range(len(gridLines)):
    #     print(gridLines[line])
    # print(gridLines)

    #testiranje igra so A* algoritam

    playgame=astar_search(game)
    print(playgame.solve())
    print(playgame.solution())


