import pygame
from .. import gGameSettings


class Checkpoint(pygame.sprite.Sprite):
    """
    This class handles the halfway checkpoint in the middle of the level.
    """
    def __init__(self, x, name, y=0, width=10, height=600):
        super(Checkpoint, self).__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(gGameSettings.COLOR_RGB_BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.name = name
