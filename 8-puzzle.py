import PySimpleGUI
import time
from copy import deepcopy
from math import sqrt
import heapq


def get_position(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                position = (i,j)
                return position


def swap(state, pos1, pos2):
    temp = state[pos1[0]][pos1[1]]
    state[pos1[0]][pos1[1]] = state[pos2[0]][pos2[1]]
    state[pos2[0]][pos2[1]] = temp

def copy_state(state):
    copy = [[0 for i in range(3)] for j in range(3)]
    for i in range(3):
        for j in range(3):
            copy[i][j] = state[i][j]
    return copy

def get_neighbors(state, parent_index):
    neighbors = []
    position = get_position(state)
    
    # left
    if position[1] > 0:
        pos1 = position
        pos2 = (position[0], position[1] - 1)
        left_neighbor = copy_state(state) 
        swap(left_neighbor, pos1, pos2)
        left_neighbor = (left_neighbor, parent_index)
        neighbors.append(left_neighbor)

    # right
    if position[1] < 2:
        pos1 = position
        pos2 = (position[0], position[1] + 1)
        right_neighbor = copy_state(state) 
        swap(right_neighbor, pos1, pos2)
        right_neighbor = (right_neighbor, parent_index)
        neighbors.append(right_neighbor)

    # up
    if position[0] > 0:
        pos1 = position
        pos2 = (position[0] - 1, position[1])
        up_neighbor = copy_state(state) 
        swap(up_neighbor, pos1, pos2)
        up_neighbor = (up_neighbor, parent_index)
        neighbors.append(up_neighbor)
        
    # down
    if position[0] < 2:
        pos1 = position
        pos2 = (position[0] + 1, position[1])
        down_neighbor = copy_state(state) 
        swap(down_neighbor, pos1, pos2)
        down_neighbor = (down_neighbor, parent_index)
        neighbors.append(down_neighbor)

    return neighbors
    


def set_initial_state(state):
    state = state.split()
    ctr = 0
    initial_state = [[0 for i in range(3)] for j in range(3)]
    for i in range(3):
        for j in range(3):
            initial_state[i][j] = int(state[ctr])
            ctr += 1
    return (initial_state, -1)

def compare_states(state1, state2):
    for i in range(3):
        for j in range(3):
            if state1[i][j] != state2[i][j]:
                return False
    return True

def check_if_included(state, src):
    for i in range(len(src)):
        if compare_states(state[0], src[i][0]) == True:
            return True
    return False

def get_path_indices(explored):
    current_state = explored[-1]
    path = []
    path.append(-1)
    while True:
        parent = current_state[1]
        if parent == -1:
            return path
        path.append(parent)
        current_state = explored[parent]

def get_path(explored):
    path = get_path_indices(explored)
    solution = []
    for i in range(len(path)):
        solution.append(explored[path.pop(-1)][0])
    return solution


def BFS(initial_state):
    frontier = []
    frontier.append(initial_state)
    explored = []
    goal_state = [[0,1,2],[3,4,5],[6,7,8]]
    parent_index = 0
    while len(frontier) != 0:
        current_state = frontier.pop(0)
        explored.append(current_state)
        if compare_states(current_state[0], goal_state):         
            return explored
        neighbors = get_neighbors(current_state[0], parent_index)
        for i in range(len(neighbors)):
            if check_if_included(neighbors[i], frontier) == False and check_if_included(neighbors[i], explored) == False:
                frontier.append(neighbors[i])
        parent_index += 1
    return False

ansmat = [[i,i+1,i+2] for i in [0,3,6]]
# the solved state matrix

def manhatan(pos):  #calculate the manhattan distance
    eval = 0
    for i in range(3):
        for j in range(3):
            eval = eval + abs( pos[i][j]/3 - i ) + abs( pos[i][j]%3 - j ) 
            # for each cell add it's displacement in x and displacement in y
    return eval

def euclid(pos):    #calculate the euclidean distance
    eval = 0
    for i in range(3):
        for j in range(3):
            eval = eval +  sqrt( ( pos[i][j]/3 - i )**2 + ( pos[i][j]%3 - j )**2 ) 
            # for each cell add the square root of it's displacement in x squared and in y squarred
    return sqrt(eval)


class board:    # class for each state
    def __init__(self,pos , point = None ):
        self.pos = pos  # state's position
        self.track = [] # history from initial state's position to this position
        
        if point == None:               # get the x and y of the "moving" 0 cell
            self.freeCell = self.getFreeCell()  # find it's coordinates if not specified in the constructor
        else:
            self.freeCell = point       # if cell was given in the constructor

    def getFreeCell(self):
        for i in range(3):
            for j in range(3):
                if self.pos[i][j]==0:   # linear loop until 0 is found
                    return (i,j)        # return coordinates

    def getPossibleMoves(self):
        self.moves = []
        if self.freeCell[1] > 0: # if not on the leftmost column add move left's coordinates
            self.moves.append( ( self.freeCell[0] , self.freeCell[1] - 1 ) )
        if self.freeCell[1] < 2: # if not on the rightmost column add move right's coordinates
            self.moves.append( ( self.freeCell[0] , self.freeCell[1] + 1 ) )
        if self.freeCell[0] > 0: # if not on the top row add move up's coordinates
            self.moves.append( ( self.freeCell[0] - 1 , self.freeCell[1] ) )
        if self.freeCell[0] < 2: # if not on the bottom row add move down's coordinates
            self.moves.append( ( self.freeCell[0] + 1 , self.freeCell[1] ) )

    def swap(self,point): # swap freecell with another given point
        (self.pos[point[0]][point[1]] , self.pos[self.freeCell[0]][self.freeCell[1]]) = \
        (self.pos[self.freeCell[0]][self.freeCell[1]] , self.pos[point[0]][point[1]])

        self.freeCell = point

    def visitEval(self): # function to get a 1:1 mapping from each state to an integer 
        eval = 0         # using a 9^n system
        for i in range(3):
            for j in range(3):
                eval = eval + self.pos[i][j] * ( 9 ** ( i*3 + j ) )
        return eval

    def DFS(self):
        frontier = []   # initialize the stack
        dfsDict = {}    # initialize lookup table
        frontier.append(self)  # push initial state into stack
        while (frontier):
            temp = frontier.pop() 
            temp.track.append(deepcopy(temp.pos)) # update the path with this state
            visit = temp.visitEval()
            dfsDict.update( { visit:visit } )     # add this state to the look up table
            if temp.pos == ansmat:                # check if current state is the solution
                self.track = temp.track           # check if current state is the solution
                print('\x1b[6;30;42m' + f'Solution in {len(self.track)} moves ' + '\x1b[0m')
                # for i in range(self.track):
                #     print(self.track[i])          # print path to the solution
                return True
            temp.getPossibleMoves()               # get states neighbors  
            for (i,j) in temp.moves:
                temp1 = deepcopy(temp)            
                temp1.swap((i,j))
                if temp1.pos not in [frontier[iter].pos for iter in range(len(frontier)) ]:
                    if temp1.visitEval() not in dfsDict:    # for each neighbor check if not in stack nor lookup table
                        frontier.append(temp1)              # push it into stack
        return False 
    


    def aStar(self,isEuclid = True):
        frontier = []   # initialize the heap
        frontier.append( ( 0 , self ) ) # add initial state into heap value is irrelevant since it is minimum by default
        heapq.heapify(frontier)
        asDict = {}     # initialize lookup table 
        while (frontier):
            temp = heapq.heappop(frontier)[1]     # get minimum approximate distance state from heap
            temp.track.append(deepcopy(temp.pos)) # update the path with this state
            visit = temp.visitEval()
            asDict.update( { visit:visit } )      # add this state to the look up table
            if temp.pos == ansmat:
                self.track = temp.track           # check if current state is the solution
                print('\x1b[6;30;42m' + f'Solution in {len(self.track)} moves ' + '\x1b[0m')
                # for i in range(self.track):
                #     print(self.track[i])          # print path to the solution
                return True

            temp.getPossibleMoves()               # get states neighbors  
            for (i,j) in temp.moves:              # for each neighbor
                temp1 = deepcopy(temp)            
                temp1.swap((i,j))
                if temp1.pos not in [frontier[iter][1].pos for iter in range(len(frontier)) ]: # if not in the heap
                    if temp1.visitEval() not in asDict:     # if not in the lookup table
                        if isEuclid:                        # calculate the approximate distance value
                            val = euclid(temp1.pos)         # either by euclidean distance or manhattan distance
                        else:
                            val = manhatan(temp1.pos)
                        heapq.heappush( frontier , ( val , temp1) ) # push into heap the state and position it in heap according
                                                                    # to aforemetioned calculated approximate distance
        return False 



def GUI():
    layout =[
        [PySimpleGUI.T('enter the puzzle in row major order separated \nwith spaces')],
        [PySimpleGUI.In(key='textbox')],
        [PySimpleGUI.Radio('BFS', 1, pad=(5, 10), key='BFS'), 
        PySimpleGUI.Radio('DFS', 1, pad=(5, 10), key='DFS'), 
        PySimpleGUI.Radio('A*Man', 1, pad=(5, 10), key='A*Man'),
        PySimpleGUI.Radio('A*Euc', 1, pad=(5, 10), key='A*Euc')
        ],
        [PySimpleGUI.Btn('Solve', pad=(118,8))]
        ]
    btn_row = []
    for i in range(3):
        for j in range(3):
            btn_row.append(PySimpleGUI.Button(size=(6,3), pad=(18,5), key=('btn'+str(i)+str(j))))
        layout.append(btn_row)
        btn_row = []
    window = PySimpleGUI.Window("8-puzzle solver",layout, size = (300,375))
    while True:
        event, values = window.read()
        if event == PySimpleGUI.WIN_CLOSED:
            window.close()
            break    
        if event == "Solve":
            input_initial_state = values['textbox']
            initial_state = set_initial_state(input_initial_state)
            if values['BFS'] == True:
                explored = BFS(initial_state)
                solution = get_path(explored)
            if values['DFS'] == True:
                b = board(initial_state[0])
                b.DFS()
                solution = b.track
            if values['A*Man'] == True:
                b = board(initial_state[0])
                b.aStar(False)
                solution = b.track
            if values['A*Euc'] == True:
                b = board(initial_state[0])
                b.aStar(True)
                solution = b.track           
            for state in solution:
                for i in range(3):
                    for j in range(3):
                        window['btn'+str(i)+str(j)].update(state[i][j])
                        window.finalize()
                time.sleep(1)

GUI()
