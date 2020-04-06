

import pygame
from .. import setup, tools
from .. import gGameSettings
from . import powerups


class Mario(pygame.sprite.Sprite):
    """
    This is a class to create an instance of the PLAYER, or MARIO.
    """
    def __init__(self):

        """
        The constructor for the Mario class.

        Sets the sprite sheet to 'mario_bros', which is in the resource folder. This sprite sheet contains all animation frames for Mario.
        """
        pygame.sprite.Sprite.__init__(self)
        self.spr_sheet = setup.GFX['mario_bros']

        self.timerSetup()
        self.setup_state_booleans()
        self.setup_forces()
        self.counterSetup()
        self.Gfx_LoadSpriteSheet()

        self.state = gGameSettings.MARIO_STATE_WALK
        self.image = self.right_frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)

        self.key_timer = 0


    def timerSetup(self):
        """
        This function sets all global timers to 0.
        """
        self.walking_timer = 0
        self.invincible_animation_timer = 0
        self.invincible_start_timer = 0
        self.fire_transition_timer = 0
        self.death_timer = 0
        self.transition_timer = 0
        self.last_fireball_time = 0
        self.hurt_invisible_timer = 0
        self.hurt_invisible_timer2 = 0
        self.flag_pole_timer = 0


    def setup_state_booleans(self):
        """
        This function sets all boolean values that Mario will have when he is spawned into the game.
        """
        self.facing_right = True # Mario is facing right at the start of the level
        self.allow_jump = True # He is allowed to jump
        self.dead = False # He is not dead
        self.invincible = False # He is not invincible
        self.big = False # He is small mario, as he has not gotten the magic mushroom yet.
        self.fire = False #He is not fire mario, as he has not gotten the fire flower yet.
        self.allow_fireball = True
        self.in_transition_state = False # He is not transitioning states
        self.hurt_invincible = False # He is not hurt
        self.in_castle = False # He is not in the castle
        self.crouching = False # He is not crouching
        self.losing_invincibility = False # He is not invinicble, so he cannot be in a state in which his invincibility is wearing off

    def setup_forces(self):
        """
        This function sets all forces that will be acting on Mario when he is spawned into the game. 
        """
        self.x_vel = 0
        self.y_vel = 0
        self.max_x_vel = gGameSettings.MARIO_MAX_WALK_SPEED
        self.max_y_vel = gGameSettings.MARIO_MAX_Y_VELOCITY
        self.x_accel = gGameSettings.MARIO_WALK_ACCELERATION
        self.jump_vel = gGameSettings.MARIO_JUMP_VELOCITY
        self.gravity = gGameSettings.WORLD_GRAVITY


    def counterSetup(self):
        """
        This function sets all of Mario's internal counters to zero, clearing any previous values that they may have had.
        """
        self.frame_index = 0
        self.invincible_index = 0
        self.fire_transition_index = 0
        self.fireball_count = 0
        self.flag_pole_right = 0


    def Gfx_LoadSpriteSheet(self):

        """
        This function loads sprite images needed for Mario's animation. It uses arrays for each set of animations, and uses the
        getImage function with parameters (x, y, width, height) to access coordinates of the sprite sheet to use as an animation frame.
        """
        self.right_frames = []
        self.left_frames = []

        self.right_small_normal_frames = []
        self.left_small_normal_frames = []
        self.right_small_green_frames = []
        self.left_small_green_frames = []
        self.right_small_COLOR_RGB_RED_frames = []
        self.left_small_COLOR_RGB_RED_frames = []
        self.right_small_black_frames = []
        self.left_small_black_frames = []

        self.right_big_normal_frames = []
        self.left_big_normal_frames = []
        self.right_big_green_frames = []
        self.left_big_green_frames = []
        self.right_big_COLOR_RGB_RED_frames = []
        self.left_big_COLOR_RGB_RED_frames = []
        self.right_big_black_frames = []
        self.left_big_black_frames = []

        self.right_fire_frames = []
        self.left_fire_frames = []


        # Images for normal small mario #

        self.right_small_normal_frames.append(
            self.getImage(178, 32, 12, 16))  # Right [0]
        self.right_small_normal_frames.append(
            self.getImage(80,  32, 15, 16))  # Right walking 1 [1]
        self.right_small_normal_frames.append(
            self.getImage(96,  32, 16, 16))  # Right walking 2 [2]
        self.right_small_normal_frames.append(
            self.getImage(112,  32, 16, 16))  # Right walking 3 [3]
        self.right_small_normal_frames.append(
            self.getImage(144, 32, 16, 16))  # Right jump [4]
        self.right_small_normal_frames.append(
            self.getImage(130, 32, 14, 16))  # Right skid [5]
        self.right_small_normal_frames.append(
            self.getImage(160, 32, 15, 16))  # Death frame [6]
        self.right_small_normal_frames.append(
            self.getImage(320, 8, 16, 24))  # Transition small to big [7]
        self.right_small_normal_frames.append(
            self.getImage(241, 33, 16, 16))  # Transition big to small [8]
        self.right_small_normal_frames.append(
            self.getImage(194, 32, 12, 16))  # Frame 1 of flag pole Slide [9]
        self.right_small_normal_frames.append(
            self.getImage(210, 33, 12, 16))  # Frame 2 of flag pole slide [10]


        #Images for small green mario (for invincible animation)#

        self.right_small_green_frames.append(
            self.getImage(178, 224, 12, 16))  # Right standing [0]
        self.right_small_green_frames.append(
            self.getImage(80, 224, 15, 16))  # Right walking 1 [1]
        self.right_small_green_frames.append(
            self.getImage(96, 224, 16, 16))  # Right walking 2 [2]
        self.right_small_green_frames.append(
            self.getImage(112, 224, 15, 16))  # Right walking 3 [3]
        self.right_small_green_frames.append(
            self.getImage(144, 224, 16, 16))  # Right jump [4]
        self.right_small_green_frames.append(
            self.getImage(130, 224, 14, 16))  # Right skid [5]

        #Images for red mario (for invincible animation) #

        self.right_small_COLOR_RGB_RED_frames.append(
            self.getImage(178, 272, 12, 16))  # Right standing [0]
        self.right_small_COLOR_RGB_RED_frames.append(
            self.getImage(80, 272, 15, 16))  # Right walking 1 [1]
        self.right_small_COLOR_RGB_RED_frames.append(
            self.getImage(96, 272, 16, 16))  # Right walking 2 [2]
        self.right_small_COLOR_RGB_RED_frames.append(
            self.getImage(112, 272, 15, 16))  # Right walking 3 [3]
        self.right_small_COLOR_RGB_RED_frames.append(
            self.getImage(144, 272, 16, 16))  # Right jump [4]
        self.right_small_COLOR_RGB_RED_frames.append(
            self.getImage(130, 272, 14, 16))  # Right skid [5]

        #Images for black mario (for invincible animation) #

        self.right_small_black_frames.append(
            self.getImage(178, 176, 12, 16))  # Right standing [0]
        self.right_small_black_frames.append(
            self.getImage(80, 176, 15, 16))  # Right walking 1 [1]
        self.right_small_black_frames.append(
            self.getImage(96, 176, 16, 16))  # Right walking 2 [2]
        self.right_small_black_frames.append(
            self.getImage(112, 176, 15, 16))  # Right walking 3 [3]
        self.right_small_black_frames.append(
            self.getImage(144, 176, 16, 16))  # Right jump [4]
        self.right_small_black_frames.append(
            self.getImage(130, 176, 14, 16))  # Right skid [5]


        # Images for normal big Mario #

        self.right_big_normal_frames.append(
            self.getImage(176, 0, 16, 32))  # Right standing [0]
        self.right_big_normal_frames.append(
            self.getImage(81, 0, 16, 32))  # Right walking 1 [1]
        self.right_big_normal_frames.append(
            self.getImage(97, 0, 15, 32))  # Right walking 2 [2]
        self.right_big_normal_frames.append(
            self.getImage(113, 0, 15, 32))  # Right walking 3 [3]
        self.right_big_normal_frames.append(
            self.getImage(144, 0, 16, 32))  # Right jump [4]
        self.right_big_normal_frames.append(
            self.getImage(128, 0, 16, 32))  # Right skid [5]
        self.right_big_normal_frames.append(
            self.getImage(336, 0, 16, 32))  # Right throwing [6]
        self.right_big_normal_frames.append(
            self.getImage(160, 10, 16, 22))  # Right crouching [7]
        self.right_big_normal_frames.append(
            self.getImage(272, 2, 16, 29))  # Transition big to small [8]
        self.right_big_normal_frames.append(
            self.getImage(193, 2, 16, 30))  # Frame 1 of flag pole slide [9]
        self.right_big_normal_frames.append(
            self.getImage(209, 2, 16, 29))  # Frame 2 of flag pole slide [10]

        # Images for green  big Mario #

        self.right_big_green_frames.append(
            self.getImage(176, 192, 16, 32))  # Right standing [0]
        self.right_big_green_frames.append(
            self.getImage(81, 192, 16, 32))  # Right walking 1 [1]
        self.right_big_green_frames.append(
            self.getImage(97, 192, 15, 32))  # Right walking 2 [2]
        self.right_big_green_frames.append(
            self.getImage(113, 192, 15, 32))  # Right walking 3 [3]
        self.right_big_green_frames.append(
            self.getImage(144, 192, 16, 32))  # Right jump [4]
        self.right_big_green_frames.append(
            self.getImage(128, 192, 16, 32))  # Right skid [5]
        self.right_big_green_frames.append(
            self.getImage(336, 192, 16, 32))  # Right throwing [6]
        self.right_big_green_frames.append(
            self.getImage(160, 202, 16, 22))  # Right Crouching [7]

        # Images for red big Mario #

        self.right_big_COLOR_RGB_RED_frames.append(
            self.getImage(176, 240, 16, 32))  # Right standing [0]
        self.right_big_COLOR_RGB_RED_frames.append(
            self.getImage(81, 240, 16, 32))  # Right walking 1 [1]
        self.right_big_COLOR_RGB_RED_frames.append(
            self.getImage(97, 240, 15, 32))  # Right walking 2 [2]
        self.right_big_COLOR_RGB_RED_frames.append(
            self.getImage(113, 240, 15, 32))  # Right walking 3 [3]
        self.right_big_COLOR_RGB_RED_frames.append(
            self.getImage(144, 240, 16, 32))  # Right jump [4]
        self.right_big_COLOR_RGB_RED_frames.append(
            self.getImage(128, 240, 16, 32))  # Right skid [5]
        self.right_big_COLOR_RGB_RED_frames.append(
            self.getImage(336, 240, 16, 32))  # Right throwing [6]
        self.right_big_COLOR_RGB_RED_frames.append(
            self.getImage(160, 250, 16, 22))  # Right crouching [7]

        # Images for black big Mario #

        self.right_big_black_frames.append(
            self.getImage(176, 144, 16, 32))  # Right standing [0]
        self.right_big_black_frames.append(
            self.getImage(81, 144, 16, 32))  # Right walking 1 [1]
        self.right_big_black_frames.append(
            self.getImage(97, 144, 15, 32))  # Right walking 2 [2]
        self.right_big_black_frames.append(
            self.getImage(113, 144, 15, 32))  # Right walking 3 [3]
        self.right_big_black_frames.append(
            self.getImage(144, 144, 16, 32))  # Right jump [4]
        self.right_big_black_frames.append(
            self.getImage(128, 144, 16, 32))  # Right skid [5]
        self.right_big_black_frames.append(
            self.getImage(336, 144, 16, 32))  # Right throwing [6]
        self.right_big_black_frames.append(
            self.getImage(160, 154, 16, 22))  # Right Crouching [7]


        # Images for Fire Mario #

        self.right_fire_frames.append(
            self.getImage(176, 48, 16, 32))  # Right standing [0]
        self.right_fire_frames.append(
            self.getImage(81, 48, 16, 32))  # Right walking 1 [1]
        self.right_fire_frames.append(
            self.getImage(97, 48, 15, 32))  # Right walking 2 [2]
        self.right_fire_frames.append(
            self.getImage(113, 48, 15, 32))  # Right walking 3 [3]
        self.right_fire_frames.append(
            self.getImage(144, 48, 16, 32))  # Right jump [4]
        self.right_fire_frames.append(
            self.getImage(128, 48, 16, 32))  # Right skid [5]
        self.right_fire_frames.append(
            self.getImage(336, 48, 16, 32))  # Right throwing [6]
        self.right_fire_frames.append(
            self.getImage(160, 58, 16, 22))  # Right crouching [7]
        self.right_fire_frames.append(
            self.getImage(0, 0, 0, 0))  # Place holder [8]
        self.right_fire_frames.append(
            self.getImage(193, 50, 16, 29))  # Frame 1 of flag pole slide [9]
        self.right_fire_frames.append(
            self.getImage(209, 50, 16, 29))  # Frame 2 of flag pole slide [10]


        # The left image frames are numbered the same as the right frames but are simply reversed. #

        for frame in self.right_small_normal_frames:
            new_image = pygame.transform.flip(frame, True, False)
            self.left_small_normal_frames.append(new_image)

        for frame in self.right_small_green_frames:
            new_image = pygame.transform.flip(frame, True, False)
            self.left_small_green_frames.append(new_image)

        for frame in self.right_small_COLOR_RGB_RED_frames:
            new_image = pygame.transform.flip(frame, True, False)
            self.left_small_COLOR_RGB_RED_frames.append(new_image)

        for frame in self.right_small_black_frames:
            new_image = pygame.transform.flip(frame, True, False)
            self.left_small_black_frames.append(new_image)

        for frame in self.right_big_normal_frames:
            new_image = pygame.transform.flip(frame, True, False)
            self.left_big_normal_frames.append(new_image)

        for frame in self.right_big_green_frames:
            new_image = pygame.transform.flip(frame, True, False)
            self.left_big_green_frames.append(new_image)

        for frame in self.right_big_COLOR_RGB_RED_frames:
            new_image = pygame.transform.flip(frame, True, False)
            self.left_big_COLOR_RGB_RED_frames.append(new_image)

        for frame in self.right_big_black_frames:
            new_image = pygame.transform.flip(frame, True, False)
            self.left_big_black_frames.append(new_image)

        for frame in self.right_fire_frames:
            new_image = pygame.transform.flip(frame, True, False)
            self.left_fire_frames.append(new_image)


        self.normal_small_frames = [self.right_small_normal_frames,
                              self.left_small_normal_frames]

        self.green_small_frames = [self.right_small_green_frames,
                             self.left_small_green_frames]

        self.red_small_frames = [self.right_small_COLOR_RGB_RED_frames,
                           self.left_small_COLOR_RGB_RED_frames]

        self.black_small_frames = [self.right_small_black_frames,
                             self.left_small_black_frames]

        self.invincible_small_frames_list = [self.normal_small_frames,
                                          self.green_small_frames,
                                          self.red_small_frames,
                                          self.black_small_frames]

        self.normal_big_frames = [self.right_big_normal_frames,
                                  self.left_big_normal_frames]

        self.green_big_frames = [self.right_big_green_frames,
                                 self.left_big_green_frames]

        self.red_big_frames = [self.right_big_COLOR_RGB_RED_frames,
                               self.left_big_COLOR_RGB_RED_frames]

        self.black_big_frames = [self.right_big_black_frames,
                                 self.left_big_black_frames]

        self.fire_frames = [self.right_fire_frames,
                            self.left_fire_frames]

        self.invincible_big_frames_list = [self.normal_big_frames,
                                           self.green_big_frames,
                                           self.red_big_frames,
                                           self.black_big_frames]

        self.all_images = [self.right_big_normal_frames,
                           self.right_big_black_frames,
                           self.right_big_COLOR_RGB_RED_frames,
                           self.right_big_green_frames,
                           self.right_small_normal_frames,
                           self.right_small_green_frames,
                           self.right_small_COLOR_RGB_RED_frames,
                           self.right_small_black_frames,
                           self.left_big_normal_frames,
                           self.left_big_black_frames,
                           self.left_big_COLOR_RGB_RED_frames,
                           self.left_big_green_frames,
                           self.left_small_normal_frames,
                           self.left_small_COLOR_RGB_RED_frames,
                           self.left_small_green_frames,
                           self.left_small_black_frames]


        self.right_frames = self.normal_small_frames[0]
        self.left_frames = self.normal_small_frames[1]


    def getImage(self, x, y, width, height):
        """
        This functiion gets the surface, and then copies the spritesheet using the parameters given in order to return the correct
        sprite for Mario's animation.

        Parameters:
            x (int): X coordinate of sprite in sheet
            y (int): Y coordinate of sprite in sheet
            width (int): Width of sprite in sheet
            height (int): Height of sprite in sheet
        
        Returns:
            Returns the image
        """
        image = pygame.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.spr_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(gGameSettings.COLOR_RGB_BLACK)
        image = pygame.transform.scale(image,
                                   (int(rect.width*gGameSettings.SIZE_MULTIPLIER),
                                    int(rect.height*gGameSettings.SIZE_MULTIPLIER)))
        return image


    def update(self, keys, gGameInfo, fire_group):
        """
        This function updates Mario's animation every frame

        Parameters:
            keys: Dictionary key for Mario's state
            gGameInfo: Global game info
            fire_group: Check for fire mario.
            
        """
        self.current_time = gGameInfo[gGameSettings.GLOBAL_TIME]
        self.stateHandler(keys, fire_group)
        self.Mario_StateCheckSpecial()
        self.Mario_SetAnimationImage()


    def stateHandler(self, keys, fire_group):

        """
        This function handles Mario's states depending on what he is doing at a particular moment.

        Parameters:
            keys: Dictionary key for Mario's state
            gGameInfo: Global game info
            fire_group: Check for fire mario.
        """
        if self.state == gGameSettings.MARIO_STATE_STANDING:
            self.Mario_Standing(keys, fire_group)
        elif self.state == gGameSettings.MARIO_STATE_WALK:
            self.Mario_Walking(keys, fire_group)
        elif self.state == gGameSettings.MARIO_STATE_JUMP:
            self.Mario_Jumping(keys, fire_group)
        elif self.state == gGameSettings.MARIO_STATE_FALL:
            self.Mario_Falling(keys, fire_group)
        elif self.state == gGameSettings.GOOMBA_STATE_DEATH:
            self.Mario_JumpToDeath()
        elif self.state == gGameSettings.MARIO_STATE_SMALL_TO_BIG:
            self.Mario_ChangingToBig()
        elif self.state == gGameSettings.MARIO_STATE_BIG_TO_FIRE:
            self.Mario_ChangeToFire()
        elif self.state == gGameSettings.MARIO_STATE_BIG_TO_SMALL:
            self.Mario_ChangingToSmall()
        elif self.state == gGameSettings.MARIO_STATE_ON_FLAGPOLE:
            self.Mario_PoleSlide()
        elif self.state == gGameSettings.FLAGSTATE_BOTTOM_OF_POLE:
            self.Mario_BottomOfPole()
        elif self.state == gGameSettings.MARIO_STATE_WALKING_TO_CASTLE:
            self.Mario_WalkingToCastle()
        elif self.state == gGameSettings.MARIO_STATE_END_OF_LEVEL:
            self.Mario_FallAtEnd()


    def Mario_Standing(self, keys, fire_group):
        """
        This function handles Mario's "Standing" state

        Parameters:
            keys: Dictionary key for Mario's state
            fire_group: Check for fire mario
        """
        self.Mario_JumpCheck(keys)
        self.Mario_FireballCheck(keys)

        self.frame_index = 0
        self.x_vel = 0
        self.y_vel = 0

        if keys[tools.keybinding['action']]:
            if self.fire and self.allow_fireball:
                self.Mario_ShootFireball(fire_group)

        if keys[tools.keybinding['down']]:
            self.crouching = True

        if keys[tools.keybinding['left']]:
            self.facing_right = False
            self.Mario_ExitCrouch()
            self.state = gGameSettings.MARIO_STATE_WALK
        elif keys[tools.keybinding['right']]:
            self.facing_right = True
            self.Mario_ExitCrouch()
            self.state = gGameSettings.MARIO_STATE_WALK
        elif keys[tools.keybinding['jump']]:
            if self.allow_jump:
                if self.big:
                    setup.SFX['big_jump'].play()
                else:
                    setup.SFX['small_jump'].play()
                self.state = gGameSettings.MARIO_STATE_JUMP
                self.y_vel = gGameSettings.MARIO_JUMP_VELOCITY
        else:
            self.state = gGameSettings.MARIO_STATE_STANDING

        if not keys[tools.keybinding['down']]:
            self.Mario_ExitCrouch()


    def Mario_ExitCrouch(self):
        """
        This function changes Mario's collision box from crouch to leaving crouch.
        """
        bottom = self.rect.bottom
        left = self.rect.x
        if self.facing_right:
            self.image = self.right_frames[0]
        else:
            self.image = self.left_frames[0]
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.x = left
        self.crouching = False


    def Mario_JumpCheck(self, keys):
        """
        This function checks if Mario is allowed to jump. It prevents double jumps.

        Parameters:
            keys: Dictionary key for Mario's state.
        """
        if not keys[tools.keybinding['jump']]:
            self.allow_jump = True


    def Mario_FireballCheck(self, keys):
        """
        This function checks if Mario is allowed to use a fireball.

        Parameters:
            keys: Dictionary key for Mario's state.
        
        """
        if not keys[tools.keybinding['action']]:
            self.allow_fireball = True


    def Mario_ShootFireball(self, powerups):
        """
        This function shoots a fireball from Mario's hand.
        
        Parameters:
            powerups: Empty array that will be filled with fireball powerups. Used to prevent too many from being loaded on screen at once.
        """
        setup.SFX['fireball'].play()
        self.fireball_count = self.Mario_FireballCount(powerups)

        if (self.current_time - self.last_fireball_time) > 200:
            if self.fireball_count < 2:
                self.allow_fireball = False
                powerups.add(
                    powerups.FireBall(self.rect.right, self.rect.y, self.facing_right))
                self.last_fireball_time = self.current_time

                self.frame_index = 6
                if self.facing_right:
                    self.image = self.right_frames[self.frame_index]
                else:
                    self.image = self.left_frames[self.frame_index]


    def Mario_FireballCount(self, powerups):
        """
        This function counts the number of fireballs in the fireball array at a time.

        Parameters:
            powerups: Array of fireball powerups. Used to prevent too many fireballs from being loaded on screen at once.
        
        Returns:
            Length of fireball_list
        """
        fireball_list = []

        for powerup in powerups:
            if powerup.name == gGameSettings.BRICK_CONTENTS_FIREBALL:
                fireball_list.append(powerup)

        return len(fireball_list)


    def Mario_Walking(self, keys, fire_group):
        """
        This function handles Mario's "Walking" state.

        Parameters:
            keys: Dictionary key for Mario's state.
            fire_group: Check for fire mario.
        """
        self.Mario_JumpCheck(keys)
        self.Mario_FireballCheck(keys)

        if self.frame_index == 0:
            self.frame_index += 1
            self.walking_timer = self.current_time
        else:
            if (self.current_time - self.walking_timer >
                    self.Mario_Math_CalcAnimationSpeed()):
                if self.frame_index < 3:
                    self.frame_index += 1
                else:
                    self.frame_index = 1

                self.walking_timer = self.current_time

        if keys[tools.keybinding['action']]:
            self.max_x_vel = gGameSettings.MARIO_MAX_RUN_SPEED
            self.x_accel = gGameSettings.MARIO_RUN_ACCELERATION
            if self.fire and self.allow_fireball:
                self.Mario_ShootFireball(fire_group)
        else:
            self.max_x_vel = gGameSettings.MARIO_MAX_WALK_SPEED
            self.x_accel = gGameSettings.MARIO_WALK_ACCELERATION

        if keys[tools.keybinding['jump']]:
            if self.allow_jump:
                if self.big:
                    setup.SFX['big_jump'].play()
                else:
                    setup.SFX['small_jump'].play()
                self.state = gGameSettings.MARIO_STATE_JUMP
                if self.x_vel > 4.5 or self.x_vel < -4.5:
                    self.y_vel = gGameSettings.MARIO_JUMP_VELOCITY - .5
                else:
                    self.y_vel = gGameSettings.MARIO_JUMP_VELOCITY


        if keys[tools.keybinding['left']]:
            self.Mario_ExitCrouch()
            self.facing_right = False
            if self.x_vel > 0:
                self.frame_index = 5
                self.x_accel = gGameSettings.MARIO_SMALL_TURNAROUND_SPEED
            else:
                self.x_accel = gGameSettings.MARIO_WALK_ACCELERATION

            if self.x_vel > (self.max_x_vel * -1):
                self.x_vel -= self.x_accel
                if self.x_vel > -0.5:
                    self.x_vel = -0.5
            elif self.x_vel < (self.max_x_vel * -1):
                self.x_vel += self.x_accel

        elif keys[tools.keybinding['right']]:
            self.Mario_ExitCrouch()
            self.facing_right = True
            if self.x_vel < 0:
                self.frame_index = 5
                self.x_accel = gGameSettings.MARIO_SMALL_TURNAROUND_SPEED
            else:
                self.x_accel = gGameSettings.MARIO_WALK_ACCELERATION

            if self.x_vel < self.max_x_vel:
                self.x_vel += self.x_accel
                if self.x_vel < 0.5:
                    self.x_vel = 0.5
            elif self.x_vel > self.max_x_vel:
                self.x_vel -= self.x_accel

        else:
            if self.facing_right:
                if self.x_vel > 0:
                    self.x_vel -= self.x_accel
                else:
                    self.x_vel = 0
                    self.state = gGameSettings.MARIO_STATE_STANDING
            else:
                if self.x_vel < 0:
                    self.x_vel += self.x_accel
                else:
                    self.x_vel = 0
                    self.state = gGameSettings.MARIO_STATE_STANDING


    def Mario_Math_CalcAnimationSpeed(self):
        """
        Calculates Mario's current Animation Speed

        Returns:
            animation_speed: current animation speed
        """
        if self.x_vel == 0:
            animation_speed = 130
        elif self.x_vel > 0:
            animation_speed = 130 - (self.x_vel * (13))
        else:
            animation_speed = 130 - (self.x_vel * (13) * -1)

        return animation_speed


    def Mario_Jumping(self, keys, fire_group):
        """
        This function handles Mario's jumping state.

        Parameters:
            keys: Dictionary key for Mario's state.
            fire_group: Check for fire mario.
        """
        self.allow_jump = False
        self.frame_index = 4
        self.gravity = gGameSettings.MARIO_JUMP_GRAVITY
        self.y_vel += self.gravity
        self.Mario_FireballCheck(keys)

        if self.y_vel >= 0 and self.y_vel < self.max_y_vel:
            self.gravity = gGameSettings.WORLD_GRAVITY
            self.state = gGameSettings.MARIO_STATE_FALL

        if keys[tools.keybinding['left']]:
            if self.x_vel > (self.max_x_vel * - 1):
                self.x_vel -= self.x_accel

        elif keys[tools.keybinding['right']]:
            if self.x_vel < self.max_x_vel:
                self.x_vel += self.x_accel

        if not keys[tools.keybinding['jump']]:
            self.gravity = gGameSettings.WORLD_GRAVITY
            self.state = gGameSettings.MARIO_STATE_FALL

        if keys[tools.keybinding['action']]:
            if self.fire and self.allow_fireball:
                self.Mario_ShootFireball(fire_group)


    def Mario_Falling(self, keys, fire_group):
        """
        This function handles Mario's falling state.

        Parameters:
            keys: Dictionary key for Mario's state.
            fire_group: Check for fire mario.
        """
        self.Mario_FireballCheck(keys)
        if self.y_vel < gGameSettings.MARIO_MAX_Y_VELOCITY:
            self.y_vel += self.gravity

        if keys[tools.keybinding['left']]:
            if self.x_vel > (self.max_x_vel * - 1):
                self.x_vel -= self.x_accel

        elif keys[tools.keybinding['right']]:
            if self.x_vel < self.max_x_vel:
                self.x_vel += self.x_accel

        if keys[tools.keybinding['action']]:
            if self.fire and self.allow_fireball:
                self.Mario_ShootFireball(fire_group)


    def Mario_JumpToDeath(self):
        """
        This function handles Mario's death jump state.
        """
        if self.death_timer == 0:
            self.death_timer = self.current_time
        elif (self.current_time - self.death_timer) > 500:
            self.rect.y += self.y_vel
            self.y_vel += self.gravity


    def InitializeDeathJump(self, gGameInfo):
        """
        This function sets Mario's velocity and initial parameters for his state when jumping down a bottomless pit.

        Parameters:
            gGameInfo: Global game variables
        """
        self.dead = True
        gGameInfo[gGameSettings.MARIO_STATE_DEAD] = True
        self.y_vel = -11
        self.gravity = .5
        self.frame_index = 6
        self.image = self.right_frames[self.frame_index]
        self.state = gGameSettings.GOOMBA_STATE_DEATH
        self.in_transition_state = True


    def Mario_ChangingToBig(self):
        """
        This function handles Mario's animation and transition when transitioning to big Mario after eating a mushroom.
        """
        self.in_transition_state = True

        if self.transition_timer == 0:
            self.transition_timer = self.current_time
        elif self.Math_Time_Diff(135, 200):
            self.Mario_SetMiddleTransitionAnimation()
        elif self.Math_Time_Diff(200, 365):
            self.Mario_SetSmallTransitionAnimation()
        elif self.Math_Time_Diff(365, 430):
            self.Mario_SetMiddleTransitionAnimation()
        elif self.Math_Time_Diff(430, 495):
            self.Mario_SetSmallTransitionAnimation()
        elif self.Math_Time_Diff(495, 560):
            self.Mario_SetMiddleTransitionAnimation()
        elif self.Math_Time_Diff(560, 625):
            self.Mario_SetBigTransitionAnimation()
        elif self.Math_Time_Diff(625, 690):
            self.Mario_SetSmallTransitionAnimation()
        elif self.Math_Time_Diff(690, 755):
            self.Mario_SetMiddleTransitionAnimation()
        elif self.Math_Time_Diff(755, 820):
            self.Mario_SetBigTransitionAnimation()
        elif self.Math_Time_Diff(820, 885):
            self.Mario_SetSmallTransitionAnimation()
        elif self.Math_Time_Diff(885, 950):
            self.Mario_SetBigTransitionAnimation()
            self.state = gGameSettings.MARIO_STATE_WALK
            self.in_transition_state = False
            self.transition_timer = 0
            self.Mario_ChangeToBig()


    def Math_Time_Diff(self, start_time, end_time):
        """
        This function returns the difference between two transition times.

        Returns:
            True if (self.current_time - self.transition_timer) >= start_time and (self.current_time - self.transition_timer) < end_time
        """
        if (self.current_time - self.transition_timer) >= start_time\
            and (self.current_time - self.transition_timer) < end_time:
            return True


    def Mario_SetMiddleTransitionAnimation(self):
        """
        Sets Mario's animation image to the middle image during a transition.
        """
        if self.facing_right:
            self.image = self.normal_small_frames[0][7]
        else:
            self.image = self.normal_small_frames[1][7]
        bottom = self.rect.bottom
        centerx = self.rect.centerx
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.centerx = centerx


    def Mario_SetSmallTransitionAnimation(self):
        """
        Sets Mario's animation image to the small image during a transition.
        """
        if self.facing_right:
            self.image = self.normal_small_frames[0][0]
        else:
            self.image = self.normal_small_frames[1][0]
        bottom = self.rect.bottom
        centerx = self.rect.centerx
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.centerx = centerx


    def Mario_SetBigTransitionAnimation(self):
        """
        Sets Mario's animation image to the big image during a transition
        """
        if self.facing_right:
            self.image = self.normal_big_frames[0][0]
        else:
            self.image = self.normal_big_frames[1][0]
        bottom = self.rect.bottom
        centerx = self.rect.centerx
        self.rect = self.image.get_rect()
        self.rect.bottom = bottom
        self.rect.centerx = centerx


    def Mario_ChangeToBig(self):
        """
        This function handles the transition period between when Mario is small to when he changes to big. 
        """
        self.big = True
        self.right_frames = self.right_big_normal_frames
        self.left_frames = self.left_big_normal_frames
        bottom = self.rect.bottom
        left = self.rect.x
        image = self.right_frames[0]
        self.rect = image.get_rect()
        self.rect.bottom = bottom
        self.rect.x = left


    def Mario_ChangeToFire(self):
        """
        This function handles the transition period when Mario is big and changing to fire flower Mario.
        """
        self.in_transition_state = True

        if self.facing_right:
            frames = [self.right_fire_frames[3],
                      self.right_big_green_frames[3],
                      self.right_big_COLOR_RGB_RED_frames[3],
                      self.right_big_black_frames[3]]
        else:
            frames = [self.left_fire_frames[3],
                      self.left_big_green_frames[3],
                      self.left_big_COLOR_RGB_RED_frames[3],
                      self.left_big_black_frames[3]]

        if self.fire_transition_timer == 0:
            self.fire_transition_timer = self.current_time
        elif (self.current_time - self.fire_transition_timer) > 65 and (self.current_time - self.fire_transition_timer) < 130:
            self.image = frames[0]
        elif (self.current_time - self.fire_transition_timer) < 195:
            self.image = frames[1]
        elif (self.current_time - self.fire_transition_timer) < 260:
            self.image = frames[2]
        elif (self.current_time - self.fire_transition_timer) < 325:
            self.image = frames[3]
        elif (self.current_time - self.fire_transition_timer) < 390:
            self.image = frames[0]
        elif (self.current_time - self.fire_transition_timer) < 455:
            self.image = frames[1]
        elif (self.current_time - self.fire_transition_timer) < 520:
            self.image = frames[2]
        elif (self.current_time - self.fire_transition_timer) < 585:
            self.image = frames[3]
        elif (self.current_time - self.fire_transition_timer) < 650:
            self.image = frames[0]
        elif (self.current_time - self.fire_transition_timer) < 715:
            self.image = frames[1]
        elif (self.current_time - self.fire_transition_timer) < 780:
            self.image = frames[2]
        elif (self.current_time - self.fire_transition_timer) < 845:
            self.image = frames[3]
        elif (self.current_time - self.fire_transition_timer) < 910:
            self.image = frames[0]
        elif (self.current_time - self.fire_transition_timer) < 975:
            self.image = frames[1]
        elif (self.current_time - self.fire_transition_timer) < 1040:
            self.image = frames[2]
            self.fire = True
            self.in_transition_state = False
            self.state = gGameSettings.MARIO_STATE_WALK
            self.transition_timer = 0


    def Mario_ChangingToSmall(self):
        """
        This function handles Mario's animation and transition when transitioning to small Mario after getting hit by an enemy or dying.
        """
        self.in_transition_state = True
        self.hurt_invincible = True
        self.state = gGameSettings.MARIO_STATE_BIG_TO_SMALL

        if self.facing_right:
            frames = [self.right_big_normal_frames[4],
                      self.right_big_normal_frames[8],
                      self.right_small_normal_frames[8]
                      ]
        else:
            frames = [self.left_big_normal_frames[4],
                      self.left_big_normal_frames[8],
                      self.left_small_normal_frames[8]
                     ]

        if self.transition_timer == 0:
            self.transition_timer = self.current_time
        elif (self.current_time - self.transition_timer) < 265:
            self.image = frames[0]
            self.Mario_SetInvincibility()
            self.Mario_AdjustCollision()
        elif (self.current_time - self.transition_timer) < 330:
            self.image = frames[1]
            self.Mario_SetInvincibility()
            self.Mario_AdjustCollision()
        elif (self.current_time - self.transition_timer) < 395:
            self.image = frames[2]
            self.Mario_SetInvincibility()
            self.Mario_AdjustCollision()
        elif (self.current_time - self.transition_timer) < 460:
            self.image = frames[1]
            self.Mario_SetInvincibility()
            self.Mario_AdjustCollision()
        elif (self.current_time - self.transition_timer) < 525:
            self.image = frames[2]
            self.Mario_SetInvincibility()
            self.Mario_AdjustCollision()
        elif (self.current_time - self.transition_timer) < 590:
            self.image = frames[1]
            self.Mario_SetInvincibility()
            self.Mario_AdjustCollision()
        elif (self.current_time - self.transition_timer) < 655:
            self.image = frames[2]
            self.Mario_SetInvincibility()
            self.Mario_AdjustCollision()
        elif (self.current_time - self.transition_timer) < 720:
            self.image = frames[1]
            self.Mario_SetInvincibility()
            self.Mario_AdjustCollision()
        elif (self.current_time - self.transition_timer) < 785:
            self.image = frames[2]
            self.Mario_SetInvincibility()
            self.Mario_AdjustCollision()
        elif (self.current_time - self.transition_timer) < 850:
            self.image = frames[1]
            self.Mario_SetInvincibility()
            self.Mario_AdjustCollision()
        elif (self.current_time - self.transition_timer) < 915:
            self.image = frames[2]
            self.Mario_AdjustCollision()
            self.in_transition_state = False
            self.state = gGameSettings.MARIO_STATE_WALK
            self.big = False
            self.transition_timer = 0
            self.hurt_invisible_timer = 0
            self.Mario_ChangeToSmall()


    def Mario_AdjustCollision(self):
        """
        This function is used when Mario's size changes, in order to adjust his collision appropriately.
        """
        x = self.rect.x
        bottom = self.rect.bottom
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = bottom


    def Mario_ChangeToSmall(self):
        """
        This function handles the transition period when Mario changes to small mario after being hit. 
        """
        self.big = False
        self.right_frames = self.right_small_normal_frames
        self.left_frames = self.left_small_normal_frames
        bottom = self.rect.bottom
        left = self.rect.x
        image = self.right_frames[0]
        self.rect = image.get_rect()
        self.rect.bottom = bottom
        self.rect.x = left

    def Mario_PoleSlide(self):
        """
        This function handles the game state in which Mario slide down the flagpole at the end of the level.
        """
        self.state = gGameSettings.MARIO_STATE_ON_FLAGPOLE
        self.in_transition_state = True
        self.x_vel = 0
        self.y_vel = 0

        if self.flag_pole_timer == 0:
            self.flag_pole_timer = self.current_time
        elif self.rect.bottom < 493:
            if (self.current_time - self.flag_pole_timer) < 65:
                self.image = self.right_frames[9]
            elif (self.current_time - self.flag_pole_timer) < 130:
                self.image = self.right_frames[10]
            elif (self.current_time - self.flag_pole_timer) >= 130:
                self.flag_pole_timer = self.current_time

            self.rect.right = self.flag_pole_right
            self.y_vel = 5
            self.rect.y += self.y_vel

            if self.rect.bottom >= 488:
                self.flag_pole_timer = self.current_time

        elif self.rect.bottom >= 493:
            self.image = self.right_frames[10]


    def Mario_BottomOfPole(self):
        """
        This function handles the animation where Mario sits at the bottom of the flagpole before being brought to the castle.
        """
        if self.flag_pole_timer == 0:
            self.flag_pole_timer = self.current_time
            self.image = self.left_frames[10]
        elif (self.current_time - self.flag_pole_timer) < 210:
            self.image = self.left_frames[10]
        else:
            self.in_transition_state = False
            if self.rect.bottom < 485:
                self.state = gGameSettings.MARIO_STATE_END_OF_LEVEL
            else:
                self.state = gGameSettings.MARIO_STATE_WALKING_TO_CASTLE


    def Mario_BottomOfPoleState(self):
        """
        This function handles the gamestate and animation for when Mario is sitting at the bottom of the flagpole at the end of a level.
        """
        self.image = self.left_frames[9]
        right = self.rect.right
        #self.rect.bottom = 493
        self.rect.x = right
        if self.big:
            self.rect.x -= 10
        self.flag_pole_timer = 0
        self.state = gGameSettings.FLAGSTATE_BOTTOM_OF_POLE


    def Mario_WalkingToCastle(self):
        """
        This function handles the gamestate and animation for when Mario walks to the castle at the end of a level.
        """
        self.max_x_vel = 5
        self.x_accel = gGameSettings.MARIO_WALK_ACCELERATION

        if self.x_vel < self.max_x_vel:
            self.x_vel += self.x_accel

        if (self.walking_timer == 0 or (self.current_time - self.walking_timer) > 200):
            self.walking_timer = self.current_time

        elif (self.current_time - self.walking_timer) > \
                self.Mario_Math_CalcAnimationSpeed():
            if self.frame_index < 3:
                self.frame_index += 1
            else:
                self.frame_index = 1
            self.walking_timer = self.current_time


    def Mario_FallAtEnd(self, *args):
        """
        This function sets Mario's y velocity to the gravity of the world in order to send the player flying and give the player a game over, thus restarting the level.
        """
        self.y_vel += gGameSettings.WORLD_GRAVITY



    def Mario_StateCheckSpecial(self):
        """
        This function checks if Mario's state is one of the four "special" states.
        """
        self.Mario_CheckIfInvicible()
        self.Mario_CheckIfFire()
        self.Mario_InvincibilityHurtCheck()
        self.Mario_CrouchCheck()


    def Mario_CheckIfInvicible(self):
        """
        This function checks if Mario is invincible. If he is, then set his losing_invincibility value to True and start a frame countdown.
        """
        if self.invincible:
            if ((self.current_time - self.invincible_start_timer) < 10000):
                self.losing_invincibility = False
                self.Mario_ChangeFrameList(30)
            elif ((self.current_time - self.invincible_start_timer) < 12000):
                self.losing_invincibility = True
                self.Mario_ChangeFrameList(100)
            else:
                self.losing_invincibility = False
                self.invincible = False
        else:
            if self.big:
                self.right_frames = self.right_big_normal_frames
                self.left_frames = self.left_big_normal_frames
            else:
                self.right_frames = self.invincible_small_frames_list[0][0]
                self.left_frames = self.invincible_small_frames_list[0][1]


    def Mario_ChangeFrameList(self, frame_switch_speed):
        if (self.current_time - self.invincible_animation_timer) > frame_switch_speed:
            if self.invincible_index < (len(self.invincible_small_frames_list) - 1):
                self.invincible_index += 1
            else:
                self.invincible_index = 0

            if self.big:
                frames = self.invincible_big_frames_list[self.invincible_index]
            else:
                frames = self.invincible_small_frames_list[self.invincible_index]

            self.right_frames = frames[0]
            self.left_frames = frames[1]

            self.invincible_animation_timer = self.current_time


    def Mario_CheckIfFire(self):
        if self.fire and self.invincible == False:
            self.right_frames = self.fire_frames[0]
            self.left_frames = self.fire_frames[1]


    def Mario_InvincibilityHurtCheck(self):
        """
        This function checks if Mario is hurt during the cooldown period after getting hit.
        """
        if self.hurt_invincible and self.state != gGameSettings.MARIO_STATE_BIG_TO_SMALL:
            if self.hurt_invisible_timer2 == 0:
                self.hurt_invisible_timer2 = self.current_time
            elif (self.current_time - self.hurt_invisible_timer2) < 2000:
                self.Mario_SetInvincibility()
            else:
                self.hurt_invincible = False
                self.hurt_invisible_timer = 0
                self.hurt_invisible_timer2 = 0
                for frames in self.all_images:
                    for image in frames:
                        image.set_alpha(255)


    def Mario_SetInvincibility(self):
        """
        This function makes mario invicible on a certain time interval after getting hit by an enemy.
        """
        if self.hurt_invisible_timer == 0:
            self.hurt_invisible_timer = self.current_time
        elif (self.current_time - self.hurt_invisible_timer) < 35:
            self.image.set_alpha(0)
        elif (self.current_time - self.hurt_invisible_timer) < 70:
            self.image.set_alpha(255)
            self.hurt_invisible_timer = self.current_time


    def Mario_CrouchCheck(self):
        """
        This function checks if Mario is crouching. If he is, set animation to crouch and change collision.
        """
        if self.crouching and self.big:
            bottom = self.rect.bottom
            left = self.rect.x
            if self.facing_right:
                self.image = self.right_frames[7]
            else:
                self.image = self.left_frames[7]
            self.rect = self.image.get_rect()
            self.rect.bottom = bottom
            self.rect.x = left


    def Mario_SetAnimationImage(self):
        """
        This function adjusts Mario's image for his animation depending on what his state value is.
        """
        if self.state == gGameSettings.GOOMBA_STATE_DEATH \
            or self.state == gGameSettings.MARIO_STATE_SMALL_TO_BIG \
            or self.state == gGameSettings.MARIO_STATE_BIG_TO_FIRE \
            or self.state == gGameSettings.MARIO_STATE_BIG_TO_SMALL \
            or self.state == gGameSettings.MARIO_STATE_ON_FLAGPOLE \
            or self.state == gGameSettings.FLAGSTATE_BOTTOM_OF_POLE \
            or self.crouching:
            pass
        elif self.facing_right:
            self.image = self.right_frames[self.frame_index]
        else:
            self.image = self.left_frames[self.frame_index]
