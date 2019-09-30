

import pygame
from .. import setup
from .. import csts

class Flag(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(Flag, self).__init__()
        self.spr_sheet = setup.GFX['item_objects']
        self.setup_images()
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.y = y
        self.state = csts.TOP_OF_POLE


    def setup_images(self):

        self.frames = []

        self.frames.append(
            self.imageGetter(128, 32, 16, 16))


    def imageGetter(self, x, y, width, height):

        image = pygame.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.spr_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(csts.BLACK)
        image = pygame.transform.scale(image,
                                   (int(rect.width*csts.BRICK_SIZE_MULTIPLIER),
                                    int(rect.height*csts.BRICK_SIZE_MULTIPLIER)))
        return image


    def update(self, *args):

        self.standHandler()


    def standHandler(self):

        if self.state == csts.TOP_OF_POLE:
            self.image = self.frames[0]
        elif self.state == csts.SLIDE_DOWN:
            self.sliding_down()
        elif self.state == csts.BOTTOM_OF_POLE:
            self.image = self.frames[0]


    def sliding_down(self):

        self.y_vel = 5
        self.rect.y += self.y_vel

        if self.rect.bottom >= 485:
            self.state = csts.BOTTOM_OF_POLE


class Pole(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(Pole, self).__init__()
        self.spr_sheet = setup.GFX['tile_set']
        self.setup_frames()
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


    def setup_frames(self):

        self.frames = []

        self.frames.append(
            self.imageGetter(263, 144, 2, 16))


    def imageGetter(self, x, y, width, height):

        image = pygame.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.spr_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(csts.BLACK)
        image = pygame.transform.scale(image,
                                   (int(rect.width*csts.BRICK_SIZE_MULTIPLIER),
                                    int(rect.height*csts.BRICK_SIZE_MULTIPLIER)))
        return image


    def update(self, *args):

        pass


class Finial(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super(Finial, self).__init__()
        self.spr_sheet = setup.GFX['tile_set']
        self.setup_frames()
        self.image = self.frames[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y


    def setup_frames(self):

        self.frames = []

        self.frames.append(
            self.imageGetter(228, 120, 8, 8))


    def imageGetter(self, x, y, width, height):
    
        image = pygame.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.spr_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(csts.BLACK)
        image = pygame.transform.scale(image,
                                   (int(rect.width*csts.SIZE_MULTIPLIER),
                                    int(rect.height*csts.SIZE_MULTIPLIER)))
        return image


    def update(self, *args):
        pass
