from .state import State

import pygame
from pygame.locals import *
from pygame._sdl2 import Texture
from src.scripts.audio_handler import AudioHandler

pygame.font.init()


# make separate class for 3D and 2D part of the game
class Victory(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ScreenSize = (1000, 800)

        self.mp = pygame.Vector2(500, 400)

        self.grey = pygame.Color('grey')

        self.titleFont = pygame.font.Font('src/assets/yoster.ttf', 96)
        self.title = self.titleFont.render('Congratulations!', False, (255, 255, 0))
        self.title = self.to_texture(self.title)
        self.titleRect = self.title.get_rect(center=(500, 75))

        self.font = pygame.font.Font('src/assets/yoster.ttf', 32)

        self.play_time = 0 #seconds
        self.clicked = 0
        self.mouse_movement = 0 #depends on dpi

        self.render_text()

    def to_texture(self, surface):
        return Texture.from_surface(
            self.renderer, surface
        )

    def render_text(self):
        self.playtimeText = self.font.render(f'Your playtime: {self.play_time // 60} minutes', False, self.grey)
        self.playtimeText = self.to_texture(self.playtimeText)
        self.playtimeRect = self.playtimeText.get_rect(topleft=(50, 150))

        self.clickedText = self.font.render(f'You have clicked {self.clicked} times', False, self.grey)
        self.clickedText = self.to_texture(self.clickedText)
        self.clickedRect = self.clickedText.get_rect(topleft=(50, 225))

        movement = self.mouse_movement // 100 # cm
        movement //= 100 # meters
        self.mouseText = self.font.render(f'You moved your mouse {self.mouse_movement} meters', False, self.grey)
        self.mouseText = self.to_texture(self.mouseText)
        self.mouseRect = self.mouseText.get_rect(topleft=(50, 300))

    def update_time(self):
        self.play_time += self.get_dt()

    def get_dt(self):
        fps = self.app.clock.get_fps()

        if fps == 0:
            return 0
        
        return 1 / fps

    def render(self):
        self.renderer.draw_color = (0, 0, 0, 255)
        self.renderer.clear()

        self.title.draw(srcrect=None, dstrect=self.titleRect)

        self.playtimeText.draw(srcrect=None, dstrect=self.playtimeRect)
        self.clickedText.draw(srcrect=None, dstrect=self.clickedRect)
        self.mouseText.draw(srcrect=None, dstrect=self.mouseRect)

    def handle_event(self, event):
        if event.type == MOUSEMOTION:
            length = (self.mp - event.pos).magnitude()
            self.mp.update(event.pos)
            self.mouse_movement += length

        if event.type == KEYDOWN:
            self.clicked += 1

        if event.type == MOUSEBUTTONDOWN:
            self.clicked += 1
                    