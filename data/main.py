

from . import setup,tools
from .states import main_menu,load_screen,level1
from . import gGameSettings

def main():
    """
    This function initializes global game settings that will be used to start the game.
    Global game settings are accessed using gGameSettings.{setting}.
    """
    run_it = tools.Control(setup.ORIGINAL_TITLE)
    state_dict = {gGameSettings.GLOBALSTATE_MAIN_MENU: main_menu.Menu(),
                  gGameSettings.GLOBALSTATE_LOAD_SCREEN: load_screen.LoadScreen(),
                  gGameSettings.GLOBALSTATE_TIME_OUT: load_screen.TimeOut(),
                  gGameSettings.GLOBALSTATE_GAME_OVER: load_screen.GameOver(),
                  gGameSettings.GLOBALSTATE_LEVEL1: level1.Level1()}

    run_it.setup_states(state_dict, gGameSettings.GLOBALSTATE_MAIN_MENU)
    run_it.main()
