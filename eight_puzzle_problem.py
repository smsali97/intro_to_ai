import queue
from copy import deepcopy
import networkx as nx
from collections import defaultdict
class EightPuzzle():

    FINAL_STATE = [['1','2','3'],['4','_','5'],['6','7','8']]

    '''
    Checks if the specified tile (r,c) is blank
    '''
    def isBlankTile(self,r,c):
        return self.state[r][c] is '_'

    '''
    Checks if the Eight Puzzle in the final state or not
    '''
    def inFinalState(self):
        for i in range(3):
            for j in range(3):
                if not self.state[i][j] is self.FINAL_STATE[i][j]:
                    return False
        return True

    '''
    Swaps the two tiles: T1 (r1,c1) T2 (r2,c2) and updates the blank tile
    '''
    def swapTile(self,r1,c1,r2,c2):
        self.state[r1][c1], self.state[r2][c2] = self.state[r2][c2], self.state[r1][c1]

    '''
    Swaps the two tiles: Blank Tile and T1 (r1,c1) and updates the blank tile
    '''
    def swapBlankTile(self,r1,c1):
        self.blankCoords = self.getBlankCoords()
        self.swapTile(self.blankCoords[0],self.blankCoords[1],r1,c1)
        self.blankCoords = (r1,c1)

    '''

    Gets coordinates of the blank tile
    '''
    def getBlankCoords(self):
        for i in range(3):
            for j in range(3):
                if self.state[i][j]  is '_':
                    return (i,j)
        return (-1,-1)

    '''
    String representation of puzzle
    '''
    def my_repr(self,level,flag):
        greenStuff = 'GOAL STATE --> '
        temp_str = ''

        for i in self.state:
            if (flag):
                temp_str += greenStuff
            temp_str += "  "*level+ ' | '.join(i) + '\n'
        return temp_str

    def __str__(self, level=0):
        flag = False
        if (self.inFinalState()): flag = True
        ret = self.my_repr(level,flag)+"\n"
        for child in self.children:
            ret += child.__str__(level+1)
        return ret

    def my_print(self,level):
        temp_str = ""
        for i in self.state:
            temp_str += "  "*level + ' | '.join(i) + '\n'
        print(temp_str)
        return


    '''
    Constructor
    '''
    def __init__(self,state):
        self.state = state
        self.blankCoords = self.getBlankCoords()
        self.FINAL_STATE = EightPuzzle.FINAL_STATE
        self.children = []
        self.graph = nx.DiGraph()
        self.visited = False
        self.parent = None

    def __lt__(self, other):
        return str(self) < str(other)

    '''
    Given a state generates the next possible states
    '''
    def nextStates(self):
        nextStates = list()
        x, y = self.getBlankCoords()
        for i in [x-1,x+1]:
            # out of bounds
            if i is -1 or i is 3: continue
            new_state = deepcopy(self.state)
            new_node = EightPuzzle(new_state)
            new_node.swapBlankTile(i,y)
            nextStates.append(new_node)

        for i in [y-1,y+1]:
            # out of bounds
            if i is -1 or i is 3: continue
            new_state = deepcopy(self.state)
            new_node = EightPuzzle(new_state)
            new_node.swapBlankTile(x,i)
            nextStates.append(new_node)
        return nextStates

    '''
    Performs BFS
    '''
    def BFS(self):
        level = 0
        Q = queue.Queue()
        Q.put(self) #put initial state first until its and all its children are visited
        self.visited = True
        is_visited = defaultdict(bool)
        is_visited[str(self.state)] = True
        ctr = 0
        while (not Q.empty()):
            v = Q.get()
            # print(v)
            if (v.inFinalState()):
                print("Iterations took: " + str(ctr))
                return
            ctr += 1

            for neighbor in v.nextStates():
                if neighbor.inFinalState():
                    neighbor.parent = v

                    temp = neighbor
                    output = ""
                    while (temp is not None):
                        output = temp.my_repr(flag=False,level=0) + '\n \\\ followed by //\n\n' + output
                        temp = temp.parent
                    print(output)
                    print("Iterations took: " + str(ctr))

                    return
                if not is_visited[str(neighbor.state)]:
                    neighbor.parent = v
                    Q.put(neighbor)
                    is_visited[str(neighbor.state)] = True
                    v.children.append(neighbor)

    '''
    Performs A* Search
    '''
    def A_star_search(self,heuristic='manhattan'):
        pQ = queue.PriorityQueue()
        if heuristic is 'manhattan':
            pQ.put((self.manhattanDistance(),self))
        else:
            pQ.put((self.sumNoOfTilesDisplaced(),self))
        is_visited = defaultdict(bool)
        is_visited[str(self)] = True
        ctr = 0
        while (not pQ.empty()):
            ctr += 1
            v = pQ.get()[1]
            # print(v)
            if (v.inFinalState()):
                temp = v
                output = ""
                while (temp is not None):
                    output = temp.my_repr(flag=False,level=0) + '\n \\\ followed by //\n\n' + output
                    temp = temp.parent
                print(output)
                print("Iterations took: " + str(ctr))
                return
            for child in v.nextStates():
                if not is_visited[str(child)]:
                    child.parent = v
                    if heuristic is 'manhattan':
                        x = (child.manhattanDistance(),child)
                    else:
                        x = (child.sumNoOfTilesDisplaced(),child)
                    is_visited[str(child)] = True
                    pQ.put(x)

    '''
    Number of tiles displaced from goal state
    '''
    def sumNoOfTilesDisplaced(self):
        ctr = 0
        for i in range(3):
            for j in range(3):
                if not self.state[i][j] is self.FINAL_STATE[i][j]:
                    ctr += 1
        return ctr
    '''
    Finds location (i,j) of the specifed tile
    '''
    def findLocation(self,specified_tile):
        for i in range(3):
            for j in range(3):
                if specified_tile is self.FINAL_STATE[i][j]:
                    return (i,j)
        return (None,None)

    '''
    Computes manhattand Distance of the self state to the goal state
    '''
    def manhattanDistance(self):
        manSum = 0
        for i in range(3):
            for j in range(3):
                goal_i, goal_j = self.findLocation(self.state[i][j])
                manSum += abs(goal_i - i) + abs(goal_j - j)
        return manSum


def main():
    # inital config
    eightPuzzle = EightPuzzle([['3','1','4'],['_','8','5'],['2','6','7']])
    x = input("Please type a number: \n 1 for BFS \n 2 for A* (Manhattan) \n 3 for A* (Sum of Tiles Displaced) \n 4 for exit\n")
    if x is "1":
        eightPuzzle.BFS()
    elif x is "2":
        eightPuzzle.A_star_search(heuristic='manhattan')
    elif x is "3":
        eightPuzzle.A_star_search(heuristic='tiles displaced')
    elif x is "4":
        print("Bye!")
        exit()
    else:
        print("Tch. Cannot obey simple rules. ")
        exit()

if __name__ == '__main__':
    main()
