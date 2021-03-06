import pygame
from .. import setup
from .. import gGameSettings


class Flag(pygame.sprite.Sprite):
    """
    This class handles the flagpole and controls it's animation based on it's state.
    """
    def __init__(self, x, y):

        super(Flag, self).__init__()
        self.spr_sheet = setup.GFX['item_objects']
        self.image = self.getImage(129, 2, 14, 14)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.state = 'rising'
        self.y_vel = -2
        self.target_height = y


    def getImage(self, x, y, width, height):

        image = pygame.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.spr_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(gGameSettings.COLOR_RGB_BLACK)
        image = pygame.transform.scale(image,
                                   (int(rect.width*gGameSettings.SIZE_MULTIPLIER),
                                    int(rect.height*gGameSettings.SIZE_MULTIPLIER)))
        return image

    def update(self, *args):

        if self.state == 'rising':
            self.rising()
        elif self.state == 'resting':
            self.resting()

    def rising(self):

        self.rect.y += self.y_vel
        if self.rect.bottom <= self.target_height:
            self.state = 'resting'

    def resting(self):

        pass
