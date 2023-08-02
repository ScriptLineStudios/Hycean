import pygame
import pygame._sdl2
#from pygame._sdl2 import Window, Renderer
from pygame.locals import *

from src.scripts.states import *

pygame.init()


class App:
    def __init__(self, fps):
        self.ScreenSize = (960, 540)
        caption = 'Game Title'
        
        self.window = pygame._sdl2.Window(caption, self.ScreenSize)
        self.renderer = pygame._sdl2.Renderer(self.window)

        self.states = {
            #'main_menu': Menu()
            'game': Game(),
        }

        self.crnt_state = 'game'
        self.state = self.states[self.crnt_state]

        self.clock = pygame.time.Clock()
        self.fps = fps

    def run(self):
        renderer = self.renderer
        while True:
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit

            renderer.draw_color = (255, 255, 255, 255)
            renderer.clear()

            self.state.update()
            self.state.render(renderer)

            renderer.present()
            self.window.title = f'Game Title FPS: {round(self.clock.get_fps())}'