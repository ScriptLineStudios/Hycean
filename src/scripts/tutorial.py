import pygame
from pygame.locals import *
from pygame._sdl2 import Texture
from src.scripts.audio_handler import AudioHandler


class Tutorial:
    def __init__(self, renderer, app):
        self.renderer = renderer
        self.app = app

        self.font = pygame.font.Font('src/assets/yoster.ttf', 32)

        self.regular = (255, 255, 255)
        self.done = (0, 255, 0)
        
        self.texts = [
            'Press LMB to control spaceship',
            'Move Mouse to navigate',
            'Hold RMB or SHIFT to accelerate',
            'Click on computer to locate resources',
            'Tutorial finished, good job!'
        ]

        self.renderRegular = []
        self.renderDone = []

        self.crnt_task = 0

        self.done_anim = False
        self.done_time = 0
        self.done_frames = 30

        self.mp = pygame.Vector2(500, 400)
        self.total_motion = 0
        self.done_movement = 8000

        for text in self.texts:
            self.renderRegular.append(
                self.to_texture(
                self.font.render(text, False, self.regular))
            )
            
            self.renderDone.append(
                self.to_texture(
                self.font.render(text, False, self.done))
            )

        self.crnt_text = self.renderRegular[self.crnt_task]
        self.crnt_text_done = self.renderDone[self.crnt_task]
        self.text_rect = self.crnt_text.get_rect(center=(500, 700))

        self.finished = False

        self.success = AudioHandler.sounds['success']

    def to_texture(self, surface):
        return Texture.from_surface(
            self.renderer, surface
        )
    
    def completed_task(self):
        if not self.done_anim:
            self.done_anim = True
            self.success.play()

    def next_task(self):
        self.crnt_task += 1

        if self.crnt_task >= len(self.texts):
            self.finished = True
        else:
            self.crnt_text = self.renderRegular[self.crnt_task]
            self.crnt_text_done = self.renderDone[self.crnt_task]
            
            self.done_anim = False

        if self.crnt_task == 4:
            self.completed_task()
            self.done_time = 0
            self.done_frames = 60

    def update(self):
        if self.done_anim:
            if self.done_time < self.done_frames:
                self.done_time += 1
            else:
                self.done_anim = False
                self.done_time = 0
                self.next_task()

        if self.crnt_task == 3:
            if self.app.ui.computer_active:
                self.completed_task()

    def draw(self):
        if not self.finished:
            self.update()

            if self.done_anim:
                self.crnt_text_done.draw(srcrect=None, dstrect=self.text_rect)
            else:
                self.crnt_text.draw(srcrect=None, dstrect=self.text_rect)

    def handle_event(self, event):
        if event.type == MOUSEMOTION:
            if self.crnt_task == 1:
                movement = event.pos - self.mp
                self.total_motion += movement.length()

                if self.total_motion > self.done_movement:
                    self.completed_task()

                self.mp = pygame.Vector2(event.pos)

        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.crnt_task == 0:
                    self.completed_task()

            if event.button == 3:
                if self.crnt_task == 2:
                    self.completed_task()
            
        if event.type == KEYDOWN:
            if event.key == K_LSHIFT:
                if self.crnt_task == 2:
                    self.completed_task()