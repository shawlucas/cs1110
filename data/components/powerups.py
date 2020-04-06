import pygame
from .. import gGameSettings
from .. import setup


class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super(Powerup, self).__init__()


    def setup_powerup(self, x, y, name, setup_frames):
        self.spr_sheet = setup.GFX['item_objects']
        self.frames = []
        self.frame_index = 0
        setup_frames()
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.y = y
        self.state = gGameSettings.MUSHROOM_STATE_REVEAL
        self.y_vel = -1
        self.x_vel = 0
        self.direction = gGameSettings.GOOMBA_STATE_MOVING_RIGHT
        self.box_height = y
        self.gravity = 1
        self.max_y_vel = 8
        self.animate_timer = 0
        self.name = name


    def getImage(self, x, y, width, height):


        image = pygame.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.spr_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(gGameSettings.COLOR_RGB_BLACK)


        image = pygame.transform.scale(image,
                                   (int(rect.width*gGameSettings.SIZE_MULTIPLIER),
                                    int(rect.height*gGameSettings.SIZE_MULTIPLIER)))
        return image


    def update(self, gGameInfo, *args):

        self.current_time = gGameInfo[gGameSettings.GLOBAL_TIME]
        self.stateHandler()


    def stateHandler(self):
        pass


    def revealing(self, *args):

        self.rect.y += self.y_vel

        if self.rect.bottom <= self.box_height:
            self.rect.bottom = self.box_height
            self.y_vel = 0
            self.state = gGameSettings.MUSHROOM_STATE_SLIDING


    def sliding(self):

        if self.direction == gGameSettings.GOOMBA_STATE_MOVING_RIGHT:
            self.x_vel = 3
        else:
            self.x_vel = -3


    def falling(self):

        if self.y_vel < self.max_y_vel:
            self.y_vel += self.gravity


class Mushroom(Powerup):

    def __init__(self, x, y, name='mushroom'):
        super(Mushroom, self).__init__(x, y)
        self.setup_powerup(x, y, name, self.setup_frames)


    def setup_frames(self):

        self.frames.append(self.getImage(0, 0, 16, 16))


    def stateHandler(self):

        if self.state == gGameSettings.MUSHROOM_STATE_REVEAL:
            self.revealing()
        elif self.state == gGameSettings.MUSHROOM_STATE_SLIDING:
            self.sliding()
        elif self.state == gGameSettings.MARIO_STATE_FALL:
            self.falling()


class LifeMushroom(Mushroom):

    def __init__(self, x, y, name='1up_mushroom'):
        super(LifeMushroom, self).__init__(x, y)
        self.setup_powerup(x, y, name, self.setup_frames)

    def setup_frames(self):
        self.frames.append(self.getImage(16, 0, 16, 16))


class FireFlower(Powerup):

    def __init__(self, x, y, name=gGameSettings.BRICK_CONTENTS_FIREFLOWER):
        super(FireFlower, self).__init__(x, y)
        self.setup_powerup(x, y, name, self.setup_frames)


    def setup_frames(self):

        self.frames.append(
            self.getImage(0, 32, 16, 16))
        self.frames.append(
            self.getImage(16, 32, 16, 16))
        self.frames.append(
            self.getImage(32, 32, 16, 16))
        self.frames.append(
            self.getImage(48, 32, 16, 16))


    def stateHandler(self):

        if self.state == gGameSettings.MUSHROOM_STATE_REVEAL:
            self.revealing()
        elif self.state == gGameSettings.BRICK_STATE_RESTING:
            self.resting()


    def revealing(self):

        self.rect.y += self.y_vel

        if self.rect.bottom <= self.box_height:
            self.rect.bottom = self.box_height
            self.state = gGameSettings.BRICK_STATE_RESTING

        self.animation()


    def resting(self):

        self.animation()


    def animation(self):

        if (self.current_time - self.animate_timer) > 30:
            if self.frame_index < 3:
                self.frame_index += 1
            else:
                self.frame_index = 0

            self.image = self.frames[self.frame_index]
            self.animate_timer = self.current_time


