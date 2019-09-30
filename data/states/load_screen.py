

from .. import setup, tools
from .. import csts
from .. import game_sound
from ..components import info


class LoadScreen(tools._st):
    def __init__(self):
        tools._st.__init__(self)

    def startup(self, current_time, persist):
        self.start_time = current_time
        self.persist = persist
        self.ginfo = self.persist
        self.next = self.set_next_state()

        info_state = self.set_overhead_info_state()

        self.overhead_info = info.OverheadInfo(self.ginfo, info_state)
        self.sound_manager = game_sound.Sound(self.overhead_info)


    def set_next_state(self):

        return csts.LEVEL1

    def set_overhead_info_state(self):

        return csts.LOAD_SCREEN


    def update(self, surface, keys, current_time):

        if (current_time - self.start_time) < 2400:
            surface.fill(csts.BLACK)
            self.overhead_info.update(self.ginfo)
            self.overhead_info.draw(surface)

        elif (current_time - self.start_time) < 2600:
            surface.fill(csts.BLACK)

        elif (current_time - self.start_time) < 2635:
            surface.fill((106, 150, 252))

        else:
            self.done = True




class GameOver(LoadScreen):

    def __init__(self):
        super(GameOver, self).__init__()


    def set_next_state(self):

        return csts.MAIN_MENU

    def set_overhead_info_state(self):

        return csts.GAME_OVER

    def update(self, surface, keys, current_time):
        self.current_time = current_time
        self.sound_manager.update(self.persist, None)

        if (self.current_time - self.start_time) < 7000:
            surface.fill(csts.BLACK)
            self.overhead_info.update(self.ginfo)
            self.overhead_info.draw(surface)
        elif (self.current_time - self.start_time) < 7200:
            surface.fill(csts.BLACK)
        elif (self.current_time - self.start_time) < 7235:
            surface.fill((106, 150, 252))
        else:
            self.done = True


class TimeOut(LoadScreen):

    def __init__(self):
        super(TimeOut, self).__init__()

    def set_next_state(self):

        if self.persist[csts.LIVES] == 0:
            return csts.GAME_OVER
        else:
            return csts.LOAD_SCREEN

    def set_overhead_info_state(self):

        return csts.TIME_OUT

    def update(self, surface, keys, current_time):
        self.current_time = current_time

        if (self.current_time - self.start_time) < 2400:
            surface.fill(csts.BLACK)
            self.overhead_info.update(self.ginfo)
            self.overhead_info.draw(surface)
        else:
            self.done = True
