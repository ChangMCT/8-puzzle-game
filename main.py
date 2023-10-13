# Chang MCT
# Description: Game screen for 8 puzzle game
##################
# Sources:
# [1]: https://stackoverflow.com/questions/10990137/pygame-mouse-clicking-detection
# [2]: https://www.geeksforgeeks.org/check-instance-8-puzzle-solvable/

#Section: Imports
from tabnanny import check
from tkinter import * 
from tkinter.filedialog import askopenfilename
import pygame
import time
import dfs_bfs
import a_star

#Section: Constants
WHITE = (255,255,255)
BLOCK_COLOR = (238,139,142)
BUTTON_COLOR = (32,192,32)
DEFAULT_OUTLINE = (192,32,32)
HIGHLIGHT_OUTLINE = (32,32,192)
BLOCK_SIZE = 100
PUZZLE_START_X = 250
PUZZLE_START_Y = 80
GOAL_STATE = [1,2,3,4,5,6,7,8,0]
STEP_LIMIT = 45
#Section: Global vars
screen = 0
game_state = [1,2,3,4,5,6,7,8,0]
init_state = 0
blank= 8
playing = True
solver = 0
solution = None
step = 0
#Reads file input and loads it into game state
def read_input(filename):
    global game_state, blank, init_state
    
    try:
        input = open(filename,"r")
    except:
        print("Could not find file: puzzle. \n Exiting...")
        exit(1)
    
    #temp array for storage
    cells = []
    
    try:
        #Get each line and load content as array of int
        for i in range (0,3):
            nums = input.readline().split()
            for j in range (0,3):
                if(int(nums[j])>-1 and int(nums[j])<9):
                    cells.append(int(nums[j]))
                else:    
                    print("Got unexpected input. \nExiting...")
                    exit(1)
        #Load into game state
        game_state = cells
        init_state = cells.copy()
        #Locate the blank cell
        for i in range(0,9):
            if(game_state[i]==0):
                blank = i
                break
    except:
        print("Input file contains deformed content. \nExiting...")
        exit(1)
    
    input.close()

#Checks if puzzle is solved already
def check_solved():
    global screen

    msg_font = pygame.font.SysFont('Century Gothic', 30)

    if(game_state==GOAL_STATE):
        pygame.draw.rect(screen, WHITE, pygame.Rect(275, 20, 400,40))
        msg = msg_font.render('Congrats!',False,(0,0,0))
        screen.blit(msg, (325,20))
        pygame.display.flip()
        
        return True
        
    return False

#Checks if puzzle is solvable
#This function is a modified from [2]
def solvable():
    is_solvable = True
    for i in range (0,9):
        for j in range(i+1,9):
            if game_state[j]!= 0 and game_state[i] != 0 and game_state[i]>game_state[j]:
                is_solvable = not is_solvable
    return is_solvable

