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

        self.states = {
            #'main_menu': Menu()
            'space': Space(self, self.renderer),
            'ocean': Ocean(self, self.renderer),
            'game_over': GameOver(self, self.renderer)
        }

        self.crnt_state = 'space'
        self.state = self.states[self.crnt_state]
        self.state.start()
        #self.state.stop()

        #self.crnt_state = 'space'
        #self.state = self.states[self.crnt_state]
        #self.state.start()
        
        #self.crnt_state = 'ocean'
        #self.state = self.states[self.crnt_state]
        #self.state.start()

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
                
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        self.crnt_state = 'game_over'
                        self.state = self.states[self.crnt_state]
                        self.state.update_screen()

            renderer.draw_color = (255, 255, 255, 255)
            renderer.clear()

            self.state.render()

            renderer.present()
            try:
                self.state.window.title = f'Game Title FPS: {round(self.clock.get_fps())}'      
            except:
                self.window.title = f'Game Title FPS: {round(self.clock.get_fps())}'      