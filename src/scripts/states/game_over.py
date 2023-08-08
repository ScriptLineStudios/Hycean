from .state import State
from src.scripts.audio_handler import AudioHandler

from random import randint, choice
from string import ascii_letters

import pygame
from pygame.locals import KEYDOWN, K_r, K_SPACE, K_KP_ENTER
from pygame._sdl2 import Texture
from json import load


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
        self.restartRect = self.restartText.get_rect(center = (500, 650))
        
        self.restart = False
        self.RestartAnim = False
        self.scale = 1.0
        self.maxScale = 1.2
        self.speed = 0.05

        with open('src/assets/GameOverRandom.json', 'r') as file:
            self.listText = load(file)['sentences'][:-1]

        self.RestartSound = AudioHandler.sounds['restart']

        self.first_time = True

        self.controls = self.to_texture(pygame.image.load('src/assets/controls.png'))

        self.update_screen()

    def render(self):
        self.texture.draw()

        self.game_over.draw(srcrect=None, dstrect=self.game_over_rect)
        self.asteroid_render.draw(srcrect=None, dstrect=self.asteroid_rect)

        self.randomRender.draw(srcrect=None, dstrect=self.rndRenderRect)

        if self.RestartAnim:
            if self.scale < self.maxScale: 
                self.scale += self.speed
            else:
                self.RestartAnim = False
        else:
            if self.scale > 1:
                self.scale -= self.speed
            else:
                if self.restart:
                    self.restart_space()

        scaledRestart = self.restartRect.copy()
        scaledRestart.width *= self.scale
        scaledRestart.height *= self.scale
        scaledRestart.center = self.restartRect.center

        self.restartText.draw(srcrect=None, dstrect=scaledRestart)

    def show_tutorial(self):
        if self.first_time:
            self.controls.draw(srcrect=None, dstrect=None)

    def restart_space(self):
        # RESTART SPACE STATE
        app = self.app
        app.state.stop()
        app.crnt_state = 'space'
        app.state = app.states[app.crnt_state]
        app.state.start()
        app.state.restart()

    def to_texture(self, surface):
        return Texture.from_surface(
            self.renderer, surface
        )

    def update_screen(self):
        # RESTARTS GAME OVER SCREEN
        self.surface = self.renderer.to_surface()
        self.surface = pygame.transform.gaussian_blur(self.surface, 4)
        self.surface = pygame.transform.grayscale(self.surface)

        self.texture = self.to_texture(self.surface)

        self.asteroid_name = f'{choice(ascii_letters).upper()}-{randint(100, 999)}'
        self.asteroid_text = f'Asteroid {self.asteroid_name} Hit Your Ship'
        self.asteroid_render = self.font.render(self.asteroid_text, False, (160, 130, 0))
        self.asteroid_render = self.to_texture(self.asteroid_render)
        self.asteroid_rect = self.asteroid_render.get_rect(center = (500, 180))

        randomText = choice(self.listText)
        self.randomRender = self.font.render(randomText, False, (240, 240, 0))
        self.randomRender = self.to_texture(self.randomRender)
        self.rndRenderRect = self.randomRender.get_rect(center = (500, 400))

        self.RestartAnim = False
        self.scale = 1.0
        self.maxScale = 1.2
        self.speed = 0.05

        self.restart = False

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key in [K_r, K_SPACE, K_KP_ENTER]:
                self.RestartSound.play()
                self.RestartAnim = True
                self.restart = True