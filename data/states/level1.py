from __future__ import division


import pygame
from .. import setup, tools
from .. import gGameSettings
from .. import game_sound
from .. components import mario
from .. components import collider
from .. components import bricks
from .. components import coin_box
from .. components import enemies
from .. components import checkpoint
from .. components import flagpole
from .. components import info
from .. components import score
from .. components import castle_flag


class Level1(tools.GameState_Initialize):
    """
    This function contains all code needed to execute Level1. 
    It mostly consists of animation data, which was primarily generated through a C program that parsed level data.
    """
    def __init__(self):
        tools.GameState_Initialize.__init__(self)

    def startup(self, current_time, persist):
        self.gGameInfo = persist
        self.persist = self.gGameInfo
        self.gGameInfo[gGameSettings.GLOBAL_TIME] = current_time
        self.gGameInfo[gGameSettings.GLOBAL_LEVEL_STATE] = gGameSettings.GLOBALSTATE_GAME_PLAY
        self.gGameInfo[gGameSettings.MARIO_STATE_DEAD] = False

        self.state = gGameSettings.GLOBALSTATE_GAME_PLAY
        self.death_timer = 0
        self.flag_timer = 0
        self.flag_score = None
        self.flag_score_total = 0

        self.moving_score_list = []
        self.overhead_info_display = info.HeaderInfo(self.gGameInfo, gGameSettings.GLOBAL_CURRENT_LEVEL)
        self.sound_manager = game_sound.Sound(self.overhead_info_display)

        self.bgSetup()
        self.groundSetup()
        self.pipeSetup()
        self.setup_steps()
        self.brickSetup()
        self.coinBoxSetup()
        self.fpSetup()
        self.enemySetup()
        self.marioSetup()
        self.checkpointSetup()
        self.setup_spritegroups()


    def bgSetup(self):
        self.background = setup.GFX['level_1']
        self.back_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background,
                                  (int(self.back_rect.width*gGameSettings.BACKGROUND_MULTIPLER),
                                  int(self.back_rect.height*gGameSettings.BACKGROUND_MULTIPLER)))
        self.back_rect = self.background.get_rect()
        width = self.back_rect.width
        height = self.back_rect.height

        self.level = pygame.Surface((width, height)).convert()
        self.level_rect = self.level.get_rect()
        self.viewport = setup.SCREEN.get_rect(bottom=self.level_rect.bottom)
        self.viewport.x = self.gGameInfo[gGameSettings.CAMERA_START_X]


    def groundSetup(self):
        ground_rect1 = collider.Collider(0, gGameSettings.gr_height,    2953, 60)
        ground_rect2 = collider.Collider(3048, gGameSettings.gr_height,  635, 60)
        ground_rect3 = collider.Collider(3819, gGameSettings.gr_height, 2735, 60)
        ground_rect4 = collider.Collider(6647, gGameSettings.gr_height, 2300, 60)

        self.ground_group = pygame.sprite.Group(ground_rect1,
                                           ground_rect2,
                                           ground_rect3,
                                           ground_rect4)


    def pipeSetup(self):

        pipe1 = collider.Collider(1202, 452, 83, 82)
        pipe2 = collider.Collider(1631, 409, 83, 140)
        pipe3 = collider.Collider(1973, 366, 83, 170)
        pipe4 = collider.Collider(2445, 366, 83, 170)
        pipe5 = collider.Collider(6989, 452, 83, 82)
        pipe6 = collider.Collider(7675, 452, 83, 82)

        self.pipe_group = pygame.sprite.Group(pipe1, pipe2,
                                          pipe3, pipe4,
                                          pipe5, pipe6)


    def setup_steps(self):
        step1 = collider.Collider(5745, 495, 40, 44)
        step2 = collider.Collider(5788, 452, 40, 44)
        step3 = collider.Collider(5831, 409, 40, 44)
        step4 = collider.Collider(5874, 366, 40, 176)


        step5 = collider.Collider(6001, 366, 40, 176)
        step6 = collider.Collider(6044, 408, 40, 40)
        step7 = collider.Collider(6087, 452, 40, 40)
        step8 = collider.Collider(6130, 495, 40, 40)

        step9 = collider.Collider(6345, 495, 40, 40)
        step10 = collider.Collider(6388, 452, 40, 40)
        step11 = collider.Collider(6431, 409, 40, 40)
        step12 = collider.Collider(6474, 366, 40, 40)
        step13 = collider.Collider(6517, 366, 40, 176)

        step14 = collider.Collider(6644, 366, 40, 176)
        step15 = collider.Collider(6687, 408, 40, 40)
        step16 = collider.Collider(6728, 452, 40, 40)
        step17 = collider.Collider(6771, 495, 40, 40)

        step18 = collider.Collider(7760, 495, 40, 40)
        step19 = collider.Collider(7803, 452, 40, 40)
        step20 = collider.Collider(7845, 409, 40, 40)
        step21 = collider.Collider(7888, 366, 40, 40)
        step22 = collider.Collider(7931, 323, 40, 40)
        step23 = collider.Collider(7974, 280, 40, 40)
        step24 = collider.Collider(8017, 237, 40, 40)
        step25 = collider.Collider(8060, 194, 40, 40)
        step26 = collider.Collider(8103, 194, 40, 360)

        step27 = collider.Collider(8488, 495, 40, 40)

        self.step_group = pygame.sprite.Group(step1,  step2,
                                          step3,  step4,
                                          step5,  step6,
                                          step7,  step8,
                                          step9,  step10,
                                          step11, step12,
                                          step13, step14,
                                          step15, step16,
                                          step17, step18,
                                          step19, step20,
                                          step21, step22,
                                          step23, step24,
                                          step25, step26,
                                          step27)


    def brickSetup(self):

        self.coin_group = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.brick_pieces_group = pygame.sprite.Group()

        brick1  = bricks.Brick(858,  365)
        brick2  = bricks.Brick(944,  365)
        brick3  = bricks.Brick(1030, 365)
        brick4  = bricks.Brick(3299, 365)
        brick5  = bricks.Brick(3385, 365)
        brick6  = bricks.Brick(3430, 193)
        brick7  = bricks.Brick(3473, 193)
        brick8  = bricks.Brick(3516, 193)
        brick9  = bricks.Brick(3559, 193)
        brick10 = bricks.Brick(3602, 193)
        brick11 = bricks.Brick(3645, 193)
        brick12 = bricks.Brick(3688, 193)
        brick13 = bricks.Brick(3731, 193)
        brick14 = bricks.Brick(3901, 193)
        brick15 = bricks.Brick(3944, 193)
        brick16 = bricks.Brick(3987, 193)
        brick17 = bricks.Brick(4030, 365, gGameSettings.BRICK_CONTAINS_SIX_COINS, self.coin_group)
        brick18 = bricks.Brick(4287, 365)
        brick19 = bricks.Brick(4330, 365, gGameSettings.BRICK_CONTENTS_STAR, self.powerups)
        brick20 = bricks.Brick(5058, 365)
        brick21 = bricks.Brick(5187, 193)
        brick22 = bricks.Brick(5230, 193)
        brick23 = bricks.Brick(5273, 193)
        brick24 = bricks.Brick(5488, 193)
        brick25 = bricks.Brick(5574, 193)
        brick26 = bricks.Brick(5617, 193)
        brick27 = bricks.Brick(5531, 365)
        brick28 = bricks.Brick(5574, 365)
        brick29 = bricks.Brick(7202, 365)
        brick30 = bricks.Brick(7245, 365)
        brick31 = bricks.Brick(7331, 365)

        self.brick_group = pygame.sprite.Group(brick1,  brick2,
                                           brick3,  brick4,
                                           brick5,  brick6,
                                           brick7,  brick8,
                                           brick9,  brick10,
                                           brick11, brick12,
                                           brick13, brick14,
                                           brick15, brick16,
                                           brick17, brick18,
                                           brick19, brick20,
                                           brick21, brick22,
                                           brick23, brick24,
                                           brick25, brick26,
                                           brick27, brick28,
                                           brick29, brick30,
                                           brick31)


    def coinBoxSetup(self):

        coin_box1  = coin_box.Coin_box(685, 365, gGameSettings.BRICK_CONTENTS_COIN, self.coin_group)
        coin_box2  = coin_box.Coin_box(901, 365, gGameSettings.BRICK_CONTENTS_MUSHROOM, self.powerups)
        coin_box3  = coin_box.Coin_box(987, 365, gGameSettings.BRICK_CONTENTS_COIN, self.coin_group)
        coin_box4  = coin_box.Coin_box(943, 193, gGameSettings.BRICK_CONTENTS_COIN, self.coin_group)
        coin_box5  = coin_box.Coin_box(3342, 365, gGameSettings.BRICK_CONTENTS_MUSHROOM, self.powerups)
        coin_box6  = coin_box.Coin_box(4030, 193, gGameSettings.BRICK_CONTENTS_COIN, self.coin_group)
        coin_box7  = coin_box.Coin_box(4544, 365, gGameSettings.BRICK_CONTENTS_COIN, self.coin_group)
        coin_box8  = coin_box.Coin_box(4672, 365, gGameSettings.BRICK_CONTENTS_COIN, self.coin_group)
        coin_box9  = coin_box.Coin_box(4672, 193, gGameSettings.BRICK_CONTENTS_MUSHROOM, self.powerups)
        coin_box10 = coin_box.Coin_box(4800, 365, gGameSettings.BRICK_CONTENTS_COIN, self.coin_group)
        coin_box11 = coin_box.Coin_box(5531, 193, gGameSettings.BRICK_CONTENTS_COIN, self.coin_group)
        coin_box12 = coin_box.Coin_box(7288, 365, gGameSettings.BRICK_CONTENTS_COIN, self.coin_group)

        self.coin_box_group = pygame.sprite.Group(coin_box1,  coin_box2,
                                              coin_box3,  coin_box4,
                                              coin_box5,  coin_box6,
                                              coin_box7,  coin_box8,
                                              coin_box9,  coin_box10,
                                              coin_box11, coin_box12)


    def fpSetup(self):

        self.flag = flagpole.Flag(8505, 100)

        pole0 = flagpole.Pole(8505, 97)
        pole1 = flagpole.Pole(8505, 137)
        pole2 = flagpole.Pole(8505, 177)
        pole3 = flagpole.Pole(8505, 217)
        pole4 = flagpole.Pole(8505, 257)
        pole5 = flagpole.Pole(8505, 297)
        pole6 = flagpole.Pole(8505, 337)
        pole7 = flagpole.Pole(8505, 377)
        pole8 = flagpole.Pole(8505, 417)
        pole9 = flagpole.Pole(8505, 450)

        finial = flagpole.Finial(8507, 97)

        self.flag_pole_group = pygame.sprite.Group(self.flag,
                                               finial,
                                               pole0,
                                               pole1,
                                               pole2,
                                               pole3,
                                               pole4,
                                               pole5,
                                               pole6,
                                               pole7,
                                               pole8,
                                               pole9)


    def enemySetup(self):

        goomba0 = enemies.Goomba()
        goomba1 = enemies.Goomba()
        goomba2 = enemies.Goomba()
        goomba3 = enemies.Goomba()
        goomba4 = enemies.Goomba(193)
        goomba5 = enemies.Goomba(193)
        goomba6 = enemies.Goomba()
        goomba7 = enemies.Goomba()
        goomba8 = enemies.Goomba()
        goomba9 = enemies.Goomba()
        goomba10 = enemies.Goomba()
        goomba11 = enemies.Goomba()
        goomba12 = enemies.Goomba()
        goomba13 = enemies.Goomba()
        goomba14 = enemies.Goomba()
        goomba15 = enemies.Goomba()

        koopa0 = enemies.Koopa()

        enemy_group1 = pygame.sprite.Group(goomba0)
        enemy_group2 = pygame.sprite.Group(goomba1)
        enemy_group3 = pygame.sprite.Group(goomba2, goomba3)
        enemy_group4 = pygame.sprite.Group(goomba4, goomba5)
        enemy_group5 = pygame.sprite.Group(goomba6, goomba7)
        enemy_group6 = pygame.sprite.Group(koopa0)
        enemy_group7 = pygame.sprite.Group(goomba8, goomba9)
        enemy_group8 = pygame.sprite.Group(goomba10, goomba11)
        enemy_group9 = pygame.sprite.Group(goomba12, goomba13)
        enemy_group10 = pygame.sprite.Group(goomba14, goomba15)

        self.enemy_group_list = [enemy_group1,
                                 enemy_group2,
                                 enemy_group3,
                                 enemy_group4,
                                 enemy_group5,
                                 enemy_group6,
                                 enemy_group7,
                                 enemy_group8,
                                 enemy_group9,
                                 enemy_group10]


    def marioSetup(self):

        self.mario = mario.Mario()
        self.mario.rect.x = self.viewport.x + 110
        self.mario.rect.bottom = gGameSettings.gr_height


    def checkpointSetup(self):

        check1 = checkpoint.Checkpoint(510, "1")
        check2 = checkpoint.Checkpoint(1400, '2')
        check3 = checkpoint.Checkpoint(1740, '3')
        check4 = checkpoint.Checkpoint(3080, '4')
        check5 = checkpoint.Checkpoint(3750, '5')
        check6 = checkpoint.Checkpoint(4150, '6')
        check7 = checkpoint.Checkpoint(4470, '7')
        check8 = checkpoint.Checkpoint(4950, '8')
        check9 = checkpoint.Checkpoint(5100, '9')
        check10 = checkpoint.Checkpoint(6800, '10')
        check11 = checkpoint.Checkpoint(8504, '11', 5, 6)
        check12 = checkpoint.Checkpoint(8775, '12')
        check13 = checkpoint.Checkpoint(2740, 'secret_mushroom', 360, 40, 12)

        self.check_point_group = pygame.sprite.Group(check1, check2, check3,
                                                 check4, check5, check6,
                                                 check7, check8, check9,
                                                 check10, check11, check12,
                                                 check13)


    def setup_spritegroups(self):

        self.sprites_about_to_die_group = pygame.sprite.Group()
        self.shell_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()

        self.ground_step_pipe_group = pygame.sprite.Group(self.ground_group,
                                                      self.pipe_group,
                                                      self.step_group)

        self.mario_and_enemy_group = pygame.sprite.Group(self.mario,
                                                     self.enemy_group)


    def update(self, surface, keys, current_time):

        self.gGameInfo[gGameSettings.GLOBAL_TIME] = self.current_time = current_time
        self.standHandlers(keys)
        self.check_if_time_out()
        self.blitScr(surface)
        self.sound_manager.update(self.gGameInfo, self.mario)



    def standHandlers(self, keys):
        if self.state == gGameSettings.GLOBALSTATE_PAUSED:
            self.update_during_transition_state(keys)
        elif self.state == gGameSettings.GLOBALSTATE_GAME_PLAY:
            self.update_all_sprites(keys)
        elif self.state == gGameSettings.GLOBALSTATE_IN_CASTLE:
            self.update_while_in_castle()
        elif self.state == gGameSettings.GLOBALSTATE_FLAG_AND_FIREWORKS:
            self.update_flag_and_fireworks()


    def update_during_transition_state(self, keys):
        self.mario.update(keys, self.gGameInfo, self.powerups)
        for score in self.moving_score_list:
            score.update(self.moving_score_list, self.gGameInfo)
        if self.flag_score:
            self.flag_score.update(None, self.gGameInfo)
            self.check_to_add_flag_score()
        self.coin_box_group.update(self.gGameInfo)
        self.flag_pole_group.update(self.gGameInfo)
        self.check_if_mario_in_transition_state()
        self.check_flag()
        self.check_for_mario_death()
        self.overhead_info_display.update(self.gGameInfo, self.mario)


    def check_if_mario_in_transition_state(self):
        if self.mario.in_transition_state:
            self.gGameInfo[gGameSettings.GLOBAL_LEVEL_STATE] = self.state = gGameSettings.GLOBALSTATE_PAUSED
        elif self.mario.in_transition_state == False:
            if self.state == gGameSettings.GLOBALSTATE_PAUSED:
                self.gGameInfo[gGameSettings.GLOBAL_LEVEL_STATE] = self.state = gGameSettings.GLOBALSTATE_GAME_PLAY


    def update_all_sprites(self, keys):

        self.mario.update(keys, self.gGameInfo, self.powerups)
        for score in self.moving_score_list:
            score.update(self.moving_score_list, self.gGameInfo)
        if self.flag_score:
            self.flag_score.update(None, self.gGameInfo)
            self.check_to_add_flag_score()
        self.flag_pole_group.update()
        self.check_points_check()
        self.enemy_group.update(self.gGameInfo)
        self.sprites_about_to_die_group.update(self.gGameInfo, self.viewport)
        self.shell_group.update(self.gGameInfo)
        self.brick_group.update()
        self.coin_box_group.update(self.gGameInfo)
        self.powerups.update(self.gGameInfo, self.viewport)
        self.coin_group.update(self.gGameInfo, self.viewport)
        self.brick_pieces_group.update()
        self.adjust_sprite_positions()
        self.check_if_mario_in_transition_state()
        self.check_for_mario_death()
        self.update_viewport()
        self.overhead_info_display.update(self.gGameInfo, self.mario)


    def check_points_check(self):

        checkpoint = pygame.sprite.spritecollideany(self.mario,
                                                 self.check_point_group)
        if checkpoint:
            checkpoint.kill()

            for i in range(1,11):
                if checkpoint.name == str(i):
                    for index, enemy in enumerate(self.enemy_group_list[i -1]):
                        enemy.rect.x = self.viewport.right + (index * 60)
                    self.enemy_group.add(self.enemy_group_list[i-1])

            if checkpoint.name == '11':
                self.mario.state = gGameSettings.MARIO_STATE_ON_FLAGPOLE
                self.mario.invincible = False
                self.mario.flag_pole_right = checkpoint.rect.right
                if self.mario.rect.bottom < self.flag.rect.y:
                    self.mario.rect.bottom = self.flag.rect.y
                self.flag.state = gGameSettings.FLAGSTATE_SLIDE_DOWN
                self.create_flag_points()

            elif checkpoint.name == '12':
                self.state = gGameSettings.GLOBALSTATE_IN_CASTLE
                self.mario.kill()
                self.mario.state == gGameSettings.MARIO_STATE_STANDING
                self.mario.in_castle = True
                self.overhead_info_display.state = gGameSettings.GLOBAL_FAST_COUNT_DOWN


            elif checkpoint.name == 'secret_mushroom' and self.mario.y_vel < 0:
                mushroom_box = coin_box.Coin_box(checkpoint.rect.x,
                                        checkpoint.rect.bottom - 40,
                                        '1up_mushroom',
                                        self.powerups)
                mushroom_box.start_bump(self.moving_score_list)
                self.coin_box_group.add(mushroom_box)

                self.mario.y_vel = 7
                self.mario.rect.y = mushroom_box.rect.bottom
                self.mario.state = gGameSettings.MARIO_STATE_FALL

            self.mario_and_enemy_group.add(self.enemy_group)


    def create_flag_points(self):
        x = 8518
        y = gGameSettings.gr_height - 60
        mario_bottom = self.mario.rect.bottom

        if mario_bottom > (gGameSettings.gr_height - 40 - 40):
            self.flag_score = score.Score(x, y, 100, True)
            self.flag_score_total = 100
        elif mario_bottom > (gGameSettings.gr_height - 40 - 160):
            self.flag_score = score.Score(x, y, 400, True)
            self.flag_score_total = 400
        elif mario_bottom > (gGameSettings.gr_height - 40 - 240):
            self.flag_score = score.Score(x, y, 800, True)
            self.flag_score_total = 800
        elif mario_bottom > (gGameSettings.gr_height - 40 - 360):
            self.flag_score = score.Score(x, y, 2000, True)
            self.flag_score_total = 2000
        else:
            self.flag_score = score.Score(x, y, 5000, True)
            self.flag_score_total = 5000


    def adjust_sprite_positions(self):

        self.adjust_mario_position()
        self.adjust_enemy_position()
        self.adjust_shell_position()
        self.adjust_powerup_position()


    def adjust_mario_position(self):

        self.last_x_position = self.mario.rect.right
        self.mario.rect.x += round(self.mario.x_vel)
        self.check_mario_x_collisions()

        if self.mario.in_transition_state == False:
            self.mario.rect.y += round(self.mario.y_vel)
            self.check_mario_y_collisions()

        if self.mario.rect.x < (self.viewport.x + 5):
            self.mario.rect.x = (self.viewport.x + 5)


    def check_mario_x_collisions(self):

        collider = pygame.sprite.spritecollideany(self.mario, self.ground_step_pipe_group)
        coin_box = pygame.sprite.spritecollideany(self.mario, self.coin_box_group)
        brick = pygame.sprite.spritecollideany(self.mario, self.brick_group)
        enemy = pygame.sprite.spritecollideany(self.mario, self.enemy_group)
        shell = pygame.sprite.spritecollideany(self.mario, self.shell_group)
        powerup = pygame.sprite.spritecollideany(self.mario, self.powerups)

        if coin_box:
            self.adjust_mario_for_x_collisions(coin_box)

        elif brick:
            self.adjust_mario_for_x_collisions(brick)

        elif collider:
            self.adjust_mario_for_x_collisions(collider)

        elif enemy:
            if self.mario.invincible:
                setup.SFX['kick'].play()
                self.gGameInfo[gGameSettings.GLOBAL_SCORE] += 100
                self.moving_score_list.append(
                    score.Score(self.mario.rect.right - self.viewport.x,
                                self.mario.rect.y, 100))
                enemy.kill()
                enemy.start_death_jump(gGameSettings.GOOMBA_STATE_MOVING_RIGHT)
                self.sprites_about_to_die_group.add(enemy)
            elif self.mario.big:
                setup.SFX['pipe'].play()
                self.mario.fire = False
                self.mario.y_vel = -1
                self.mario.state = gGameSettings.MARIO_STATE_BIG_TO_SMALL
                self.convert_fireflowers_to_mushrooms()
            elif self.mario.hurt_invincible:
                pass
            else:
                self.mario.InitializeDeathJump(self.gGameInfo)
                self.state = gGameSettings.GLOBALSTATE_PAUSED

        elif shell:
            self.adjust_mario_for_x_shell_collisions(shell)

        elif powerup:
            if powerup.name == gGameSettings.BRICK_CONTENTS_STAR:
                self.gGameInfo[gGameSettings.GLOBAL_SCORE] += 1000

                self.moving_score_list.append(
                    score.Score(self.mario.rect.centerx - self.viewport.x,
                                self.mario.rect.y, 1000))
                self.mario.invincible = True
                self.mario.invincible_start_timer = self.current_time
            elif powerup.name == gGameSettings.BRICK_CONTENTS_MUSHROOM:
                setup.SFX['powerup'].play()
                self.gGameInfo[gGameSettings.GLOBAL_SCORE] += 1000
                self.moving_score_list.append(
                    score.Score(self.mario.rect.centerx - self.viewport.x,
                                self.mario.rect.y - 20, 1000))

                self.mario.y_vel = -1
                self.mario.state = gGameSettings.MARIO_STATE_SMALL_TO_BIG
                self.mario.in_transition_state = True
                self.convert_mushrooms_to_fireflowers()
            elif powerup.name == gGameSettings.BRICK_CONTENTS_1UP:
                self.moving_score_list.append(
                    score.Score(powerup.rect.right - self.viewport.x,
                                powerup.rect.y,
                                gGameSettings.SCORE_ONEUP))

                self.gGameInfo[gGameSettings.GLOBAL_LIVES] += 1
                setup.SFX['one_up'].play()
            elif powerup.name == gGameSettings.BRICK_CONTENTS_FIREFLOWER:
                setup.SFX['powerup'].play()
                self.gGameInfo[gGameSettings.GLOBAL_SCORE] += 1000
                self.moving_score_list.append(
                    score.Score(self.mario.rect.centerx - self.viewport.x,
                                self.mario.rect.y, 1000))

                if self.mario.big and self.mario.fire == False:
                    self.mario.state = gGameSettings.MARIO_STATE_BIG_TO_FIRE
                    self.mario.in_transition_state = True
                elif self.mario.big == False:
                    self.mario.state = gGameSettings.MARIO_STATE_SMALL_TO_BIG
                    self.mario.in_transition_state = True
                    self.convert_mushrooms_to_fireflowers()

            if powerup.name != gGameSettings.BRICK_CONTENTS_FIREBALL:
                powerup.kill()


    def convert_mushrooms_to_fireflowers(self):

        for brick in self.brick_group:
            if brick.contents == gGameSettings.BRICK_CONTENTS_MUSHROOM:
                brick.contents = gGameSettings.BRICK_CONTENTS_FIREFLOWER
        for coin_box in self.coin_box_group:
            if coin_box.contents == gGameSettings.BRICK_CONTENTS_MUSHROOM:
                coin_box.contents = gGameSettings.BRICK_CONTENTS_FIREFLOWER


    def convert_fireflowers_to_mushrooms(self):

        for brick in self.brick_group:
            if brick.contents == gGameSettings.BRICK_CONTENTS_FIREFLOWER:
                brick.contents = gGameSettings.BRICK_CONTENTS_MUSHROOM
        for coin_box in self.coin_box_group:
            if coin_box.contents == gGameSettings.BRICK_CONTENTS_FIREFLOWER:
                coin_box.contents = gGameSettings.BRICK_CONTENTS_MUSHROOM


    def adjust_mario_for_x_collisions(self, collider):

        if self.mario.rect.x < collider.rect.x:
            self.mario.rect.right = collider.rect.left
        else:
            self.mario.rect.left = collider.rect.right

        self.mario.x_vel = 0


    def adjust_mario_for_x_shell_collisions(self, shell):

        if shell.state == gGameSettings.GOOMBA_STATE_JUMPED:
            if self.mario.rect.x < shell.rect.x:
                self.gGameInfo[gGameSettings.GLOBAL_SCORE] += 400
                self.moving_score_list.append(
                    score.Score(shell.rect.centerx - self.viewport.x,
                                shell.rect.y,
                                400))
                self.mario.rect.right = shell.rect.left
                shell.direction = gGameSettings.GOOMBA_STATE_MOVING_RIGHT
                shell.x_vel = 5
                shell.rect.x += 5

            else:
                self.mario.rect.left = shell.rect.right
                shell.direction = gGameSettings.GOOMBA_STATE_MOVING_LEFT
                shell.x_vel = -5
                shell.rect.x += -5

            shell.state = gGameSettings.KOOPA_STATE_SLIDING_SHELL

        elif shell.state == gGameSettings.KOOPA_STATE_SLIDING_SHELL:
            if self.mario.big and not self.mario.invincible:
                self.mario.state = gGameSettings.MARIO_STATE_BIG_TO_SMALL
            elif self.mario.invincible:
                self.gGameInfo[gGameSettings.GLOBAL_SCORE] += 200
                self.moving_score_list.append(
                    score.Score(shell.rect.right - self.viewport.x,
                                shell.rect.y, 200))
                shell.kill()
                self.sprites_about_to_die_group.add(shell)
                shell.start_death_jump(gGameSettings.GOOMBA_STATE_MOVING_RIGHT)
            else:
                if not self.mario.hurt_invincible and not self.mario.invincible:
                    self.state = gGameSettings.GLOBALSTATE_PAUSED
                    self.mario.InitializeDeathJump(self.gGameInfo)


    def check_mario_y_collisions(self):

        ground_step_or_pipe = pygame.sprite.spritecollideany(self.mario, self.ground_step_pipe_group)
        enemy = pygame.sprite.spritecollideany(self.mario, self.enemy_group)
        shell = pygame.sprite.spritecollideany(self.mario, self.shell_group)
        brick = pygame.sprite.spritecollideany(self.mario, self.brick_group)
        coin_box = pygame.sprite.spritecollideany(self.mario, self.coin_box_group)
        powerup = pygame.sprite.spritecollideany(self.mario, self.powerups)

        brick, coin_box = self.prevent_collision_conflict(brick, coin_box)

        if coin_box:
            self.adjust_mario_for_y_coin_box_collisions(coin_box)

        elif brick:
            self.adjust_mario_for_y_brick_collisions(brick)

        elif ground_step_or_pipe:
            self.adjust_mario_for_y_ground_pipe_collisions(ground_step_or_pipe)

        elif enemy:
            if self.mario.invincible:
                setup.SFX['kick'].play()
                enemy.kill()
                self.sprites_about_to_die_group.add(enemy)
                enemy.start_death_jump(gGameSettings.GOOMBA_STATE_MOVING_RIGHT)
            else:
                self.adjust_mario_for_y_enemy_collisions(enemy)

        elif shell:
            self.adjust_mario_for_y_shell_collisions(shell)

        elif powerup:
            if powerup.name == gGameSettings.BRICK_CONTENTS_STAR:
                setup.SFX['powerup'].play()
                powerup.kill()
                self.mario.invincible = True
                self.mario.invincible_start_timer = self.current_time

        self.test_if_mario_is_falling()


    def prevent_collision_conflict(self, obstacle1, obstacle2):

        if obstacle1 and obstacle2:
            obstacle1_distance = self.mario.rect.centerx - obstacle1.rect.centerx
            if obstacle1_distance < 0:
                obstacle1_distance *= -1
            obstacle2_distance = self.mario.rect.centerx - obstacle2.rect.centerx
            if obstacle2_distance < 0:
                obstacle2_distance *= -1

            if obstacle1_distance < obstacle2_distance:
                obstacle2 = False
            else:
                obstacle1 = False

        return obstacle1, obstacle2


    def adjust_mario_for_y_coin_box_collisions(self, coin_box):

        if self.mario.rect.y > coin_box.rect.y:
            if coin_box.state == gGameSettings.BRICK_STATE_RESTING:
                if coin_box.contents == gGameSettings.BRICK_CONTENTS_COIN:
                    self.gGameInfo[gGameSettings.GLOBAL_SCORE] += 200
                    coin_box.start_bump(self.moving_score_list)
                    if coin_box.contents == gGameSettings.BRICK_CONTENTS_COIN:
                        self.gGameInfo[gGameSettings.GLOBAL_COIN_TOTAL] += 1
                else:
                    coin_box.start_bump(self.moving_score_list)

            elif coin_box.state == gGameSettings.COIN_STATE_OPENED:
                pass
            setup.SFX['bump'].play()
            self.mario.y_vel = 7
            self.mario.rect.y = coin_box.rect.bottom
            self.mario.state = gGameSettings.MARIO_STATE_FALL
        else:
            self.mario.y_vel = 0
            self.mario.rect.bottom = coin_box.rect.top
            self.mario.state = gGameSettings.MARIO_STATE_WALK


    def adjust_mario_for_y_brick_collisions(self, brick):

        if self.mario.rect.y > brick.rect.y:
            if brick.state == gGameSettings.BRICK_STATE_RESTING:
                if self.mario.big and brick.contents is None:
                    setup.SFX['brick_smash'].play()
                    self.check_if_enemy_on_brick(brick)
                    brick.kill()
                    self.brick_pieces_group.add(
                        bricks.BrickPiece(brick.rect.x,
                                               brick.rect.y - (brick.rect.height/2),
                                               -2, -12),
                        bricks.BrickPiece(brick.rect.right,
                                               brick.rect.y - (brick.rect.height/2),
                                               2, -12),
                        bricks.BrickPiece(brick.rect.x,
                                               brick.rect.y,
                                               -2, -6),
                        bricks.BrickPiece(brick.rect.right,
                                               brick.rect.y,
                                               2, -6))
                else:
                    setup.SFX['bump'].play()
                    if brick.coin_total > 0:
                        self.gGameInfo[gGameSettings.GLOBAL_COIN_TOTAL] += 1
                        self.gGameInfo[gGameSettings.GLOBAL_SCORE] += 200
                    self.check_if_enemy_on_brick(brick)
                    brick.start_bump(self.moving_score_list)
            elif brick.state == gGameSettings.COIN_STATE_OPENED:
                setup.SFX['bump'].play()
            self.mario.y_vel = 7
            self.mario.rect.y = brick.rect.bottom
            self.mario.state = gGameSettings.MARIO_STATE_FALL

        else:
            self.mario.y_vel = 0
            self.mario.rect.bottom = brick.rect.top
            self.mario.state = gGameSettings.MARIO_STATE_WALK


    def check_if_enemy_on_brick(self, brick):

        brick.rect.y -= 5

        enemy = pygame.sprite.spritecollideany(brick, self.enemy_group)

        if enemy:
            setup.SFX['kick'].play()
            self.gGameInfo[gGameSettings.GLOBAL_SCORE] += 100
            self.moving_score_list.append(
                score.Score(enemy.rect.centerx - self.viewport.x,
                            enemy.rect.y,
                            100))
            enemy.kill()
            self.sprites_about_to_die_group.add(enemy)
            if self.mario.rect.centerx > brick.rect.centerx:
                enemy.start_death_jump('right')
            else:
                enemy.start_death_jump('left')

        brick.rect.y += 5



    def adjust_mario_for_y_ground_pipe_collisions(self, collider):

        if collider.rect.bottom > self.mario.rect.bottom:
            self.mario.y_vel = 0
            self.mario.rect.bottom = collider.rect.top
            if self.mario.state == gGameSettings.MARIO_STATE_END_OF_LEVEL:
                self.mario.state = gGameSettings.MARIO_STATE_WALKING_TO_CASTLE
            else:
                self.mario.state = gGameSettings.MARIO_STATE_WALK
        elif collider.rect.top < self.mario.rect.top:
            self.mario.y_vel = 7
            self.mario.rect.top = collider.rect.bottom
            self.mario.state = gGameSettings.MARIO_STATE_FALL


    def test_if_mario_is_falling(self):

        self.mario.rect.y += 1
        test_collide_group = pygame.sprite.Group(self.ground_step_pipe_group,
                                                 self.brick_group,
                                                 self.coin_box_group)


        if pygame.sprite.spritecollideany(self.mario, test_collide_group) is None:
            if self.mario.state != gGameSettings.MARIO_STATE_JUMP \
                and self.mario.state != gGameSettings.GOOMBA_STATE_DEATH \
                and self.mario.state != gGameSettings.MARIO_STATE_SMALL_TO_BIG \
                and self.mario.state != gGameSettings.MARIO_STATE_BIG_TO_FIRE \
                and self.mario.state != gGameSettings.MARIO_STATE_BIG_TO_SMALL \
                and self.mario.state != gGameSettings.MARIO_STATE_ON_FLAGPOLE \
                and self.mario.state != gGameSettings.MARIO_STATE_WALKING_TO_CASTLE \
                and self.mario.state != gGameSettings.MARIO_STATE_END_OF_LEVEL:
                self.mario.state = gGameSettings.MARIO_STATE_FALL
            elif self.mario.state == gGameSettings.MARIO_STATE_WALKING_TO_CASTLE or \
                self.mario.state == gGameSettings.MARIO_STATE_END_OF_LEVEL:
                self.mario.state = gGameSettings.MARIO_STATE_END_OF_LEVEL

        self.mario.rect.y -= 1


    def adjust_mario_for_y_enemy_collisions(self, enemy):

        if self.mario.y_vel > 0:
            setup.SFX['stomp'].play()
            self.gGameInfo[gGameSettings.GLOBAL_SCORE] += 100
            self.moving_score_list.append(
                score.Score(enemy.rect.centerx - self.viewport.x,
                            enemy.rect.y, 100))
            enemy.state = gGameSettings.GOOMBA_STATE_JUMPED
            enemy.kill()
            if enemy.name == gGameSettings.ENEMY_GOOMBA:
                enemy.death_timer = self.current_time
                self.sprites_about_to_die_group.add(enemy)
            elif enemy.name == gGameSettings.ENEMY_KOOPA:
                self.shell_group.add(enemy)

            self.mario.rect.bottom = enemy.rect.top
            self.mario.state = gGameSettings.MARIO_STATE_JUMP
            self.mario.y_vel = -7



    def adjust_mario_for_y_shell_collisions(self, shell):

        if self.mario.y_vel > 0:
            self.gGameInfo[gGameSettings.GLOBAL_SCORE] += 400
            self.moving_score_list.append(
                score.Score(self.mario.rect.centerx - self.viewport.x,
                            self.mario.rect.y, 400))
            if shell.state == gGameSettings.GOOMBA_STATE_JUMPED:
                setup.SFX['kick'].play()
                shell.state = gGameSettings.KOOPA_STATE_SLIDING_SHELL
                if self.mario.rect.centerx < shell.rect.centerx:
                    shell.direction = gGameSettings.GOOMBA_STATE_MOVING_RIGHT
                    shell.rect.left = self.mario.rect.right + 5
                else:
                    shell.direction = gGameSettings.GOOMBA_STATE_MOVING_LEFT
                    shell.rect.right = self.mario.rect.left - 5
            else:
                shell.state = gGameSettings.GOOMBA_STATE_JUMPED


    def adjust_enemy_position(self):

        for enemy in self.enemy_group:
            enemy.rect.x += enemy.x_vel
            self.check_enemy_x_collisions(enemy)

            enemy.rect.y += enemy.y_vel
            self.check_enemy_y_collisions(enemy)
            self.delete_if_off_screen(enemy)


    def check_enemy_x_collisions(self, enemy):

        enemy.kill()

        collider = pygame.sprite.spritecollideany(enemy, self.ground_step_pipe_group)
        enemy_collider = pygame.sprite.spritecollideany(enemy, self.enemy_group)

        if collider:
            if enemy.direction == gGameSettings.GOOMBA_STATE_MOVING_RIGHT:
                enemy.rect.right = collider.rect.left
                enemy.direction = gGameSettings.GOOMBA_STATE_MOVING_LEFT
                enemy.x_vel = -2
            elif enemy.direction == gGameSettings.GOOMBA_STATE_MOVING_LEFT:
                enemy.rect.left = collider.rect.right
                enemy.direction = gGameSettings.GOOMBA_STATE_MOVING_RIGHT
                enemy.x_vel = 2


        elif enemy_collider:
            if enemy.direction == gGameSettings.GOOMBA_STATE_MOVING_RIGHT:
                enemy.rect.right = enemy_collider.rect.left
                enemy.direction = gGameSettings.GOOMBA_STATE_MOVING_LEFT
                enemy_collider.direction = gGameSettings.GOOMBA_STATE_MOVING_RIGHT
                enemy.x_vel = -2
                enemy_collider.x_vel = 2
            elif enemy.direction == gGameSettings.GOOMBA_STATE_MOVING_LEFT:
                enemy.rect.left = enemy_collider.rect.right
                enemy.direction = gGameSettings.GOOMBA_STATE_MOVING_RIGHT
                enemy_collider.direction = gGameSettings.GOOMBA_STATE_MOVING_LEFT
                enemy.x_vel = 2
                enemy_collider.x_vel = -2

        self.enemy_group.add(enemy)
        self.mario_and_enemy_group.add(self.enemy_group)


    def check_enemy_y_collisions(self, enemy):

        collider = pygame.sprite.spritecollideany(enemy, self.ground_step_pipe_group)
        brick = pygame.sprite.spritecollideany(enemy, self.brick_group)
        coin_box = pygame.sprite.spritecollideany(enemy, self.coin_box_group)

        if collider:
            if enemy.rect.bottom > collider.rect.bottom:
                enemy.y_vel = 7
                enemy.rect.top = collider.rect.bottom
                enemy.state = gGameSettings.MARIO_STATE_FALL
            elif enemy.rect.bottom < collider.rect.bottom:

                enemy.y_vel = 0
                enemy.rect.bottom = collider.rect.top
                enemy.state = gGameSettings.MARIO_STATE_WALK

        elif brick:
            if brick.state == gGameSettings.BRICK_STATE_BUMPED:
                enemy.kill()
                self.sprites_about_to_die_group.add(enemy)
                if self.mario.rect.centerx > brick.rect.centerx:
                    enemy.start_death_jump('right')
                else:
                    enemy.start_death_jump('left')

            elif enemy.rect.x > brick.rect.x:
                enemy.y_vel = 7
                enemy.rect.top = brick.rect.bottom
                enemy.state = gGameSettings.MARIO_STATE_FALL
            else:
                enemy.y_vel = 0
                enemy.rect.bottom = brick.rect.top
                enemy.state = gGameSettings.MARIO_STATE_WALK

        elif coin_box:
            if coin_box.state == gGameSettings.BRICK_STATE_BUMPED:
                self.gGameInfo[gGameSettings.GLOBAL_SCORE] += 100
                self.moving_score_list.append(
                    score.Score(enemy.rect.centerx - self.viewport.x,
                                enemy.rect.y, 100))
                enemy.kill()
                self.sprites_about_to_die_group.add(enemy)
                if self.mario.rect.centerx > coin_box.rect.centerx:
                    enemy.start_death_jump('right')
                else:
                    enemy.start_death_jump('left')

            elif enemy.rect.x > coin_box.rect.x:
                enemy.y_vel = 7
                enemy.rect.top = coin_box.rect.bottom
                enemy.state = gGameSettings.MARIO_STATE_FALL
            else:
                enemy.y_vel = 0
                enemy.rect.bottom = coin_box.rect.top
                enemy.state = gGameSettings.MARIO_STATE_WALK


        else:
            enemy.rect.y += 1
            test_group = pygame.sprite.Group(self.ground_step_pipe_group,
                                         self.coin_box_group,
                                         self.brick_group)
            if pygame.sprite.spritecollideany(enemy, test_group) is None:
                if enemy.state != gGameSettings.MARIO_STATE_JUMP:
                    enemy.state = gGameSettings.MARIO_STATE_FALL

            enemy.rect.y -= 1


    def adjust_shell_position(self):

        for shell in self.shell_group:
            shell.rect.x += shell.x_vel
            self.check_shell_x_collisions(shell)

            shell.rect.y += shell.y_vel
            self.check_shell_y_collisions(shell)
            self.delete_if_off_screen(shell)


    def check_shell_x_collisions(self, shell):

        collider = pygame.sprite.spritecollideany(shell, self.ground_step_pipe_group)
        enemy = pygame.sprite.spritecollideany(shell, self.enemy_group)

        if collider:
            setup.SFX['bump'].play()
            if shell.x_vel > 0:
                shell.direction = gGameSettings.GOOMBA_STATE_MOVING_LEFT
                shell.rect.right = collider.rect.left
            else:
                shell.direction = gGameSettings.GOOMBA_STATE_MOVING_RIGHT
                shell.rect.left = collider.rect.right

        if enemy:
            setup.SFX['kick'].play()
            self.gGameInfo[gGameSettings.GLOBAL_SCORE] += 100
            self.moving_score_list.append(
                score.Score(enemy.rect.right - self.viewport.x,
                            enemy.rect.y, 100))
            enemy.kill()
            self.sprites_about_to_die_group.add(enemy)
            enemy.start_death_jump(shell.direction)


    def check_shell_y_collisions(self, shell):

        collider = pygame.sprite.spritecollideany(shell, self.ground_step_pipe_group)

        if collider:
            shell.y_vel = 0
            shell.rect.bottom = collider.rect.top
            shell.state = gGameSettings.KOOPA_STATE_SLIDING_SHELL

        else:
            shell.rect.y += 1
            if pygame.sprite.spritecollideany(shell, self.ground_step_pipe_group) is None:
                shell.state = gGameSettings.MARIO_STATE_FALL
            shell.rect.y -= 1


    def adjust_powerup_position(self):

        for powerup in self.powerups:
            if powerup.name == gGameSettings.BRICK_CONTENTS_MUSHROOM:
                self.adjust_mushroom_position(powerup)
            elif powerup.name == gGameSettings.BRICK_CONTENTS_STAR:
                self.adjust_star_position(powerup)
            elif powerup.name == gGameSettings.BRICK_CONTENTS_FIREBALL:
                self.adjust_fireball_position(powerup)
            elif powerup.name == '1up_mushroom':
                self.adjust_mushroom_position(powerup)


    def adjust_mushroom_position(self, mushroom):

        if mushroom.state != gGameSettings.MUSHROOM_STATE_REVEAL:
            mushroom.rect.x += mushroom.x_vel
            self.check_mushroom_x_collisions(mushroom)

            mushroom.rect.y += mushroom.y_vel
            self.check_mushroom_y_collisions(mushroom)
            self.delete_if_off_screen(mushroom)


    def check_mushroom_x_collisions(self, mushroom):

        collider = pygame.sprite.spritecollideany(mushroom, self.ground_step_pipe_group)
        brick = pygame.sprite.spritecollideany(mushroom, self.brick_group)
        coin_box = pygame.sprite.spritecollideany(mushroom, self.coin_box_group)

        if collider:
            self.adjust_mushroom_for_collision_x(mushroom, collider)

        elif brick:
            self.adjust_mushroom_for_collision_x(mushroom, brick)

        elif coin_box:
            self.adjust_mushroom_for_collision_x(mushroom, coin_box)


    def check_mushroom_y_collisions(self, mushroom):

        collider = pygame.sprite.spritecollideany(mushroom, self.ground_step_pipe_group)
        brick = pygame.sprite.spritecollideany(mushroom, self.brick_group)
        coin_box = pygame.sprite.spritecollideany(mushroom, self.coin_box_group)

        if collider:
            self.adjust_mushroom_for_collision_y(mushroom, collider)
        elif brick:
            self.adjust_mushroom_for_collision_y(mushroom, brick)
        elif coin_box:
            self.adjust_mushroom_for_collision_y(mushroom, coin_box)
        else:
            self.check_if_falling(mushroom, self.ground_step_pipe_group)
            self.check_if_falling(mushroom, self.brick_group)
            self.check_if_falling(mushroom, self.coin_box_group)


    def adjust_mushroom_for_collision_x(self, item, collider):

        if item.rect.x < collider.rect.x:
            item.rect.right = collider.rect.x
            item.direction = gGameSettings.GOOMBA_STATE_MOVING_LEFT
        else:
            item.rect.x = collider.rect.right
            item.direction = gGameSettings.GOOMBA_STATE_MOVING_RIGHT


    def adjust_mushroom_for_collision_y(self, item, collider):

        item.rect.bottom = collider.rect.y
        item.state = gGameSettings.MUSHROOM_STATE_SLIDING
        item.y_vel = 0


    def adjust_star_position(self, star):

        if star.state == gGameSettings.STAR_STATE_BOUNCING:
            star.rect.x += star.x_vel
            self.check_mushroom_x_collisions(star)
            star.rect.y += star.y_vel
            self.check_star_y_collisions(star)
            star.y_vel += star.gravity
            self.delete_if_off_screen(star)


    def check_star_y_collisions(self, star):

        collider = pygame.sprite.spritecollideany(star, self.ground_step_pipe_group)
        brick = pygame.sprite.spritecollideany(star, self.brick_group)
        coin_box = pygame.sprite.spritecollideany(star, self.coin_box_group)

        if collider:
            self.adjust_star_for_collision_y(star, collider)
        elif brick:
            self.adjust_star_for_collision_y(star, brick)
        elif coin_box:
            self.adjust_star_for_collision_y(star, coin_box)


    def adjust_star_for_collision_y(self, star, collider):

        if star.rect.y > collider.rect.y:
            star.rect.y = collider.rect.bottom
            star.y_vel = 0
        else:
            star.rect.bottom = collider.rect.top
            star.start_bounce(-8)


    def adjust_fireball_position(self, fireball):

        if fireball.state == gGameSettings.FIRE_STATE_FLYING:
            fireball.rect.x += fireball.x_vel
            self.check_fireball_x_collisions(fireball)
            fireball.rect.y += fireball.y_vel
            self.check_fireball_y_collisions(fireball)
        elif fireball.state == gGameSettings.FIRE_STATE_BOUNCING:
            fireball.rect.x += fireball.x_vel
            self.check_fireball_x_collisions(fireball)
            fireball.rect.y += fireball.y_vel
            self.check_fireball_y_collisions(fireball)
            fireball.y_vel += fireball.gravity
        self.delete_if_off_screen(fireball)


    def bounce_fireball(self, fireball):

        fireball.y_vel = -8
        if fireball.direction == gGameSettings.GOOMBA_STATE_MOVING_RIGHT:
            fireball.x_vel = 15
        else:
            fireball.x_vel = -15

        if fireball in self.powerups:
            fireball.state = gGameSettings.FIRE_STATE_BOUNCING


    def check_fireball_x_collisions(self, fireball):

        collide_group = pygame.sprite.Group(self.ground_group,
                                        self.pipe_group,
                                        self.step_group,
                                        self.coin_box_group,
                                        self.brick_group)

        collider = pygame.sprite.spritecollideany(fireball, collide_group)

        if collider:
            fireball.kill()
            self.sprites_about_to_die_group.add(fireball)
            fireball.explode_transition()



    def check_fireball_y_collisions(self, fireball):

        collide_group = pygame.sprite.Group(self.ground_group,
                                        self.pipe_group,
                                        self.step_group,
                                        self.coin_box_group,
                                        self.brick_group)

        collider = pygame.sprite.spritecollideany(fireball, collide_group)
        enemy = pygame.sprite.spritecollideany(fireball, self.enemy_group)
        shell = pygame.sprite.spritecollideany(fireball, self.shell_group)

        if collider and (fireball in self.powerups):
            fireball.rect.bottom = collider.rect.y
            self.bounce_fireball(fireball)

        elif enemy:
            self.fireball_kill(fireball, enemy)

        elif shell:
            self.fireball_kill(fireball, shell)


    def fireball_kill(self, fireball, enemy):

        setup.SFX['kick'].play()
        self.gGameInfo[gGameSettings.GLOBAL_SCORE] += 100
        self.moving_score_list.append(
            score.Score(enemy.rect.centerx - self.viewport.x,
                        enemy.rect.y,100))
        fireball.kill()
        enemy.kill()
        self.sprites_about_to_die_group.add(enemy, fireball)
        enemy.start_death_jump(fireball.direction)
        fireball.explode_transition()


    def check_if_falling(self, sprite, sprite_group):

        sprite.rect.y += 1

        if pygame.sprite.spritecollideany(sprite, sprite_group) is None:
            if sprite.state != gGameSettings.MARIO_STATE_JUMP:
                sprite.state = gGameSettings.MARIO_STATE_FALL

        sprite.rect.y -= 1


    def delete_if_off_screen(self, enemy):

        if enemy.rect.x < (self.viewport.x - 300):
            enemy.kill()

        elif enemy.rect.y > (self.viewport.bottom):
            enemy.kill()

        elif enemy.state == gGameSettings.KOOPA_STATE_SLIDING_SHELL:
            if enemy.rect.x > (self.viewport.right + 500):
                enemy.kill()


    def check_flag(self):

        if (self.flag.state == gGameSettings.FLAGSTATE_BOTTOM_OF_POLE
            and self.mario.state == gGameSettings.MARIO_STATE_ON_FLAGPOLE):
            self.mario.Mario_BottomOfPoleState()


    def check_to_add_flag_score(self):

        if self.flag_score.y_vel == 0:
            self.gGameInfo[gGameSettings.GLOBAL_SCORE] += self.flag_score_total
            self.flag_score_total = 0


    def check_for_mario_death(self):

        if self.mario.rect.y > gGameSettings.scr_height and not self.mario.in_castle:
            self.mario.dead = True
            self.mario.x_vel = 0
            self.state = gGameSettings.GLOBALSTATE_PAUSED
            self.gGameInfo[gGameSettings.MARIO_STATE_DEAD] = True

        if self.mario.dead:
            self.play_death_song()


    def play_death_song(self):
        if self.death_timer == 0:
            self.death_timer = self.current_time
        elif (self.current_time - self.death_timer) > 3000:
            self.set_ginfo_values()
            self.done = True


    def set_ginfo_values(self):

        if self.gGameInfo[gGameSettings.GLOBAL_SCORE] > self.persist[gGameSettings.GLOBAL_TOP_SCORE]:
            self.persist[gGameSettings.GLOBAL_TOP_SCORE] = self.gGameInfo[gGameSettings.GLOBAL_SCORE]
        if self.mario.dead:
            self.persist[gGameSettings.GLOBAL_LIVES] -= 1

        if self.persist[gGameSettings.GLOBAL_LIVES] == 0:
            self.next = gGameSettings.GLOBALSTATE_GAME_OVER
            self.gGameInfo[gGameSettings.CAMERA_START_X] = 0
        elif self.mario.dead == False:
            self.next = gGameSettings.GLOBALSTATE_MAIN_MENU
            self.gGameInfo[gGameSettings.CAMERA_START_X] = 0
        elif self.overhead_info_display.time == 0:
            self.next = gGameSettings.GLOBALSTATE_TIME_OUT
        else:
            if self.mario.rect.x > 3670 \
                    and self.gGameInfo[gGameSettings.CAMERA_START_X] == 0:
                self.gGameInfo[gGameSettings.CAMERA_START_X] = 3440
            self.next = gGameSettings.GLOBALSTATE_LOAD_SCREEN


    def check_if_time_out(self):

        if self.overhead_info_display.time <= 0 \
                and not self.mario.dead \
                and not self.mario.in_castle:
            self.state = gGameSettings.GLOBALSTATE_PAUSED
            self.mario.InitializeDeathJump(self.gGameInfo)


    def update_viewport(self):

        third = self.viewport.x + self.viewport.w//3
        mario_center = self.mario.rect.centerx
        mario_right = self.mario.rect.right

        if self.mario.x_vel > 0 and mario_center >= third:
            mult = 0.5 if mario_right < self.viewport.centerx else 1
            new = self.viewport.x + mult * self.mario.x_vel
            highest = self.level_rect.w - self.viewport.w
            self.viewport.x = min(highest, new)


    def update_while_in_castle(self):

        for score in self.moving_score_list:
            score.update(self.moving_score_list, self.gGameInfo)
        self.overhead_info_display.update(self.gGameInfo)

        if self.overhead_info_display.state == gGameSettings.GLOBAL_END_OF_LEVEL:
            self.state = gGameSettings.GLOBALSTATE_FLAG_AND_FIREWORKS
            self.flag_pole_group.add(castle_flag.Flag(8745, 322))


    def update_flag_and_fireworks(self):

        for score in self.moving_score_list:
            score.update(self.moving_score_list, self.gGameInfo)
        self.overhead_info_display.update(self.gGameInfo)
        self.flag_pole_group.update()

        self.end_game()


    def end_game(self):

        if self.flag_timer == 0:
            self.flag_timer = self.current_time
        elif (self.current_time - self.flag_timer) > 2000:
            self.set_ginfo_values()
            self.next = gGameSettings.GLOBALSTATE_GAME_OVER
            self.sound_manager.Music_Stop()
            self.done = True


    def blitScr(self, surface):

        self.level.blit(self.background, self.viewport, self.viewport)
        if self.flag_score:
            self.flag_score.draw(self.level)
        self.powerups.draw(self.level)
        self.coin_group.draw(self.level)
        self.brick_group.draw(self.level)
        self.coin_box_group.draw(self.level)
        self.sprites_about_to_die_group.draw(self.level)
        self.shell_group.draw(self.level)
        self.brick_pieces_group.draw(self.level)
        self.flag_pole_group.draw(self.level)
        self.mario_and_enemy_group.draw(self.level)

        surface.blit(self.level, (0,0), self.viewport)
        self.overhead_info_display.draw(surface)
        for score in self.moving_score_list:
            score.draw(surface)
