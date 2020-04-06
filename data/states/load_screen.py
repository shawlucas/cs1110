

from .. import setup, tools
from .. import gGameSettings
from .. import game_sound
from ..components import info


class LoadScreen(tools.GameState_Initialize):
    """
    This class contains the code needed to run the LoadScreen gamestate.
    """
    def __init__(self):
        tools.GameState_Initialize.__init__(self)

    def startup(self, current_time, persist):
        self.start_time = current_time
        self.persist = persist
        self.gGameInfo = self.persist
        self.next = self.set_next_state()

        info_state = self.set_overhead_info_state()

        self.overhead_info = info.HeaderInfo(self.gGameInfo, info_state)
        self.sound_manager = game_sound.Sound(self.overhead_info)


    def set_next_state(self):

        return gGameSettings.GLOBALSTATE_LEVEL1

    def set_overhead_info_state(self):

        return gGameSettings.GLOBALSTATE_LOAD_SCREEN


    def update(self, surface, keys, current_time):

        if (current_time - self.start_time) < 2400:
            surface.fill(gGameSettings.COLOR_RGB_BLACK)
            self.overhead_info.update(self.gGameInfo)
            self.overhead_info.draw(surface)

        elif (current_time - self.start_time) < 2600:
            surface.fill(gGameSettings.COLOR_RGB_BLACK)

        elif (current_time - self.start_time) < 2635:
            surface.fill((106, 150, 252))

        else:
            self.done = True




class GameOver(LoadScreen):

    def __init__(self):
        super(GameOver, self).__init__()


    def set_next_state(self):

        return gGameSettings.GLOBALSTATE_MAIN_MENU

    def set_overhead_info_state(self):

        return gGameSettings.GLOBALSTATE_GAME_OVER

    def update(self, surface, keys, current_time):
        self.current_time = current_time
        self.sound_manager.update(self.persist, None)

        if (self.current_time - self.start_time) < 7000:
            surface.fill(gGameSettings.COLOR_RGB_BLACK)
            self.overhead_info.update(self.gGameInfo)
            self.overhead_info.draw(surface)
        elif (self.current_time - self.start_time) < 7200:
            surface.fill(gGameSettings.COLOR_RGB_BLACK)
        elif (self.current_time - self.start_time) < 7235:
            surface.fill((106, 150, 252))
        else:
            self.done = True


class TimeOut(LoadScreen):

    def __init__(self):
        super(TimeOut, self).__init__()

    def set_next_state(self):

        if self.persist[gGameSettings.GLOBAL_LIVES] == 0:
            return gGameSettings.GLOBALSTATE_GAME_OVER
        else:
            return gGameSettings.GLOBALSTATE_LOAD_SCREEN

    def set_overhead_info_state(self):

        return gGameSettings.GLOBALSTATE_TIME_OUT

    def update(self, surface, keys, current_time):
        self.current_time = current_time

        if (self.current_time - self.start_time) < 2400:
            surface.fill(gGameSettings.COLOR_RGB_BLACK)
            self.overhead_info.update(self.gGameInfo)
            self.overhead_info.draw(surface)
        else:
            self.done = True
