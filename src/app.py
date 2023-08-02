import pygame
import pygame._sdl2
#from pygame._sdl2 import Window, Renderer
from pygame.locals import *

from src.scripts.states import *

pygame.init()

class App:
    def __init__(self, fps):
        self.ScreenSize = (1000, 800)
        caption = 'Game Title'
        
        self.window = pygame._sdl2.Window(caption, self.ScreenSize)
        self.renderer = pygame._sdl2.Renderer(self.window)

        self.states = {
            #'main_menu': Menu()
            'space': Space(self.renderer),
            # 'ocean': Ocean(),
        }

        self.crnt_state = 'space'
        self.state = self.states[self.crnt_state]

        self.clock = pygame.time.Clock()
        self.fps = 120

    def run(self):
        renderer = self.renderer
        while True:
            self.clock.tick(self.fps)

            for event in pygame.event.get():
                self.state.handle_event(event)
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit

            renderer.draw_color = (255, 255, 255, 255)
            renderer.clear()

            self.state.update()
            self.state.render()

            renderer.present()
            self.window.title = f'Game Title FPS: {round(self.clock.get_fps())}'