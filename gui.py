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

from chessboard import board


os.environ['SDL_VIDEO_CENTERED'] = '1' # Centre display window.

FPS = 30
FPSCLOCK = pygame.time.Clock()

DISPLAYSURF = None

BASICFONT = None

gameboard = None

colors = {
    'Ash':  ( 50,  50,  50),
    'White':(255, 255, 255),
    'Black':(  0,   0,   0),
}

BGCOLOR = colors['Ash']

WINDOWWIDTH, WINDOWHEIGHT = 600, 600

BASICFONTSIZE = 30

should_terminate = False


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


def start(fen=''):
    global gameboard
    pygame.init()

    # Setting up the GUI window.
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Stockfish Board Anaylisis GUI')
    BASICFONT = pygame.font.SysFont('calibri', BASICFONTSIZE)

    checkForQuit()

    DISPLAYSURF.fill(BGCOLOR)
    gameboard = board.Board(colors, BGCOLOR, DISPLAYSURF)
    gameboard.displayBoard()

    if (fen):
        gameboard.updatePieces(fen)
    else:
        gameboard.drawPieces()
    
    pygame.display.update()
    FPSCLOCK.tick(FPS)

def update(fen=None):
    checkForQuit()
    gameboard.displayBoard()
    if fen is not None:
        gameboard.updatePieces(fen)

    pygame.display.update()
    FPSCLOCK.tick(FPS)

if __name__ == "__main__":
    while True:
        start()
        if should_terminate:
            quit_program()