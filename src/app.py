import pygame
import pygame._sdl2
#from pygame._sdl2 import Window, Renderer
from pygame.locals import *

from src.scripts.audio_handler import AudioHandler
from src.scripts.states import *
from src.scripts.ui import *
from src.scripts.mouse import Mouse

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

        self.collected_materials = {
            "Aluminum": 0,
            "Fiber": 0,
            "Titanium": 0,
            "Bronze": 0,
            "Steel": 0,
            "Silver": 0,
        }

        self.ScreenSize = (1000, 800)
        caption = 'Hycean'

        self.current_resource = "Aluminum"
        
        self.window = pygame._sdl2.Window(caption, self.ScreenSize, borderless=False, opengl=False, fullscreen=False)
        self.renderer = pygame._sdl2.Renderer(self.window)

        self.oceans = {}

        self.states = {
            'main_menu': Menu(self, self.renderer),
            'space': Space(self, self.renderer),
            "ocean": Ocean(self, self.renderer, color="red", material="Aluminum"),
            'game_over': GameOver(self, self.renderer),
            'victory': Victory(self, self.renderer)
        }

        self.crnt_state = 'ocean'
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

            for event in pygame.event.get():
                self.state.handle_event(event)
                self.states['victory'].handle_event(event)
                Mouse.handle_event(event)
                self.ui.events(event)

                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit

            self.state.update()
            Mouse.update()

            renderer.draw_color = (255, 255, 255, 255)
            renderer.clear()

            self.state.render()

            if not self.crnt_state in ["game_over", "main_menu", "victory"]:
                self.ui.render()

            renderer.present()
            self.window.title = str(self.clock.get_fps())
