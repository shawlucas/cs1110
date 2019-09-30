

import pygame
from .. import setup
from .. import csts
from . import flashing_coin


class Character(pygame.sprite.Sprite):

    def __init__(self, image):
        super(Character, self).__init__()
        self.image = image
        self.rect = self.image.get_rect()


class OverheadInfo(object):
    def __init__(self, ginfo, state):
        self.spr_sheet = setup.GFX['text_images']
        self.coin_total = ginfo[csts.COIN_TOTAL]
        self.time = 401
        self.current_time = 0
        self.total_lives = ginfo[csts.LIVES]
        self.top_score = ginfo[csts.TOP_SCORE]
        self.state = state
        self.special_state = None
        self.ginfo = ginfo

        self.create_image_dict()
        self.create_score_group()
        self.create_info_labels()
        self.create_load_screen_labels()
        self.create_countdown_clock()
        self.create_coin_counter()
        self.create_flashing_coin()
        self.create_mario_image()
        self.create_game_over_label()
        self.create_time_out_label()
        self.create_main_menu_labels()


    def create_image_dict(self):
        self.image_dict = {}
        image_list = []

        image_list.append(self.imageGetter(3, 230, 7, 7))
        image_list.append(self.imageGetter(12, 230, 7, 7))
        image_list.append(self.imageGetter(19, 230, 7, 7))
        image_list.append(self.imageGetter(27, 230, 7, 7))
        image_list.append(self.imageGetter(35, 230, 7, 7))
        image_list.append(self.imageGetter(43, 230, 7, 7))
        image_list.append(self.imageGetter(51, 230, 7, 7))
        image_list.append(self.imageGetter(59, 230, 7, 7))
        image_list.append(self.imageGetter(67, 230, 7, 7))
        image_list.append(self.imageGetter(75, 230, 7, 7))

        image_list.append(self.imageGetter(83, 230, 7, 7))
        image_list.append(self.imageGetter(91, 230, 7, 7))
        image_list.append(self.imageGetter(99, 230, 7, 7))
        image_list.append(self.imageGetter(107, 230, 7, 7))
        image_list.append(self.imageGetter(115, 230, 7, 7))
        image_list.append(self.imageGetter(123, 230, 7, 7))
        image_list.append(self.imageGetter(3, 238, 7, 7))
        image_list.append(self.imageGetter(11, 238, 7, 7))
        image_list.append(self.imageGetter(20, 238, 7, 7))
        image_list.append(self.imageGetter(27, 238, 7, 7))
        image_list.append(self.imageGetter(35, 238, 7, 7))
        image_list.append(self.imageGetter(44, 238, 7, 7))
        image_list.append(self.imageGetter(51, 238, 7, 7))
        image_list.append(self.imageGetter(59, 238, 7, 7))
        image_list.append(self.imageGetter(67, 238, 7, 7))
        image_list.append(self.imageGetter(75, 238, 7, 7))
        image_list.append(self.imageGetter(83, 238, 7, 7))
        image_list.append(self.imageGetter(91, 238, 7, 7))
        image_list.append(self.imageGetter(99, 238, 7, 7))
        image_list.append(self.imageGetter(108, 238, 7, 7))
        image_list.append(self.imageGetter(115, 238, 7, 7))
        image_list.append(self.imageGetter(123, 238, 7, 7))
        image_list.append(self.imageGetter(3, 246, 7, 7))
        image_list.append(self.imageGetter(11, 246, 7, 7))
        image_list.append(self.imageGetter(20, 246, 7, 7))
        image_list.append(self.imageGetter(27, 246, 7, 7))
        image_list.append(self.imageGetter(48, 248, 7, 7))

        image_list.append(self.imageGetter(68, 249, 6, 2))
        image_list.append(self.imageGetter(75, 247, 6, 6))



        character_string = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ -*'

        for character, image in zip(character_string, image_list):
            self.image_dict[character] = image


    def imageGetter(self, x, y, width, height):
        image = pygame.Surface([width, height])
        rect = image.get_rect()

        image.blit(self.spr_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey((92, 148, 252))
        image = pygame.transform.scale(image,
                                   (int(rect.width*2.9),
                                    int(rect.height*2.9)))
        return image


    def create_score_group(self):
        self.score_images = []
        self.create_label(self.score_images, '000000', 75, 55)


    def create_info_labels(self):
        self.mario_label = []
        self.world_label = []
        self.time_label = []
        self.stage_label = []


        self.create_label(self.mario_label, 'MARIO', 75, 30)
        self.create_label(self.world_label, 'WORLD', 450, 30)
        self.create_label(self.time_label, 'TIME', 625, 30)
        self.create_label(self.stage_label, '1-1', 472, 55)

        self.label_list = [self.mario_label,
                           self.world_label,
                           self.time_label,
                           self.stage_label]


    def create_load_screen_labels(self):
        world_label = []
        number_label = []

        self.create_label(world_label, 'WORLD', 280, 200)
        self.create_label(number_label, '1-1', 430, 200)

        self.center_labels = [world_label, number_label]


    def create_countdown_clock(self):
        self.count_down_images = []
        self.create_label(self.count_down_images, str(self.time), 645, 55)


    def create_label(self, label_list, string, x, y):
        for letter in string:
            label_list.append(Character(self.image_dict[letter]))

        self.set_label_rects(label_list, x, y)


    def set_label_rects(self, label_list, x, y):
        for i, letter in enumerate(label_list):
            letter.rect.x = x + ((letter.rect.width + 3) * i)
            letter.rect.y = y
            if letter.image == self.image_dict['-']:
                letter.rect.y += 7
                letter.rect.x += 2


    def create_coin_counter(self):
        self.coin_count_images = []
        self.create_label(self.coin_count_images, '*00', 300, 55)


    def create_flashing_coin(self):
        self.flashing_coin = flashing_coin.Coin(280, 53)


    def create_mario_image(self):
        self.life_times_image = self.imageGetter(75, 247, 6, 6)
        self.life_times_rect = self.life_times_image.get_rect(center=(378, 295))
        self.life_total_label = []
        self.create_label(self.life_total_label, str(self.total_lives),
                          450, 285)

        self.spr_sheet = setup.GFX['mario_bros']
        self.mario_image = self.imageGetter(178, 32, 12, 16)
        self.mario_rect = self.mario_image.get_rect(center=(320, 290))


    def create_game_over_label(self):
        game_label = []
        over_label = []

        self.create_label(game_label, 'GAME', 280, 300)
        self.create_label(over_label, 'OVER', 400, 300)

        self.game_over_label = [game_label, over_label]


    def create_time_out_label(self):
        time_out_label = []

        self.create_label(time_out_label, 'TIME OUT', 290, 310)
        self.time_out_label = [time_out_label]


    def create_main_menu_labels(self):
        player_one_game = []
        player_two_game = []
        top = []
        top_score = []

        self.create_label(player_one_game, '1 PLAYER GAME', 272, 360)
        self.create_label(player_two_game, '2 PLAYER GAME', 272, 405)
        self.create_label(top, 'TOP - ', 290, 465)
        self.create_label(top_score, '000000', 400, 465)

        self.main_menu_labels = [player_one_game, player_two_game,
                                 top, top_score]


    def update(self, level_info, mario=None):
        self.mario = mario
        self.handle_level_state(level_info)


    def handle_level_state(self, level_info):
        if self.state == csts.MAIN_MENU:
            self.score = level_info[csts.SCORE]
            self.update_score_images(self.score_images, self.score)
            self.update_score_images(self.main_menu_labels[3], self.top_score)
            self.update_coin_total(level_info)
            self.flashing_coin.update(level_info[csts.CURRENT_TIME])

        elif self.state == csts.LOAD_SCREEN:
            self.score = level_info[csts.SCORE]
            self.update_score_images(self.score_images, self.score)
            self.update_coin_total(level_info)

        elif self.state == csts.LEVEL:
            self.score = level_info[csts.SCORE]
            self.update_score_images(self.score_images, self.score)
            if level_info[csts.LEVEL_STATE] != csts.FROZEN \
                    and self.mario.state != csts.WALKING_TO_CASTLE \
                    and self.mario.state != csts.END_OF_LEVEL_FALL \
                    and not self.mario.dead:
                self.update_count_down_clock(level_info)
            self.update_coin_total(level_info)
            self.flashing_coin.update(level_info[csts.CURRENT_TIME])

        elif self.state == csts.TIME_OUT:
            self.score = level_info[csts.SCORE]
            self.update_score_images(self.score_images, self.score)
            self.update_coin_total(level_info)

        elif self.state == csts.GAME_OVER:
            self.score = level_info[csts.SCORE]
            self.update_score_images(self.score_images, self.score)
            self.update_coin_total(level_info)

        elif self.state == csts.FAST_COUNT_DOWN:
            level_info[csts.SCORE] += 50
            self.score = level_info[csts.SCORE]
            self.update_count_down_clock(level_info)
            self.update_score_images(self.score_images, self.score)
            self.update_coin_total(level_info)
            self.flashing_coin.update(level_info[csts.CURRENT_TIME])
            if self.time == 0:
                self.state = csts.END_OF_LEVEL

        elif self.state == csts.END_OF_LEVEL:
            self.flashing_coin.update(level_info[csts.CURRENT_TIME])


    def update_score_images(self, images, score):
        index = len(images) - 1

        for digit in reversed(str(score)):
            rect = images[index].rect
            images[index] = Character(self.image_dict[digit])
            images[index].rect = rect
            index -= 1


    def update_count_down_clock(self, level_info):
        if self.state == csts.FAST_COUNT_DOWN:
            self.time -= 1

        elif (level_info[csts.CURRENT_TIME] - self.current_time) > 400:
            self.current_time = level_info[csts.CURRENT_TIME]
            self.time -= 1
        self.count_down_images = []
        self.create_label(self.count_down_images, str(self.time), 645, 55)
        if len(self.count_down_images) < 2:
            for i in range(2):
                self.count_down_images.insert(0, Character(self.image_dict['0']))
            self.set_label_rects(self.count_down_images, 645, 55)
        elif len(self.count_down_images) < 3:
            self.count_down_images.insert(0, Character(self.image_dict['0']))
            self.set_label_rects(self.count_down_images, 645, 55)


    def update_coin_total(self, level_info):
        self.coin_total = level_info[csts.COIN_TOTAL]

        coin_string = str(self.coin_total)
        if len(coin_string) < 2:
            coin_string = '*0' + coin_string
        elif len(coin_string) > 2:
            coin_string = '*00'
        else:
            coin_string = '*' + coin_string

        x = self.coin_count_images[0].rect.x
        y = self.coin_count_images[0].rect.y

        self.coin_count_images = []

        self.create_label(self.coin_count_images, coin_string, x, y)


    def draw(self, surface):
        if self.state == csts.MAIN_MENU:
            self.draw_main_menu_info(surface)
        elif self.state == csts.LOAD_SCREEN:
            self.draw_loading_screen_info(surface)
        elif self.state == csts.LEVEL:
            self.draw_level_screen_info(surface)
        elif self.state == csts.GAME_OVER:
            self.draw_game_over_screen_info(surface)
        elif self.state == csts.FAST_COUNT_DOWN:
            self.draw_level_screen_info(surface)
        elif self.state == csts.END_OF_LEVEL:
            self.draw_level_screen_info(surface)
        elif self.state == csts.TIME_OUT:
            self.draw_time_out_screen_info(surface)
        else:
            pass



    def draw_main_menu_info(self, surface):
        for info in self.score_images:
            surface.blit(info.image, info.rect)

        for label in self.main_menu_labels:
            for letter in label:
                surface.blit(letter.image, letter.rect)

        for character in self.coin_count_images:
            surface.blit(character.image, character.rect)

        for label in self.label_list:
            for letter in label:
                surface.blit(letter.image, letter.rect)

        surface.blit(self.flashing_coin.image, self.flashing_coin.rect)


    def draw_loading_screen_info(self, surface):
        for info in self.score_images:
            surface.blit(info.image, info.rect)

        for word in self.center_labels:
            for letter in word:
                surface.blit(letter.image, letter.rect)

        for word in self.life_total_label:
            surface.blit(word.image, word.rect)

        surface.blit(self.mario_image, self.mario_rect)
        surface.blit(self.life_times_image, self.life_times_rect)

        for character in self.coin_count_images:
            surface.blit(character.image, character.rect)

        for label in self.label_list:
            for letter in label:
                surface.blit(letter.image, letter.rect)

        surface.blit(self.flashing_coin.image, self.flashing_coin.rect)


    def draw_level_screen_info(self, surface):

        for info in self.score_images:
            surface.blit(info.image, info.rect)

        for digit in self.count_down_images:
                surface.blit(digit.image, digit.rect)

        for character in self.coin_count_images:
            surface.blit(character.image, character.rect)

        for label in self.label_list:
            for letter in label:
                surface.blit(letter.image, letter.rect)

        surface.blit(self.flashing_coin.image, self.flashing_coin.rect)


    def draw_game_over_screen_info(self, surface):

        for info in self.score_images:
            surface.blit(info.image, info.rect)

        for word in self.game_over_label:
            for letter in word:
                surface.blit(letter.image, letter.rect)

        for character in self.coin_count_images:
            surface.blit(character.image, character.rect)

        for label in self.label_list:
            for letter in label:
                surface.blit(letter.image, letter.rect)

        surface.blit(self.flashing_coin.image, self.flashing_coin.rect)


    def draw_time_out_screen_info(self, surface):

        for info in self.score_images:
            surface.blit(info.image, info.rect)

        for word in self.time_out_label:
            for letter in word:
                surface.blit(letter.image, letter.rect)

        for character in self.coin_count_images:
            surface.blit(character.image, character.rect)

        for label in self.label_list:
            for letter in label:
                surface.blit(letter.image, letter.rect)

        surface.blit(self.flashing_coin.image, self.flashing_coin.rect)
