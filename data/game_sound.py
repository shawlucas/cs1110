
import pygame
from . import setup
from . import gGameSettings

class Sound(object):
    """
    This is the sound class. It handles the sound of the game.
    """
    def __init__(self, overhead_info):
        self.sfx_dict = setup.SFX
        self.music_dict = setup.MUSIC
        self.overhead_info = overhead_info
        self.gGameInfo = overhead_info.gGameInfo
        self.Music_SetMixer()


    """
    This function sets up a basic pygame mixer
    """
    def Music_SetMixer(self):
    
        if self.overhead_info.state == gGameSettings.GLOBAL_CURRENT_LEVEL:
            pygame.mixer.music.load(self.music_dict['main_theme'])
            pygame.mixer.music.play()
            self.state = gGameSettings.SOUNDSTATE_DEFAULT
        elif self.overhead_info.state == gGameSettings.GLOBALSTATE_GAME_OVER:
            pygame.mixer.music.load(self.music_dict['game_over'])
            pygame.mixer.music.play()
            self.state = gGameSettings.GLOBALSTATE_GAME_OVER


    def update(self, gGameInfo, mario):
        self.gGameInfo = gGameInfo
        self.mario = mario
        self.stateHandler()

    def stateHandler(self):
        if self.state == gGameSettings.SOUNDSTATE_DEFAULT:
            if self.mario.dead:
                self.Music_Play('death', gGameSettings.MARIO_STATE_DEAD)
            elif self.mario.invincible \
                    and self.mario.losing_invincibility == False:
                self.Music_Play('invincible', gGameSettings.SOUNDSTATE_MARIO_STARPOWER)
            elif self.mario.state == gGameSettings.MARIO_STATE_ON_FLAGPOLE:
                self.Music_Play('flagpole', gGameSettings.MARIO_STATE_ON_FLAGPOLE)
            elif self.overhead_info.time == 100:
                self.Music_Play('out_of_time', gGameSettings.SOUNDSTATE_WARNING)


        elif self.state == gGameSettings.MARIO_STATE_ON_FLAGPOLE:
            if self.mario.state == gGameSettings.MARIO_STATE_WALKING_TO_CASTLE:
                self.Music_Play('stage_clear', gGameSettings.SOUNDSTATE_CLEARSTAGE)

        elif self.state == gGameSettings.SOUNDSTATE_CLEARSTAGE:
            if self.mario.in_castle:
                self.sfx_dict['count_down'].play()
                self.state = gGameSettings.GLOBAL_FAST_COUNT_DOWN

        elif self.state == gGameSettings.GLOBAL_FAST_COUNT_DOWN:
            if self.overhead_info.time == 0:
                self.sfx_dict['count_down'].stop()
                self.state = gGameSettings.SOUNDSTATE_CLEARWORLD

        elif self.state == gGameSettings.SOUNDSTATE_WARNING:
            if pygame.mixer.music.get_busy() == 0:
                self.Music_Play('main_theme_sped_up', gGameSettings.SOUNDSTATE_SPED_UP_DEFAULT)
            elif self.mario.dead:
                self.Music_Play('death', gGameSettings.MARIO_STATE_DEAD)

        elif self.state == gGameSettings.SOUNDSTATE_SPED_UP_DEFAULT:
            if self.mario.dead:
                self.Music_Play('death', gGameSettings.MARIO_STATE_DEAD)
            elif self.mario.state == gGameSettings.MARIO_STATE_ON_FLAGPOLE:
                self.Music_Play('flagpole', gGameSettings.MARIO_STATE_ON_FLAGPOLE)

        elif self.state == gGameSettings.SOUNDSTATE_MARIO_STARPOWER:
            if (self.mario.current_time - self.mario.invincible_start_timer) > 11000:
                self.Music_Play('main_theme', gGameSettings.SOUNDSTATE_DEFAULT)
            elif self.mario.dead:
                self.Music_Play('death', gGameSettings.MARIO_STATE_DEAD)


        elif self.state == gGameSettings.SOUNDSTATE_CLEARWORLD:
            pass
        elif self.state == gGameSettings.MARIO_STATE_DEAD:
            pass
        elif self.state == gGameSettings.GLOBALSTATE_GAME_OVER:
            pass

    def Music_Play(self, key, state):
        """
        This function plays music based on a given gamestate.
        
        Parameters:
            key: Dictionary key for music
            state: gamestate
        """
        pygame.mixer.music.load(self.music_dict[key])
        pygame.mixer.music.play()
        self.state = state

    def Music_Stop(self):
        """ 
        This function stops the music
        """
        pygame.mixer.music.stop()
