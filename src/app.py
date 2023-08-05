import pygame
import pygame._sdl2
#from pygame._sdl2 import Window, Renderer
from pygame.locals import *

from src.scripts.states import *
import pygame_shaders

pygame.init()

class App:
    def __init__(self):
        self.ScreenSize = (1000, 800)
        caption = 'Hycean - Space'
        
        self.window = pygame._sdl2.Window(caption, self.ScreenSize, borderless=False, opengl=False)
        self.renderer = pygame._sdl2.Renderer(self.window)

        self.display = pygame.display.set_mode((1000, 800))

        self.states = {
            #'main_menu': Menu()
            'space': Space(self, self.renderer),
            'ocean': Ocean(self, None ),
        }

        self.crnt_state = 'space'
        self.state = self.states[self.crnt_state]
        self.state.start()
        
        self.clock = pygame.time.Clock()
        self.fps = 60

    def run(self):
        renderer = self.state.renderer
        while True:
            self.clock.tick(self.fps)

            self.state.update()
            for event in pygame.event.get():
                self.state.handle_event(event)
                if event.type == QUIT:
                    pygame.quit()
                    raise SystemExit

            if self.crnt_state == "space":
                renderer.draw_color = (255, 255, 255, 255)
                renderer.clear()

            self.state.render()

            if self.crnt_state == "space":
                renderer.present()
                try:
                    self.state.window.title = f'Game Title FPS: {round(self.clock.get_fps())}'      
                except:
                    self.window.title = f'Game Title FPS: {round(self.clock.get_fps())}'      
            else:
                pygame.display.flip()