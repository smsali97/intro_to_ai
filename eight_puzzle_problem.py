import queue

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
                if not self.state[i][j] is FINAL_STATE[i][j]:
                    return False
        return True

    '''
    Swaps the two tiles: T1 (r1,c1) T2 (r2,c2)
    '''
    def swapTile(self,r1,c1,r2,c2):
        self.state[r1][c1], self.state[r2][c2] = self.state[r2][c2], self.state[r1][c1]


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
    def __str__(self):
        temp_str = ''
        for i in self.state:
            temp_str += ' | '.join(i) + '\n'
        return temp_str

    '''
    Constructor
    '''
    def __init__(self,state):
        self.state = state
        self.blankCoords = self.getBlankCoords()
        children = []


def main():
    # inital config
    eightPuzzle = EightPuzzle([['3','1','4'],['_','8','5'],['2','6','7']])
    print(eightPuzzle)
    print(eightPuzzle.blankCoords)

    queue = queue.Queue()
    queue.put(eightPuzzle)

    while not queue.empty():
        curr_node = queue.get()

        for i in range(curr_node)



if __name__ == '__main__':
    main()
