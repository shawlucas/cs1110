


import pygame
from .. import setup
from .. import gGameSettings


class Enemy(pygame.sprite.Sprite):
    """ 
    This class is a parent class that will encompass all enemies in the game.
    Attributes:
        x: initial x position
        y: initial y position
        direction: facing direction
        name: enemy name
        setup_frames: generic setup_frames function that are used in every enemy.
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)


    def enemySet(self, x, y, direction, name, setup_frames):
        self.spr_sheet = setup.GFX['smb_enemies_sheet']
        self.frames = []
        self.frame_index = 0
        self.animate_timer = 0
        self.death_timer = 0
        self.gravity = 1.5
        self.state = gGameSettings.MARIO_STATE_WALK

        self.name = name
        self.direction = direction
        setup_frames()

        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = y
        self.set_velocity()


    def set_velocity(self):
        if self.direction == gGameSettings.GOOMBA_STATE_MOVING_LEFT:
            self.x_vel = -2
        else:
            self.x_vel = 2

        self.y_vel = 0


    def getImage(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.spr_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(gGameSettings.COLOR_RGB_BLACK)


        image = pygame.transform.scale(image,
                                   (int(rect.width*gGameSettings.SIZE_MULTIPLIER),
                                    int(rect.height*gGameSettings.SIZE_MULTIPLIER)))
        return image


    def stateHandler(self):
        if self.state == gGameSettings.MARIO_STATE_WALK:
            self.walking()
        elif self.state == gGameSettings.MARIO_STATE_FALL:
            self.falling()
        elif self.state == gGameSettings.GOOMBA_STATE_JUMPED:
            self.jumped_on()
        elif self.state == gGameSettings.KOOPA_STATE_SLIDING_SHELL:
            self.shell_sliding()
        elif self.state == gGameSettings.GOOMBA_STATE_DEATH:
            self.death_jumping()


    def walking(self):
        """Default state of moving sideways"""
        if (self.current_time - self.animate_timer) > 125:
            if self.frame_index == 0:
                self.frame_index += 1
            elif self.frame_index == 1:
                self.frame_index = 0

            self.animate_timer = self.current_time


    def falling(self):
        """For when it falls off a ledge"""
        if self.y_vel < 10:
            self.y_vel += self.gravity


    def jumped_on(self):
        """Placeholder for when the enemy is stomped on"""
        pass


    def death_jumping(self):
        """Death animation"""
        self.rect.y += self.y_vel
        self.rect.x += self.x_vel
        self.y_vel += self.gravity

        if self.rect.y > 600:
            self.kill()


    def start_death_jump(self, direction):
        """Transitions enemy into a DEATH MARIO_STATE_JUMP state"""
        self.y_vel = -8
        if direction == gGameSettings.GOOMBA_STATE_MOVING_RIGHT:
            self.x_vel = 2
        else:
            self.x_vel = -2
        self.gravity = .5
        self.frame_index = 3
        self.image = self.frames[self.frame_index]
        self.state = gGameSettings.GOOMBA_STATE_DEATH


    def animation(self):
        """Basic animation, switching between two frames"""
        self.image = self.frames[self.frame_index]


    def update(self, gGameInfo, *args):
        """Updates enemy behavior"""
        self.current_time = gGameInfo[gGameSettings.GLOBAL_TIME]
        self.stateHandler()
        self.animation()




class Goomba(Enemy):
    """
    This class handles the "Goomba" enemy.
    """
    def __init__(self, y=gGameSettings.gr_height, x=0, direction=gGameSettings.GOOMBA_STATE_MOVING_LEFT, name='goomba'):
        Enemy.__init__(self)
        self.enemySet(x, y, direction, name, self.setup_frames)


    def setup_frames(self):
        """Put the image frames in a list to be animated"""

        self.frames.append(
            self.getImage(0, 4, 16, 16))
        self.frames.append(
            self.getImage(30, 4, 16, 16))
        self.frames.append(
            self.getImage(61, 0, 16, 16))
        self.frames.append(pygame.transform.flip(self.frames[1], False, True))


    def jumped_on(self):
        """When Mario squishes him"""
        self.frame_index = 2

        if (self.current_time - self.death_timer) > 500:
            self.kill()



class Koopa(Enemy):
    """
    This class handles the "Koopa" enemy.
    """
    
    def __init__(self, y=gGameSettings.gr_height, x=0, direction=gGameSettings.GOOMBA_STATE_MOVING_LEFT, name='koopa'):
        Enemy.__init__(self)
        self.enemySet(x, y, direction, name, self.setup_frames)


    def setup_frames(self):
        """Sets frame list"""
        self.frames.append(
            self.getImage(150, 0, 16, 24))
        self.frames.append(
            self.getImage(180, 0, 16, 24))
        self.frames.append(
            self.getImage(360, 5, 16, 15))
        self.frames.append(pygame.transform.flip(self.frames[2], False, True))


    def jumped_on(self):
        """When Mario jumps on the Koopa and puts him in his shell"""
        self.x_vel = 0
        self.frame_index = 2
        shell_y = self.rect.bottom
        shell_x = self.rect.x
        self.rect = self.frames[self.frame_index].get_rect()
        self.rect.x = shell_x
        self.rect.bottom = shell_y


    def shell_sliding(self):
        """When the koopa is sliding along the ground in his shell"""
        if self.direction == gGameSettings.GOOMBA_STATE_MOVING_RIGHT:
            self.x_vel = 10
        elif self.direction == gGameSettings.GOOMBA_STATE_MOVING_LEFT:
            self.x_vel = -10