class Star(Powerup):

    def __init__(self, x, y, name='star'):
        super(Star, self).__init__(x, y)
        self.setup_powerup(x, y, name, self.setup_frames)
        self.animate_timer = 0
        self.rect.y += 1  #looks more centeCOLOR_RGB_RED offset one pixel
        self.gravity = .4


    def setup_frames(self):

        self.frames.append(self.getImage(1, 48, 15, 16))
        self.frames.append(self.getImage(17, 48, 15, 16))
        self.frames.append(self.getImage(33, 48, 15, 16))
        self.frames.append(self.getImage(49, 48, 15, 16))


    def stateHandler(self):

        if self.state == gGameSettings.MUSHROOM_STATE_REVEAL:
            self.revealing()
        elif self.state == gGameSettings.STAR_STATE_BOUNCING:
            self.bouncing()


    def revealing(self):

        self.rect.y += self.y_vel

        if self.rect.bottom <= self.box_height:
            self.rect.bottom = self.box_height
            self.start_bounce(-2)
            self.state = gGameSettings.STAR_STATE_BOUNCING

        self.animation()


    def animation(self):

        if (self.current_time - self.animate_timer) > 30:
            if self.frame_index < 3:
                self.frame_index += 1
            else:
                self.frame_index = 0
            self.animate_timer = self.current_time
            self.image = self.frames[self.frame_index]


    def start_bounce(self, vel):

        self.y_vel = vel


    def bouncing(self):

        self.animation()

        if self.direction == gGameSettings.GOOMBA_STATE_MOVING_LEFT:
            self.x_vel = -5
        else:
            self.x_vel = 5



class FireBall(pygame.sprite.Sprite):

    def __init__(self, x, y, facing_right, name=gGameSettings.BRICK_CONTENTS_FIREBALL):
        super(FireBall, self).__init__()
        self.spr_sheet = setup.GFX['item_objects']
        self.setup_frames()
        if facing_right:
            self.direction = gGameSettings.GOOMBA_STATE_MOVING_RIGHT
            self.x_vel = 12
        else:
            self.direction = gGameSettings.GOOMBA_STATE_MOVING_LEFT
            self.x_vel = -12
        self.y_vel = 10
        self.gravity = .9
        self.frame_index = 0
        self.animation_timer = 0
        self.state = gGameSettings.FIRE_STATE_FLYING
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.right = x
        self.rect.y = y
        self.name = name


    def setup_frames(self):

        self.frames = []

        self.frames.append(
            self.getImage(96, 144, 8, 8)) #Frame 1 of flying
        self.frames.append(
            self.getImage(104, 144, 8, 8))  #Frame 2 of Flying
        self.frames.append(
            self.getImage(96, 152, 8, 8))   #Frame 3 of Flying
        self.frames.append(
            self.getImage(104, 152, 8, 8))  #Frame 4 of flying
        self.frames.append(
            self.getImage(112, 144, 16, 16))   #frame 1 of exploding
        self.frames.append(
            self.getImage(112, 160, 16, 16))  #frame 2 of exploding
        self.frames.append(
            self.getImage(112, 176, 16, 16))  #frame 3 of exploding


    def getImage(self, x, y, width, height):


        image = pygame.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.spr_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(gGameSettings.COLOR_RGB_BLACK)


        image = pygame.transform.scale(image,
                                   (int(rect.width*gGameSettings.SIZE_MULTIPLIER),
                                    int(rect.height*gGameSettings.SIZE_MULTIPLIER)))
        return image


    def update(self, gGameInfo, viewport):

        self.current_time = gGameInfo[gGameSettings.GLOBAL_TIME]
        self.stateHandler()
        self.check_if_off_screen(viewport)


    def stateHandler(self):

        if self.state == gGameSettings.FIRE_STATE_FLYING:
            self.animation()
        elif self.state == gGameSettings.FIRE_STATE_BOUNCING:
            self.animation()
        elif self.state == gGameSettings.FIRE_STATE_EXPLODING:
            self.animation()


    def animation(self):

        if self.state == gGameSettings.FIRE_STATE_FLYING or self.state == gGameSettings.FIRE_STATE_BOUNCING:
            if (self.current_time - self.animation_timer) > 200:
                if self.frame_index < 3:
                    self.frame_index += 1
                else:
                    self.frame_index = 0
                self.animation_timer = self.current_time
                self.image = self.frames[self.frame_index]


        elif self.state == gGameSettings.FIRE_STATE_EXPLODING:
            if (self.current_time - self.animation_timer) > 50:
                if self.frame_index < 6:
                    self.frame_index += 1
                    self.image = self.frames[self.frame_index]
                    self.animation_timer = self.current_time
                else:
                    self.kill()


    def explode_transition(self):

        self.frame_index = 4
        centerx = self.rect.centerx
        self.image = self.frames[self.frame_index]
        self.rect.centerx = centerx
        self.state = gGameSettings.FIRE_STATE_EXPLODING


    def check_if_off_screen(self, viewport):

        if (self.rect.x > viewport.right) or (self.rect.y > viewport.bottom) \
            or (self.rect.right < viewport.x):
            self.kill()
