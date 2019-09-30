
import pygame
from . import setup
from . import csts

class Sound(object):
    def __init__(self, overhead_info):
        self.sfx_dict = setup.SFX
        self.music_dict = setup.MUSIC
        self.overhead_info = overhead_info
        self.ginfo = overhead_info.ginfo
        self.set_music_mixer()



    def set_music_mixer(self):
        if self.overhead_info.state == csts.LEVEL:
            pygame.mixer.music.load(self.music_dict['main_theme'])
            pygame.mixer.music.play()
            self.state = csts.NORMAL
        elif self.overhead_info.state == csts.GAME_OVER:
            pygame.mixer.music.load(self.music_dict['game_over'])
            pygame.mixer.music.play()
            self.state = csts.GAME_OVER


    def update(self, ginfo, mario):
        self.ginfo = ginfo
        self.mario = mario
        self.standHandler()

    def  standHandler(self):
        if self.state == csts.NORMAL:
            if self.mario.dead:
                self.play_music('death', csts.MARIO_DEAD)
            elif self.mario.invincible \
                    and self.mario.losing_invincibility == False:
                self.play_music('invincible', csts.MARIO_INVINCIBLE)
            elif self.mario.state == csts.FLAGPOLE:
                self.play_music('flagpole', csts.FLAGPOLE)
            elif self.overhead_info.time == 100:
                self.play_music('out_of_time', csts.TIME_WARNING)


        elif self.state == csts.FLAGPOLE:
            if self.mario.state == csts.WALKING_TO_CASTLE:
                self.play_music('stage_clear', csts.STAGE_CLEAR)

        elif self.state == csts.STAGE_CLEAR:
            if self.mario.in_castle:
                self.sfx_dict['count_down'].play()
                self.state = csts.FAST_COUNT_DOWN

        elif self.state == csts.FAST_COUNT_DOWN:
            if self.overhead_info.time == 0:
                self.sfx_dict['count_down'].stop()
                self.state = csts.WORLD_CLEAR

        elif self.state == csts.TIME_WARNING:
            if pygame.mixer.music.get_busy() == 0:
                self.play_music('main_theme_sped_up', csts.SPED_UP_NORMAL)
            elif self.mario.dead:
                self.play_music('death', csts.MARIO_DEAD)

        elif self.state == csts.SPED_UP_NORMAL:
            if self.mario.dead:
                self.play_music('death', csts.MARIO_DEAD)
            elif self.mario.state == csts.FLAGPOLE:
                self.play_music('flagpole', csts.FLAGPOLE)

        elif self.state == csts.MARIO_INVINCIBLE:
            if (self.mario.current_time - self.mario.invincible_start_timer) > 11000:
                self.play_music('main_theme', csts.NORMAL)
            elif self.mario.dead:
                self.play_music('death', csts.MARIO_DEAD)


        elif self.state == csts.WORLD_CLEAR:
            pass
        elif self.state == csts.MARIO_DEAD:
            pass
        elif self.state == csts.GAME_OVER:
            pass

    def play_music(self, key, state):
        pygame.mixer.music.load(self.music_dict[key])
        pygame.mixer.music.play()
        self.state = state

    def stop_music(self):
        pygame.mixer.music.stop()
