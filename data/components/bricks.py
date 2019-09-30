import pygame
from .. import setup
from .. import csts
from . import powerups
from . import coin


class Brick(pygame.sprite.Sprite):
    def __init__(self, x, y, contents=None, powerup_group=None, name='brick'):
        pygame.sprite.Sprite.__init__(self)
        self.spr_sheet = setup.GFX['tile_set']

        self.frames = []
        self.frame_index = 0
        self.setup_frames()
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.mask = pygame.mask.from_surface(self.image)
        self.bumped_up = False
        self.rest_height = y
        self.state = csts.RESTING
        self.y_vel = 0
        self.gravity = 1.2
        self.name = name
        self.contents = contents
        self.setup_contents()
        self.group = powerup_group
        self.powerup_in_box = True


    def imageGetter(self, x, y, width, height):
        """Extracts the image from the sprite sheet"""
        image = pygame.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.spr_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(csts.BLACK)
        image = pygame.transform.scale(image,
                                   (int(rect.width*csts.BRICK_SIZE_MULTIPLIER),
                                    int(rect.height*csts.BRICK_SIZE_MULTIPLIER)))
        return image


    def setup_frames(self):
        self.frames.append(self.imageGetter(16, 0, 16, 16))
        self.frames.append(self.imageGetter(432, 0, 16, 16))


    def setup_contents(self):
        if self.contents == '6coins':
            self.coin_total = 6
        else:
            self.coin_total = 0


    def update(self):
        self.standHandlers()


    def standHandlers(self):
        if self.state == csts.RESTING:
            self.resting()
        elif self.state == csts.BUMPED:
            self.bumped()
        elif self.state == csts.OPENED:
            self.opened()


    def resting(self):
        if self.contents == '6coins':
            if self.coin_total == 0:
                self.state == csts.OPENED


    def bumped(self):
        self.rect.y += self.y_vel
        self.y_vel += self.gravity

        if self.rect.y >= (self.rest_height + 5):
            self.rect.y = self.rest_height
            if self.contents == 'star':
                self.state = csts.OPENED
            elif self.contents == '6coins':
                if self.coin_total == 0:
                    self.state = csts.OPENED
                else:
                    self.state = csts.RESTING
            else:
                self.state = csts.RESTING


    def start_bump(self, score_group):
        self.y_vel = -6

        if self.contents == '6coins':
            setup.SFX['coin'].play()

            if self.coin_total > 0:
                self.group.add(coin.Coin(self.rect.centerx, self.rect.y, score_group))
                self.coin_total -= 1
                if self.coin_total == 0:
                    self.frame_index = 1
                    self.image = self.frames[self.frame_index]
        elif self.contents == 'star':
            setup.SFX['powerup_appears'].play()
            self.frame_index = 1
            self.image = self.frames[self.frame_index]

        self.state = csts.BUMPED


    def opened(self):
        self.frame_index = 1
        self.image = self.frames[self.frame_index]

        if self.contents == 'star' and self.powerup_in_box:
            self.group.add(powerups.Star(self.rect.centerx, self.rest_height))
            self.powerup_in_box = False


class BrickPiece(pygame.sprite.Sprite):
    def __init__(self, x, y, xvel, yvel):
        super(BrickPiece, self).__init__()
        self.spr_sheet = setup.GFX['item_objects']
        self.setup_frames()
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.x_vel = xvel
        self.y_vel = yvel
        self.gravity = .8


    def setup_frames(self):
        self.frames = []

        image = self.imageGetter(68, 20, 8, 8)
        reversed_image = pygame.transform.flip(image, True, False)

        self.frames.append(image)
        self.frames.append(reversed_image)


    def imageGetter(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        rect = image.get_rect()

        image.blit(self.spr_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(csts.BLACK)
        image = pygame.transform.scale(image,
                                   (int(rect.width*csts.BRICK_SIZE_MULTIPLIER),
                                    int(rect.height*csts.BRICK_SIZE_MULTIPLIER)))
        return image


    def update(self):
        self.rect.x += self.x_vel
        self.rect.y += self.y_vel
        self.y_vel += self.gravity
        self.check_if_off_screen()

    def check_if_off_screen(self):
        if self.rect.y > csts.scr_height:
            self.kill()
