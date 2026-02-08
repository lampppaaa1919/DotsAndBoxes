from searching_framework import Problem

class DotsAndBoxes(Problem):
    def __init__(self, initial, goal, conquered_lines):
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
            
                    

    def actions(self, state):
        return self.successor(state).keys()

    def result(self, state, action):
        return self.successor(state)[action]

    def successor(self, state):
        succs = dict()
        
        return succs

    def goal_test(self, goal):
        return self.goal == goal



if __name__ == "__main__":
    goal=0
    conquered_lines = ()
    gridLines = list()
    for i in range(4):
        for j in range(4):
            if i+1<4:
                gridLines.append((goal,(i,j),(i+1,j)))
                goal+=1
            if j+1<4:
                gridLines.append((goal,(i,j),(i,j+1)))
                goal+=1
    game=DotsAndBoxes((0,0,"agent-a"),goal,conquered_lines)
    # for line in gridLines:
    #     print(line)
