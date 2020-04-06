

import pygame
from .. import setup
from .. import gGameSettings


class Coin(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(Coin, self).__init__()
        self.spr_sheet = setup.GFX['item_objects']
        self.create_frames()
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.timer = 0
        self.first_half = True
        self.frame_index = 0


    def create_frames(self):

        self.frames = []
        self.frame_index = 0

        self.frames.append(self.getImage(1, 160, 5, 8))
        self.frames.append(self.getImage(9, 160, 5, 8))
        self.frames.append(self.getImage(17, 160, 5, 8))


    def getImage(self, x, y, width, height):

        image = pygame.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.spr_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(gGameSettings.COLOR_RGB_BLACK)
        image = pygame.transform.scale(image,
                                   (int(rect.width*gGameSettings.BRICK_SIZE_MULTIPLIER),
                                    int(rect.height*gGameSettings.BRICK_SIZE_MULTIPLIER)))
        return image


    def update(self, current_time):
        if self.first_half:
            if self.frame_index == 0:
                if (current_time - self.timer) > 375:
                    self.frame_index += 1
                    self.timer = current_time
            elif self.frame_index < 2:
                if (current_time - self.timer) > 125:
                    self.frame_index += 1
                    self.timer = current_time
            elif self.frame_index == 2:
                if (current_time - self.timer) > 125:
                    self.frame_index -= 1
                    self.first_half = False
                    self.timer = current_time
        else:
            if self.frame_index == 1:
                if (current_time - self.timer) > 125:
                    self.frame_index -= 1
                    self.first_half = True
                    self.timer = current_time

        self.image = self.frames[self.frame_index]
