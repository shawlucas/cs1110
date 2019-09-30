import pygame
from .. import setup
from .. import csts
from . import powerups
from . import coin



class Coin_box(pygame.sprite.Sprite):
    def __init__(self, x, y, contents='coin', group=None):
        pygame.sprite.Sprite.__init__(self)
        self.spr_sheet = setup.GFX['tile_set']
        self.frames = []
        self.setup_frames()
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_timer = 0
        self.first_half = True   # First half of animation cycle
        self.state = csts.RESTING
        self.rest_height = y
        self.gravity = 1.2
        self.y_vel = 0
        self.contents = contents
        self.group = group


    def imageGetter(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.spr_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(csts.BLACK)

        image = pygame.transform.scale(image,
                                   (int(rect.width*csts.BRICK_SIZE_MULTIPLIER),
                                    int(rect.height*csts.BRICK_SIZE_MULTIPLIER)))
        return image


    def setup_frames(self):
        self.frames.append(
            self.imageGetter(384, 0, 16, 16))
        self.frames.append(
            self.imageGetter(400, 0, 16, 16))
        self.frames.append(
            self.imageGetter(416, 0, 16, 16))
        self.frames.append(
            self.imageGetter(432, 0, 16, 16))


    def update(self, ginfo):
        self.current_time = ginfo[csts.CURRENT_TIME]
        self.standHandlers()


    def standHandlers(self):
        if self.state == csts.RESTING:
            self.resting()
        elif self.state == csts.BUMPED:
            self.bumped()
        elif self.state == csts.OPENED:
            self.opened()


    def resting(self):
        if self.first_half:
            if self.frame_index == 0:
                if (self.current_time - self.animation_timer) > 375:
                    self.frame_index += 1
                    self.animation_timer = self.current_time
            elif self.frame_index < 2:
                if (self.current_time - self.animation_timer) > 125:
                    self.frame_index += 1
                    self.animation_timer = self.current_time
            elif self.frame_index == 2:
                if (self.current_time - self.animation_timer) > 125:
                    self.frame_index -= 1
                    self.first_half = False
                    self.animation_timer = self.current_time
        else:
            if self.frame_index == 1:
                if (self.current_time - self.animation_timer) > 125:
                    self.frame_index -= 1
                    self.first_half = True
                    self.animation_timer = self.current_time

        self.image = self.frames[self.frame_index]


    def bumped(self):
        self.rect.y += self.y_vel
        self.y_vel += self.gravity

        if self.rect.y > self.rest_height + 5:
            self.rect.y = self.rest_height
            self.state = csts.OPENED
            if self.contents == 'mushroom':
                self.group.add(powerups.Mushroom(self.rect.centerx, self.rect.y))
            elif self.contents == 'fireflower':
                self.group.add(powerups.FireFlower(self.rect.centerx, self.rect.y))
            elif self.contents == '1up_mushroom':
                self.group.add(powerups.LifeMushroom(self.rect.centerx, self.rect.y))


        self.frame_index = 3
        self.image = self.frames[self.frame_index]


    def start_bump(self, score_group):
        self.y_vel = -6
        self.state = csts.BUMPED

        if self.contents == 'coin':
            self.group.add(coin.Coin(self.rect.centerx,
                                     self.rect.y,
                                     score_group))
            setup.SFX['coin'].play()
        else:
            setup.SFX['powerup_appears'].play()


    def opened(self):
        pass
