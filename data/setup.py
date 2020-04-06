import os
import pygame
from . import tools
from .import gGameSettings

"""
This file simply sets up some basic os variables that vary depending on the individual's operating system/workstation setup.
"""
ORIGINAL_TITLE = gGameSettings.ORIGINAL_TITLE


os.environ['SDL_VIDEO_CENTECOLOR_RGB_RED'] = '1'
pygame.init()
pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT])
pygame.display.set_caption(gGameSettings.ORIGINAL_TITLE)
SCREEN = pygame.display.set_mode(gGameSettings.SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()


FONTS = tools.Fonts_LoadIntoRAM(os.path.join("resources","fonts"))
MUSIC = tools.Music_LoadIntoRAM(os.path.join("resources","music"))
GFX   = tools.Gfx_LoadIntoRAM(os.path.join("resources","graphics"))
SFX   = tools.Sfx_LoadIntoRAM(os.path.join("resources","sound"))
