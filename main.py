"""
main.py
Initializes the main game.
Calls the main() function.
"""

import sys
import pygame
from data.main import main
import cProfile


if __name__=='__main__':
    main()
    pygame.quit()
    sys.exit()
