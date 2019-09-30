

from . import setup,tools
from .states import main_menu,load_screen,level1
from . import csts


def main():

    run_it = tools.Control(setup.ORIGINAL_TITLE)
    state_dict = {csts.MAIN_MENU: main_menu.Menu(),
                  csts.LOAD_SCREEN: load_screen.LoadScreen(),
                  csts.TIME_OUT: load_screen.TimeOut(),
                  csts.GAME_OVER: load_screen.GameOver(),
                  csts.LEVEL1: level1.Level1()}

    run_it.setup_states(state_dict, csts.MAIN_MENU)
    run_it.main()
