# Chang MCT
# 2019-01709
# CMSC 170 Exer 1-3
# Description: Source code for A* Algorithm
##################
# Sources:
#

#Section: Constants
GOAL_STATE = [1,2,3,4,5,6,7,8,0]





class Node:
    def __init__ (self, parent, blank, state, action,cost,dist):
        self.parent = parent
        self.blank = blank
        self.state = state
        self.action = action
        self.score = cost+dist
        self.cost = cost
        self.dist = dist

def manhattan(game_state):
    score = 0
    for i in range(0,9):
        if game_state[i]==0:
            continue       
        score= score + abs((game_state[i]-1)%3-i%3)+abs((game_state[i]-1)//3-i//3)
    return score

def swap(list,a,b):
    temp = list[a]
    list[a] = list[b]
    list[b] = temp

def Actions(node):
    children = []
    #Up
    if (node.blank>2):
        new_state = node.state.copy()
        swap(new_state,node.blank-3,node.blank)
        up_child = Node(node,node.blank-3,new_state,"U",node.cost+1,manhattan(new_state))
        children.append(up_child)
    #Left
    if (node.blank%3>0):
        new_state = node.state.copy()
        swap(new_state,node.blank-1,node.blank)
        left_child = Node(node,node.blank-1,new_state,"L",node.cost+1,manhattan(new_state))
        children.append(left_child)    
    #Right
    if (node.blank%3<2):
        new_state = node.state.copy()
        swap(new_state,node.blank,node.blank+1)
        right_child = Node(node,node.blank+1,new_state,"R",node.cost+1,manhattan(new_state))
        children.append(right_child)
    #Down
    if (node.blank<6):
        new_state = node.state.copy()
        swap(new_state,node.blank,node.blank+3)
        down_child = Node(node,node.blank+3,new_state,"D",node.cost+1,manhattan(new_state))
        children.append(down_child)

    return children

def write_solution(node):
    file = open("puzzle.out","w")
    file.write(backtrack(node))
    file.close()

def check_frontier(frontier,node):
    for i in frontier:
        if(i.state==node.state):
            return node
    return None

def backtrack(node):
    str = ""
    temp = node
    while(temp):
        str = temp.action + str
        temp = temp.parent
    return str

def AStar(init_state):

    blank = 0
    
    #get the first blank
    for i in range(0,9):
        if init_state[i] == 0:
            blank = i

    frontier = []
    visited = []

    start_node = Node(None,blank,init_state,"",0,manhattan(init_state))
    explored =0
    frontier.append(start_node)
    while(frontier):
        current_node = frontier.pop(0)
        explored +=1
        visited.append(current_node.state)
        if(current_node.state==GOAL_STATE):
            print(explored)
            print(len(backtrack(current_node)))
            write_solution(current_node)
            return(backtrack(current_node))
        else:
            for node in Actions(current_node):
                temp_node = check_frontier(frontier,node)
                if((node.state not in visited and not temp_node)or (temp_node and (node.cost<temp_node.cost))):
                    #find an index with score greater than current node's score
                    if len(frontier)==0:
                        frontier.append(node)
                    else:
                        for i in range (0,len(frontier)):
                            if node.score<frontier[i].score:
                                frontier.insert(i,node)
                                break
                            elif i == len(frontier)-1:
                                frontier.append(node)
                            
#AStar([1,2,3,4,8,0,7,6,5])
#AStar([2,3,0,1,5,6,4,7,8])                    
#AStar([1,2,3,5,8,7,4,0,6])

#Additional test case
#AStar([8,7,6,5,4,3,2,1,0])