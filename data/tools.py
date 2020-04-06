"""
tools.py
This file contains the core tools that are needed to execute the game and run it. 
"""

import os
import pygame

keybinding = {
    'action':pygame.K_s,
    'jump':pygame.K_a,
    'left':pygame.K_LEFT,
    'right':pygame.K_RIGHT,
    'down':pygame.K_DOWN
}

class Control(object):
    """
    This is the "Control" class for entire project. Contains the game loop, and contains
    the event_loop which passes events to States as needed. Logic for flipping
    states is also found here.
    """

    def __init__(self, caption):
        """
        The constructor for the Control class.
        Sets attributes to their default values.

        Parameters:
            caption (string): This is the window caption, or what will be displayed at the top of the window. 
        """
        self.screen = pygame.display.get_surface()
        self.done = False
        self.clock = pygame.time.Clock()
        self.caption = caption
        self.fps = 60
        self.show_fps = False
        self.current_time = 0.0
        self.keys = pygame.key.get_pressed()
        self.state_dict = {}
        self.state_name = None
        self.state = None

    def setup_states(self, state_dict, start_state):
        """
        The function to set the gamestate. 

        Parameters:
            state_dict: Dictionary containing all the gamestates.
            start_state: Name of gamestate to switch to.
        """
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]

    def update(self):
        """
        The function to update the game. Runs every frame.

        if GAMESTATE == QUIT:
            DONE = TRUE
        ELSE IF GAMESTATE == DONE:
            GO TO NEXT GAMESTATE
        
        UPDATE STATE
        """
        self.current_time = pygame.time.get_ticks()
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(self.screen, self.keys, self.current_time)

    def flip_state(self):
        """
        The function to "flip the gamestate" or in other words, switch to the next state.
        Sets the state_name to the next state, and indexes the state_dict in order to set the state.
        """
        previous = self.state_name
        self.state_name = self.state.next
        persist = self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.current_time, persist)
        self.state.previous = previous


    def event_loop(self):
        """
        The function to loop events with the pygame module.
        Checks every frame for key actions.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            elif event.type == pygame.KEYDOWN:
                self.keys = pygame.key.get_pressed()
                self.toggle_show_fps(event.key)
            elif event.type == pygame.KEYUP:
                self.keys = pygame.key.get_pressed()
            self.state.get_event(event)


    def toggle_show_fps(self, key):
        """
        The function to toggle FPS if the pressed key is F5.
        
        Parameters:
            key: ASCII value of key. Accessed using pygame.key.
        """
        if key == pygame.K_F5:
            self.show_fps = not self.show_fps
            if not self.show_fps:
                pygame.display.set_caption(self.caption)


    def main(self):
        """
        The main loop of the program.
        In the form of a while loop, continues to execute the event_loop and update loop every frame while self.done is true.
        """
        while not self.done:
            self.event_loop()
            self.update()
            pygame.display.update()
            self.clock.tick(self.fps)
            if self.show_fps:
                fps = self.clock.get_fps()
                with_fps = "{} - {:.2f} FPS".format(self.caption, fps)
                pygame.display.set_caption(with_fps)


class GameState_Initialize(object):
    """
    This class initializes a game state. 
    """
    def __init__(self):
        self.start_time = 0.0
        self.current_time = 0.0
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.persist = {}

    def get_event(self, event):
        pass

    def startup(self, current_time, persistant):
        self.persist = persistant
        self.start_time = current_time

    def cleanup(self):
        self.done = False
        return self.persist

    def update(self, surface, keys, current_time):
        pass

def Gfx_LoadIntoRAM(directory, colorkey=(255,0,255), accept=('.png', 'jpg', 'bmp')):
    """
    Loads all graphics in the resource folder into RAM for the game to use. 

    Parameters:
        directory (string): String containing the directory of the assets.

    Returns:
        graphics: An array containing each graphic file.
    """
    graphics = {}
    for pic in os.listdir(directory):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(directory, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
                img.set_colorkey(colorkey)
            graphics[name]=img
    return graphics


def Music_LoadIntoRAM(directory, accept=('.wav', '.mp3', '.ogg', '.mdi')):
    """
    Loads all music in the resource folder into RAM for the game to use.

    Parameters:
        directory (string): String containing the directory of the music files.
    
    Returns:
        songs: An array containing each music file.
    """
    songs = {}
    for song in os.listdir(directory):
        name,ext = os.path.splitext(song)
        if ext.lower() in accept:
            songs[name] = os.path.join(directory, song)
    return songs


def Fonts_LoadIntoRAM(directory, accept=('.ttf')):
    """
    Loads all fonts in the resource folder into RAM for the game to use.

    Parameters:
        directory (string): String containing the directory of the music files.
    
    Returns:
        fonts: An array containing each font file.
    """
    fonts = {}
    for font in os.listdir(directory):
        name, ext = os.path.splitext(font)
        if ext.lower() in accept:
            fonts[name] = os.path.join(directory, font)
    return fonts


def Sfx_LoadIntoRAM(directory, accept=('.wav','.mpe','.ogg','.mdi')):
    """
    Loads all sound effects in the resource folder into RAM for the game to use.

    Parameters:
        directory (string): String containing the directory of the audio files.

    Returns:
        sounds: An array containing each sound file.
    """
    sounds = {}
    for effects in os.listdir(directory):
        name, ext = os.path.splitext(effects)
        if ext.lower() in accept:
            sounds[name] = pygame.mixer.Sound(os.path.join(directory, effects))
    return sounds
