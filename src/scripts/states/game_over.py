from .state import State

from random import randint, choice
from string import ascii_letters

import pygame
from pygame.locals import KEYDOWN, K_r, K_SPACE, K_KP_ENTER
from pygame._sdl2 import Texture
pygame.font.init()


class GameOver(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title_font = pygame.font.Font('src/assets/yoster.ttf', 96)
        self.font = pygame.font.Font('src/assets/yoster.ttf', 30)

        self.game_over = self.title_font.render('GAME OVER!', False, (100, 100, 100))
        self.game_over = self.to_texture(self.game_over)
        self.game_over_rect = self.game_over.get_rect(center = (500, 130))
        
        self.restartText = self.font.render(
            'Press R to Restart, Captain!', 
            False, (255, 0, 0)
        )
        self.restartText = self.to_texture(self.restartText)
        self.restartRect = self.restartText.get_rect(center = (500, 550))
        
        self.restart = False
        self.RestartAnim = False
        self.scale = 1.0
        self.maxScale = 1.2
        self.speed = 0.05

        self.black_screen = self.to_texture(pygame.Surface((1000, 800)))
        self.opacityAnim = False 
        self.opacity = 0
        self.alphaSpeed = 5
        self.maxAlpha = 255

        self.update_screen()

    def render(self):
        self.texture.draw()

        self.game_over.draw(srcrect=None, dstrect=self.game_over_rect)
        self.asteroid_render.draw(srcrect=None, dstrect=self.asteroid_rect)

        if self.RestartAnim:
            if self.scale < self.maxScale: 
                self.scale += self.speed
            else:
                self.RestartAnim = False
        else:
            if self.scale > 1:
                self.scale -= self.speed

        if self.opacityAnim:
            if self.opacity > self.maxAlpha:
                self.opacity += self.alphaSpeed
            else:
                self.restart = True
                print('change state to space on main')

        scaledRestart = self.restartRect.copy()
        scaledRestart.width *= self.scale
        scaledRestart.height *= self.scale
        scaledRestart.center = self.restartRect.center

        self.restartText.draw(srcrect=None, dstrect=scaledRestart)
        
        #self.black_screen.alpha = self.opacity
        #self.black_screen.draw()
    
    def to_texture(self, surface):
        return Texture.from_surface(
            self.renderer, surface
        )

    def update_screen(self):
        self.surface = self.renderer.to_surface()
        self.surface = pygame.transform.gaussian_blur(self.surface, 4)
        self.surface = pygame.transform.grayscale(self.surface)

        self.texture = self.to_texture(self.surface)

        self.asteroid_name = f'{choice(ascii_letters).upper()}-{randint(100, 999)}'
        self.asteroid_text = f'Asteroid {self.asteroid_name} Hit Your Ship'
        self.asteroid_render = self.font.render(self.asteroid_text, False, (160, 130, 0))
        self.asteroid_render = self.to_texture(self.asteroid_render)
        self.asteroid_rect = self.asteroid_render.get_rect(center = (500, 180))

        self.RestartAnim = False
        self.scale = 1.0
        self.maxScale = 1.2
        self.speed = 0.05
        
        self.opacity = 0
        self.alphaSpeed = 5
        self.maxAlpha = 255

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key in [K_r, K_SPACE, K_KP_ENTER]:
                self.RestartAnim = True