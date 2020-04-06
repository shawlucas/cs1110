import pygame
from .. import gGameSettings

class Collider(pygame.sprite.Sprite):
    """
    The collider class controls collisions of sprites and invisible sprites.
    Invisible sprites placed overtop background parts that can be collided with."""
    def __init__(self, x, y, width, height, name='collider'):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((width, height)).convert()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.state = None
