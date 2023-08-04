import pygame
import pygame._sdl2
#from pygame._sdl2 import Window, Renderer
from pygame.locals import *

from src.scripts.states import *

pygame.init()

class App:
    def __init__(self):
        self.ScreenSize = (1000, 800)
        caption = 'Hycean'
        
        self.window = pygame._sdl2.Window(caption, self.ScreenSize, opengl=True)
        self.renderer = pygame._sdl2.Renderer(self.window)

        self.states = {
            #'main_menu': Menu()
            'space': Space(self.renderer),
            'ocean': Ocean(self.renderer),
        }

        self.crnt_state = 'ocean'
        self.state = self.states[self.crnt_state]

        self.clock = pygame.time.Clock()
        self.fps = 60

    def run(self):
        renderer = self.renderer
        while True:
            self.clock.tick(self.fps)

            self.state.update()
            for event in pygame.event.get():
                self.state.handle_event(event)
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit

            renderer.draw_color = (255, 255, 255, 255)
            renderer.clear()

            self.state.render()

            renderer.present()
            self.window.title = f'Game Title FPS: {round(self.clock.get_fps())}'