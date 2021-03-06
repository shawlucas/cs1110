

import pygame
from .. import setup, tools
from .. import gGameSettings
from .. components import info, mario


class Menu(tools.GameState_Initialize):
    """
    This class contains the code needed to run the Menu gamestate.
    """
    def __init__(self):

        tools.GameState_Initialize.__init__(self)
        persist = {gGameSettings.GLOBAL_COIN_TOTAL: 0,
                   gGameSettings.GLOBAL_SCORE: 0,
                   gGameSettings.GLOBAL_LIVES: 3,
                   gGameSettings.GLOBAL_TOP_SCORE: 0,
                   gGameSettings.GLOBAL_TIME: 0.0,
                   gGameSettings.GLOBAL_LEVEL_STATE: None,
                   gGameSettings.CAMERA_START_X: 0,
                   gGameSettings.MARIO_STATE_DEAD: False}
        self.startup(0.0, persist)

    def startup(self, current_time, persist):

        self.next = gGameSettings.GLOBALSTATE_LOAD_SCREEN
        self.persist = persist
        self.gGameInfo = persist
        self.overhead_info = info.HeaderInfo(self.gGameInfo, gGameSettings.GLOBALSTATE_MAIN_MENU)

        self.spr_sheet = setup.GFX['title_screen']
        self.bgSetup()
        self.marioSetup()
        self.setup_cursor()


    def setup_cursor(self):

        self.cursor = pygame.sprite.Sprite()
        dest = (220, 358)
        self.cursor.image, self.cursor.rect = self.getImage(
            24, 160, 8, 8, dest, setup.GFX['item_objects'])
        self.cursor.state = gGameSettings.CURSORSTATE_PLAYER1


    def marioSetup(self):

        self.mario = mario.Mario()
        self.mario.rect.x = 110
        self.mario.rect.bottom = gGameSettings.gr_height


    def bgSetup(self):

        self.background = setup.GFX['level_1']
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(self.background,
                                   (int(self.background_rect.width*gGameSettings.BACKGROUND_MULTIPLER),
                                    int(self.background_rect.height*gGameSettings.BACKGROUND_MULTIPLER)))
        self.viewport = setup.SCREEN.get_rect(bottom=setup.SCREEN_RECT.bottom)

        self.image_dict = {}
        self.image_dict['GAME_NAME_BOX'] = self.getImage(
            1, 60, 176, 88, (170, 100), setup.GFX['title_screen'])



    def getImage(self, x, y, width, height, dest, spr_sheet):

        image = pygame.Surface([width, height])
        rect = image.get_rect()

        image.blit(spr_sheet, (0, 0), (x, y, width, height))
        if spr_sheet == setup.GFX['title_screen']:
            image.set_colorkey((255, 0, 220))
            image = pygame.transform.scale(image,
                                   (int(rect.width*gGameSettings.SIZE_MULTIPLIER),
                                    int(rect.height*gGameSettings.SIZE_MULTIPLIER)))
        else:
            image.set_colorkey(gGameSettings.COLOR_RGB_BLACK)
            image = pygame.transform.scale(image,
                                   (int(rect.width*3),
                                    int(rect.height*3)))

        rect = image.get_rect()
        rect.x = dest[0]
        rect.y = dest[1]
        return (image, rect)


    def update(self, surface, keys, current_time):

        self.current_time = current_time
        self.gGameInfo[gGameSettings.GLOBAL_TIME] = self.current_time
        self.update_cursor(keys)
        self.overhead_info.update(self.gGameInfo)

        surface.blit(self.background, self.viewport, self.viewport)
        surface.blit(self.image_dict['GAME_NAME_BOX'][0],
                     self.image_dict['GAME_NAME_BOX'][1])
        surface.blit(self.mario.image, self.mario.rect)
        surface.blit(self.cursor.image, self.cursor.rect)
        self.overhead_info.draw(surface)


    def update_cursor(self, keys):

        input_list = [pygame.K_RETURN, pygame.K_a, pygame.K_s]

        if self.cursor.state == gGameSettings.CURSORSTATE_PLAYER1:
            self.cursor.rect.y = 358
            if keys[pygame.K_DOWN]:
                self.cursor.state = gGameSettings.CURSORSTATE_PLAYER2
            for input in input_list:
                if keys[input]:
                    self.reset_ginfo()
                    self.done = True
        elif self.cursor.state == gGameSettings.CURSORSTATE_PLAYER2:
            self.cursor.rect.y = 403
            if keys[pygame.K_UP]:
                self.cursor.state = gGameSettings.CURSORSTATE_PLAYER1


    def reset_ginfo(self):

        self.gGameInfo[gGameSettings.GLOBAL_COIN_TOTAL] = 0
        self.gGameInfo[gGameSettings.GLOBAL_SCORE] = 0
        self.gGameInfo[gGameSettings.GLOBAL_LIVES] = 3
        self.gGameInfo[gGameSettings.GLOBAL_TIME] = 0.0
        self.gGameInfo[gGameSettings.GLOBAL_LEVEL_STATE] = None

        self.persist = self.gGameInfo
