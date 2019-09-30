import os
import pygame
from . import tools
from .import csts

ORIGINAL_TITLE = csts.ORIGINAL_TITLE


os.environ['SDL_VIDEO_CENTERED'] = '1'
pygame.init()
pygame.event.set_allowed([pygame.KEYDOWN, pygame.KEYUP, pygame.QUIT])
pygame.display.set_caption(csts.ORIGINAL_TITLE)
SCREEN = pygame.display.set_mode(csts.SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()


FONTS = tools.load_all_fonts(os.path.join("resources","fonts"))
MUSIC = tools.load_all_music(os.path.join("resources","music"))
GFX   = tools.load_all_gfx(os.path.join("resources","graphics"))
SFX   = tools.load_all_sfx(os.path.join("resources","sound"))
