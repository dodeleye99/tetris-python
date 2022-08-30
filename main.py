import os
import pygame
import constants
from game_controller import GameController

"""
This module is used as the entry point of the program.
"""

# Initialise all pygame modules
pygame.init()

# Centre the position of the program window, so  displayed at the centre of the computer screen.
os.environ['SDL_VIDEO_CENTERED'] = '1'

"""
Instantiate a GameController object, passing the screen size constants as arguments.
Immediately run the main loop after it is initialised.
"""
GameController(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT).main_loop()
