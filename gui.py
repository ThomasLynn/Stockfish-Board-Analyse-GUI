"""
    Original code from
    Ahira Justice, ADEFOKUN
    justiceahira@gmail.com
    From https://github.com/ahira-justice/chess-board
    
    Modified to customise the ui
"""


import os
import sys
import pygame
from pygame.locals import *
import numpy as np
import math

from chessboard import board


os.environ['SDL_VIDEO_CENTERED'] = '1' # Centre display window.

FPS = 30
FPSCLOCK = pygame.time.Clock()

DISPLAYSURF = None

gameboard = None
arrows = []
analysis_board = None

colors = {
    'Ash':  ( 50,  50,  50),
    'White':(255, 255, 255),
    'Black':(  0,   0,   0),
}

BGCOLOR = colors['Ash']

WINDOWWIDTH, WINDOWHEIGHT = 600, 600

BASICFONTSIZE = 30

should_terminate = False

pygame.font.init() # you have to call this at the start, 
                   # if you want to use this module.
myfont = pygame.font.SysFont('calibri', 20)
pygame.init()
DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
pygame.display.set_caption('Stockfish Board Anaylisis GUI')
offset = np.array([20,0])


def terminate():
    global should_terminate
    should_terminate = True

def quit_program():
    pygame.quit()


def checkForQuit():
    for event in pygame.event.get(QUIT): # get all the QUIT events
        terminate() #terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP): # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate() # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event) # put the other KEYUP event objects back
    
    return False


def run_ui(fen=''):
    global gameboard

    # Setting up the GUI window.

    checkForQuit()

    DISPLAYSURF.fill(BGCOLOR)
    gameboard = board.Board(colors, BGCOLOR, DISPLAYSURF)
    gameboard.displayBoard()

    if (fen):
        gameboard.updatePieces(fen)
    else:
        gameboard.drawPieces()
        
    draw_arrows()
    
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    
def update_moves(info):
    #print("info",info)
    moves = info.get('pv')
    
    if moves!=None:
    
        moves = info.get('pv')[:10]
        string = ""
        
        for i,j in enumerate(moves):
            string += analysis_board.san(j)
            analysis_board.push(j)
            if i<len(moves)-1:
                string += ", "
        for i in range(len(moves)):
            analysis_board.pop()
                
        #analysis_board.set_fen(fen)
        
        if info.get('multipv') == 1:
            print()
            
        print(info.get('multipv'),info.get('pv')[0],analysis_board.san(info.get('pv')[0]),info.get('score'), info.get('hashfull'),string)
        
        #print("test",info.get('pv'))
        
        to_add = [info.get('pv'),info.get('score')]
        if len(arrows)<info.get('multipv'):
            arrows.append(to_add)
        else:
            arrows[info.get('multipv')-1] = to_add
            
        #print("arrows",arrows)
        
def draw_arrows():
    text_pos = []
    for i, w in enumerate(reversed(arrows)):
        from_square = w[0][0].from_square
        from_position = board.Board.boardRect[7-from_square//8][from_square%8]
        to_square = w[0][0].to_square
        to_position = board.Board.boardRect[7-to_square//8][to_square%8]
        
        distance = math.sqrt((to_position[0]-from_position[0])**2 + (to_position[1]-from_position[1])**2)
        #print(from_position,to_position)
        
        arrow_drawing = np.array([(0, -50), (0, 50), (200, 50), (200, 150), (300, 0), (200, -150), (200, -50)], dtype = np.float)
        
        arrow_drawing[2:,0] += distance*6 - 300
        
        arrow_drawing = np.multiply(arrow_drawing, [1,0.5])
        
        #theta = np.radians(100)
        theta = np.arctan2(to_position[1]-from_position[1],to_position[0]-from_position[0])

        r = np.array(( (np.cos(theta), -np.sin(theta)),
                       (np.sin(theta),  np.cos(theta)) ))
        
        text_pos.append(to_position - r.dot(offset))
                       
        for i in range(len(arrow_drawing)):
            arrow_drawing[i] = r.dot(arrow_drawing[i])
            
        arrow_drawing = arrow_drawing/6

        for i in range(len(arrow_drawing)):
            arrow_drawing[i] += from_position
            arrow_drawing[i] += [25,25]
        
        arrows
        pygame.draw.polygon(DISPLAYSURF, (244, 197, 19), arrow_drawing)
        
    for i, w in enumerate(reversed(arrows)):
        #text = str(w[1].white()) # score from white's perspective
        text = str(w[1].relative)
        text_size = myfont.size(text)
        textsurface = myfont.render(text, False, (0, 0, 0))
        DISPLAYSURF.blit(textsurface,(text_pos[i][0]-text_size[0]/2+25,text_pos[i][1]-text_size[1]/2+25))

if __name__ == "__main__":
    while True:
        run_ui()
        if should_terminate:
            quit_program()
            break