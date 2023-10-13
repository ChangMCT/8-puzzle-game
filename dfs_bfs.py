# Chang MCT
# 2019-01709
# CMSC 170 Exer 1-3
# Description: Source code for DFS and BFS algorithms
##################
# Sources:
# 


#Section: Constants
GOAL_STATE = [1,2,3,4,5,6,7,8,0]
MAX_DEPTH = 16
#Section: Classes
class Node:
    def __init__ (self, blank, state, actions):
        self.blank = blank
        self.state = state
        self.actions = actions
        
def swap(list,a,b):
    temp = list[a]
    list[a] = list[b]
    list[b] = temp

def write_solution(node):
    file = open("puzzle.out","w")
    file.write(node.actions)
    file.close()


#Returns a list of nodes after said action
def Actions(node):
    children = []
    #Up
    if (node.blank>2):
        new_state = node.state.copy()
        swap(new_state,node.blank-3,node.blank)
        up_child = Node(node.blank-3,new_state,node.actions+"U")
        children.append(up_child)
    #Right
    if (node.blank%3<2):
        new_state = node.state.copy()
        swap(new_state,node.blank,node.blank+1)
        right_child = Node(node.blank+1,new_state,node.actions+"R")
        children.append(right_child)
    #Down
    if (node.blank<6):
        new_state = node.state.copy()
        swap(new_state,node.blank,node.blank+3)
        down_child = Node(node.blank+3,new_state,node.actions+"D")
        children.append(down_child)
    #Left
    if (node.blank%3>0):
        new_state = node.state.copy()
        swap(new_state,node.blank-1,node.blank)
        left_child = Node(node.blank-1,new_state,node.actions+"L")
        children.append(left_child)   

    return children

def BFS(init_state):
    blank = 0
    
    #get the first blank
    for i in range(0,9):
        if init_state[i] == 0:
            blank = i

    actions = []
    frontier = []
    visited = []
    root = Node(blank,init_state,"")

    frontier.append(root)
    explored = 0
    while(frontier):
        current_node = frontier.pop(0)
        visited.append(current_node.state)
        explored+=1
        if(current_node.state==GOAL_STATE):
            print(explored)
            print(len(current_node.actions))
            write_solution(current_node)
            return current_node.actions
        else:
            for node in Actions(current_node):
                if((not check_frontier(frontier,node)) and (node.state not in visited)):
                    frontier.append(node)
    return None

def check_frontier(frontier,node):
    for i in frontier:
        if(i.state==node.state):
            return True
    return False

def DFS(init_state):
    blank = 0
    
    #get the first blank
    for i in range(0,9):
        if init_state[i] == 0:
            blank = i

    actions = []
    frontier = []
    visited = []
    root = Node(blank,init_state,"")

    frontier.append(root)
    explored = 0
    while(frontier):
        current_node = frontier.pop()
        explored+=1
        if(explored%1000==0):
            print(explored)
        visited.append(current_node.state)
        if(current_node.state==GOAL_STATE):
            print(explored)
            print(len(current_node.actions))
            write_solution(current_node)
            return current_node.actions
        else:
            for node in Actions(current_node):
                if((not check_frontier(frontier,node)) and (node.state not in visited)):
                    frontier.append(node)
    return None