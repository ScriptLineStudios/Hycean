import pygame
import pygame._sdl2
#from pygame._sdl2 import Window, Renderer
from pygame.locals import *

from src.scripts.audio_handler import AudioHandler
from src.scripts.states import *
from src.scripts.ui import *


import pygame_shaders

pygame.init()

class App:
    def __init__(self):
        self.needed_resources = {
            "Aluminum": 100,
            "Fiber": 40,
            "Titanium": 70,
            "Bronze": 60,
            "Steel": 15,
            "Silver": 20,
        }

        self.needed_resources_stable = {
            "Aluminum": 100,
            "Fiber": 40,
            "Titanium": 70,
            "Bronze": 60,
            "Steel": 15,
            "Silver": 20,
        }

        self.ScreenSize = (1000, 800)
        caption = 'Hycean - Space'
        
        self.window = pygame._sdl2.Window(caption, self.ScreenSize, borderless=False, opengl=False)
        self.renderer = pygame._sdl2.Renderer(self.window)


        self.states = {
            'main_menu': Menu(self, self.renderer),
            'space': Space(self, self.renderer),
            "ocean": Ocean(self, self.renderer, material="Silver"),
            'game_over': GameOver(self, self.renderer)
        }

        self.crnt_state = 'main_menu'
        self.state = self.states[self.crnt_state]
        self.state.start()

        self.ui = UI(self, self.renderer)

        self.registered_matreials = []

        self.clock = pygame.time.Clock()
        self.fps = 60

    def run(self):
        renderer = self.state.renderer
        while True:
            self.clock.tick(self.fps)

            self.state.update()
            for event in pygame.event.get():
                self.state.handle_event(event)
                self.ui.events(event)
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit

            renderer.draw_color = (255, 255, 255, 255)
            renderer.clear()

            self.state.render()

            if self.crnt_state != "game_over" and self.crnt_state != "main_menu":
                self.ui.render()

            renderer.present()
            try:
                self.state.window.title = f'Game Title FPS: {round(self.clock.get_fps())}'      
            except:
                self.window.title = f'Game Title FPS: {round(self.clock.get_fps())}'      