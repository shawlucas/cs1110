import pygame
from .. import setup
from .. import csts
from . import score


class Coin(pygame.sprite.Sprite):

    def __init__(self, x, y, score_group):
        pygame.sprite.Sprite.__init__(self)
        self.spr_sheet = setup.GFX['item_objects']
        self.frames = []
        self.frame_index = 0
        self.animation_timer = 0
        self.state = csts.SPIN
        self.setup_frames()
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y - 5
        self.gravity = 1
        self.y_vel = -15
        self.initial_height = self.rect.bottom - 5
        self.score_group = score_group


    def imageGetter(self, x, y, width, height):

        image = pygame.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.spr_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(csts.BLACK)


        image = pygame.transform.scale(image,
                                   (int(rect.width*csts.SIZE_MULTIPLIER),
                                    int(rect.height*csts.SIZE_MULTIPLIER)))
        return image


    def setup_frames(self):

        self.frames.append(self.imageGetter(52, 113, 8, 14))
        self.frames.append(self.imageGetter(4, 113, 8, 14))
        self.frames.append(self.imageGetter(20, 113, 8, 14))
        self.frames.append(self.imageGetter(36, 113, 8, 14))


    def update(self, ginfo, viewport):

        self.current_time = ginfo[csts.CURRENT_TIME]
        self.viewport = viewport
        if self.state == csts.SPIN:
            self.spinning()


    def spinning(self):

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
