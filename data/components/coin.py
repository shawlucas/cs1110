import pygame
from .. import setup
from .. import gGameSettings
from . import score


class Coin(pygame.sprite.Sprite):
    """
    This class handles the animation cycle and game state of an individual Coin object.
    """
    def __init__(self, x, y, score_group):
        pygame.sprite.Sprite.__init__(self)
        self.spr_sheet = setup.GFX['item_objects']
        self.frames = []
        self.frame_index = 0
        self.animation_timer = 0
        self.state = gGameSettings.COIN_STATE_SPIN
        self.setup_frames()
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y - 5
        self.gravity = 1
        self.y_vel = -15
        self.initial_height = self.rect.bottom - 5
        self.score_group = score_group


    def getImage(self, x, y, width, height):

        image = pygame.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.spr_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(gGameSettings.COLOR_RGB_BLACK)


        image = pygame.transform.scale(image,
                                   (int(rect.width*gGameSettings.SIZE_MULTIPLIER),
                                    int(rect.height*gGameSettings.SIZE_MULTIPLIER)))
        return image


    def setup_frames(self):

        self.frames.append(self.getImage(52, 113, 8, 14))
        self.frames.append(self.getImage(4, 113, 8, 14))
        self.frames.append(self.getImage(20, 113, 8, 14))
        self.frames.append(self.getImage(36, 113, 8, 14))


    def update(self, gGameInfo, viewport):

        self.current_time = gGameInfo[gGameSettings.GLOBAL_TIME]
        self.viewport = viewport
        if self.state == gGameSettings.COIN_STATE_SPIN:
            self.spinning()


    def spinning(self):
        """
        This function handles the spinning animation of a Coin.
        """
        self.image = self.frames[self.frame_index]
        self.rect.y += self.y_vel
        self.y_vel += self.gravity

        if (self.current_time - self.animation_timer) > 80:
            if self.frame_index < 3:
                self.frame_index += 1
            else:
                self.frame_index = 0

            self.animation_timer = self.current_time

        if self.rect.bottom > self.initial_height:
            self.kill()
            self.score_group.append(score.Score(self.rect.centerx - self.viewport.x,
                                                self.rect.y,
                                                200))