#Checks if block mentioned is a neighbor of b
def neighbor(tile):
    if(tile%3>0 and tile-1==blank):
        return True
    if(tile%3<2 and tile+1==blank):
        return True
    if(tile//3>0 and tile-3==blank):
        return True
    if(tile//3<2 and tile+3==blank):
        return True
    return False

#Resets puzzle and UI back to its initial state
def solverUI_init():
    
    global screen,init_state, game_state, blank
    game_state = init_state.copy()
    block_font = pygame.font.SysFont('Century Gothic', 50)
    button_font = pygame.font.SysFont('Century Gothic', 30)    
    for i in range(0,9):
        if init_state[i]==0:
            blank = i
            break

    screen.fill(WHITE)
    #Initialize 8-puzzle blocks
    for i in range(0,len(game_state)):    
        x_start = (i%3)*BLOCK_SIZE + PUZZLE_START_X
        y_start = (i//3)*BLOCK_SIZE + PUZZLE_START_Y
        if game_state[i] >0 :   
            pygame.draw.rect(screen, BLOCK_COLOR, pygame.Rect(x_start, y_start, BLOCK_SIZE-1,BLOCK_SIZE-1))
            screen.blit(block_font.render(str(game_state[i]),False,WHITE), (x_start+25,y_start+25))

    pygame.draw.rect(screen, BLOCK_COLOR, pygame.Rect(355, 395, 80,45))
    screen.blit(button_font.render('NEXT',False,WHITE), (360,400))

#Swaps two items
def swap(list,a,b):
    temp = list[a]
    list[a] = list[b]
    list[b] = temp
    
#Handles swapping for solution step
def solverStep(action):
    global screen, game_state, blank
    block_font = pygame.font.SysFont('Century Gothic', 50)
    x = (blank%3)*100+PUZZLE_START_X
    y = (blank//3)*100+PUZZLE_START_Y
    x_old = x
    y_old = y
    temp_blank = blank
    if(action=="U"):
        swap(game_state,blank,blank-3)
        y_old -= 100
        temp_blank-=3
    elif(action=="L"):
        swap(game_state,blank,blank-1)
        x_old -= 100
        temp_blank-=1
    elif(action=="R"):
        swap(game_state,blank,blank+1)
        x_old += 100
        temp_blank+=1
    elif(action=="D"):
        swap(game_state,blank,blank+3) 
        y_old += 100 
        temp_blank+=3

    #Update cells after swapping values
    pygame.draw.rect(screen, WHITE, pygame.Rect(x_old,y_old, BLOCK_SIZE-1,BLOCK_SIZE-1))
    pygame.draw.rect(screen, BLOCK_COLOR, pygame.Rect(x,y, BLOCK_SIZE-1,BLOCK_SIZE-1))
    screen.blit(block_font.render(str(game_state[blank]),False,WHITE), (x+25,y+25))       
    blank = temp_blank

#Handles click events and display state
def handle_click(pos):
    x = pos[0]
    y = pos[1]
    #Checks what UI part of game is hit
    #Note: Would recommend implementing rectangular collisions
    global playing

    if playing:
        if( x>=PUZZLE_START_X and x<= PUZZLE_START_X+300 and y>=PUZZLE_START_Y and y<= PUZZLE_START_Y+300):
            
            global screen,blank,solver,solution,step
                
            block_font = pygame.font.SysFont('Century Gothic', 50)
            x = x - PUZZLE_START_X
            y = y - PUZZLE_START_Y
            x = x//BLOCK_SIZE
            y = y//BLOCK_SIZE
            tile = x+y*3
            # Swap if clicked tile and blank tile are neigbors
            if(neighbor(tile)):

                temp = game_state[tile]
                game_state[tile] = game_state[blank]
                game_state[blank] = temp

                new_cell_x = (blank%3)*BLOCK_SIZE + PUZZLE_START_X
                new_cell_y = (blank//3)*BLOCK_SIZE + PUZZLE_START_Y
                
                #Update the board
                pygame.draw.rect(screen, WHITE, pygame.Rect(x*100+PUZZLE_START_X,y*100+PUZZLE_START_Y, BLOCK_SIZE-1,BLOCK_SIZE-1))
                pygame.draw.rect(screen, BLOCK_COLOR, pygame.Rect(new_cell_x, new_cell_y, BLOCK_SIZE-1,BLOCK_SIZE-1))
                screen.blit(block_font.render(str(game_state[blank]),False,WHITE), (new_cell_x+25,new_cell_y+25))            
                blank = tile
                check_solved()

        #BFS Selector
        if(x>=215 and x<=285 and y>=395 and y<=440):
            pygame.draw.rect(screen, HIGHLIGHT_OUTLINE, pygame.Rect(215, 395, 70,45),5)
            pygame.draw.rect(screen, DEFAULT_OUTLINE, pygame.Rect(215, 445, 70,45),5)
            pygame.draw.rect(screen, DEFAULT_OUTLINE, pygame.Rect(215, 495, 70,45),5)
            solver = 1

        #DFS Selector
        if(x>=215 and x<=285 and y>=445 and y<=490):
            pygame.draw.rect(screen, DEFAULT_OUTLINE, pygame.Rect(215, 395, 70,45),5)
            pygame.draw.rect(screen, HIGHLIGHT_OUTLINE, pygame.Rect(215, 445, 70,45),5)
            pygame.draw.rect(screen, DEFAULT_OUTLINE, pygame.Rect(215, 495, 70,45),5)
            solver = 2

        if(x>=215 and x<=285 and y>=495 and y<=540):
            pygame.draw.rect(screen, DEFAULT_OUTLINE, pygame.Rect(215, 395, 70,45),5)
            pygame.draw.rect(screen, DEFAULT_OUTLINE, pygame.Rect(215, 445, 70,45),5)
            pygame.draw.rect(screen, HIGHLIGHT_OUTLINE, pygame.Rect(215, 495, 70,45),5)
            solver = 3

        #Solution button
        if(x>=395 and x<=525 and y>= 395 and y<=440):
            if(not solvable()):
                pass
            elif(solver==1):
                playing = False
                solution = dfs_bfs.BFS(init_state)
                solverUI_init()
            elif(solver==2):
                playing = False
                solution = dfs_bfs.DFS(init_state)
                solverUI_init()
            elif(solver==3):
                playing = False
                solution = a_star.AStar(init_state)
                solverUI_init()
        
        #Open file button
        if(x>=20 and x<=125 and y>=20 and y<=65):
            #Tk requires an instance to use its utilities
            root = Tk()
            file = askopenfilename()
            if(file):
                read_input(file)
                render_mainscreen()
            
            root.destroy()            
        
    else:
        if(x>=355 and x <= 435 and y >=395 and y<=435):
            if(step<len(solution) and step<STEP_LIMIT):
                step_font = pygame.font.SysFont('Century Gothic', 20)
                solverStep(solution[step])
                screen.blit(step_font.render(solution[step],False,(0,0,0)), (270+(step%15)*15,475+(step//15)*15)) 
                step+=1
                if(step==len(solution)):
                    path_font = pygame.font.SysFont('Century Gothic', 40)
                    screen.blit(path_font.render("Path cost: "+ str(len(solution)),False,(0,0,0)), (270,20)) 
    #Render the screen
    pygame.display.flip()

#Renders the mainscreen
def render_mainscreen():
    
    global solver
    solver = 0
    game_font = pygame.font.SysFont('Century Gothic', 30)
    block_font = pygame.font.SysFont('Century Gothic', 50)
    #Display whether game is solvable or not
    if(solvable()):
        status_text = game_font.render('Puzzle is solvable',False,(0,0,0))
    else:
        status_text = game_font.render('Puzzle is not solvable',False,(0,0,0))
    
    #Initialize display
    screen.fill(WHITE)
    screen.blit(status_text, (275,20))
    


    #Initialize 8-puzzle blocks
    for i in range(0,len(game_state)):

        
        x_start = (i%3)*BLOCK_SIZE + PUZZLE_START_X
        y_start = (i//3)*BLOCK_SIZE + PUZZLE_START_Y
        if game_state[i] >0 :   
            pygame.draw.rect(screen, BLOCK_COLOR, pygame.Rect(x_start, y_start, BLOCK_SIZE-1,BLOCK_SIZE-1))
            screen.blit(block_font.render(str(game_state[i]),False,WHITE), (x_start+25,y_start+25))

    #Buttons for various solutions
    pygame.draw.rect(screen, DEFAULT_OUTLINE, pygame.Rect(215, 395, 70,45),5)
    screen.blit(game_font.render('BFS',False,(0,0,0)), (225,400))

    pygame.draw.rect(screen, DEFAULT_OUTLINE, pygame.Rect(215, 445, 70,45),5)
    screen.blit(game_font.render('DFS',False,(0,0,0)), (225,450))

    pygame.draw.rect(screen, DEFAULT_OUTLINE, pygame.Rect(215, 495, 70,45),5)
    screen.blit(game_font.render('A*',False,(0,0,0)), (225,500))    
    
    pygame.draw.rect(screen, BUTTON_COLOR, pygame.Rect(395, 395, 130,45))
    screen.blit(game_font.render('Solution',False, WHITE), (405,400))
    
    #Button for opening files
    pygame.draw.rect(screen, BUTTON_COLOR, pygame.Rect(20, 20, 105,45))
    screen.blit(game_font.render('Open',False, WHITE), (25,25))
    
    #Render screen
    pygame.display.flip()
#Main function
def main():

    #Change scope
    global screen

    #Initialize pygame
    pygame.init()

    #Initialize puzzle
    read_input("puzzle.in")

    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption('8 Puzzle Game')

    render_mainscreen()

    check_solved()
    
    running = True
    while running:
        #[1] Listens to screen event and does action
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                handle_click(pos)
            if event.type == pygame.QUIT:
                running = False
        #Set ticks to 0.2s to avoid possible performance issues
        time.sleep(0.2)
        

main()