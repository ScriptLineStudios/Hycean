from .state import State

from random import choice, randint

import pygame
from pygame.locals import *
from pygame._sdl2 import Texture
from src.scripts.audio_handler import AudioHandler
from src.scripts.mouse import Mouse

pygame.font.init()


# make separate class for 3D and 2D part of the game
class Menu(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ScreenSize = (1000, 800)

        self.background = self.to_texture(
            pygame.image.load('src/assets/Space Background.png')
        )

        fontPath = 'src/assets/yoster.ttf'
        titleFont = pygame.font.Font('src/assets/prstartk.ttf', 112)
        font = pygame.font.Font(fontPath, 64)
        self.smallFont = pygame.font.Font(fontPath, 32)

        self.title = titleFont.render('HYCEAN', False, (255, 255, 255))
        self.titleRect = self.title.get_rect(center=(500, 130))

        self.logo = pygame.image.load("src/assets/logo.png")
        self.logo = self.to_texture(self.logo)
        self.logo_rect = self.logo.get_rect()
        self.logo_rect.width *= 0.8
        self.logo_rect.height *= 0.8
        self.logo_rect.center = (500, 100)
        self.play_text = font.render('PLAY!', False, (100, 100, 100))
        self.play_text = self.to_texture(self.play_text)
        self.play_text_green = font.render('PLAY!', False, (0, 255, 0))
        self.play_text_green = self.to_texture(self.play_text_green)

        self.play_rect = self.play_text.get_rect(center=(500, 650))

        self.press_space = self.smallFont.render('press SPACE to:', False, (70, 70, 70))
        self.press_space = self.to_texture(self.press_space)
        self.press_rect = self.press_space.get_rect(centerx=self.play_rect.centerx)
        self.press_rect.bottom = self.play_rect.top

        self.mp = (0, 0)

        self.switch = False
        self.scale_anim = False
        self.scale = 1.0
        self.maxScale = 1.2
        self.speed = 0.03

        self.scale_anim_audio = False
        self.scale_audio = 1.0
        self.maxScaleAudio = 1.15
        self.speedAudio = 0.05

        self.anim_wait = 0.25 #seconds

        titleMask = pygame.mask.from_surface(self.title)
        self.bebra = self.to_texture(titleMask.to_surface())
        images = [
            pygame.image.load('src/assets/stars/star1.png'),
            pygame.image.load('src/assets/stars/star2.png'),
            pygame.image.load('src/assets/stars/star3.png'),
            pygame.image.load('src/assets/stars/star4.png'),
            pygame.image.load('src/assets/stars/star5.png'),
        ]

        starTextures = []
        for image in images:
            starTextures.append(self.to_texture(image))

        self.stars = []
        starCount = 3500
        for star in range(starCount):
            position = (
                randint(0, self.titleRect.width - 1),
                randint(0, self.titleRect.height -1)
            )
            velocity = pygame.Vector2(0, 0)

            if titleMask.get_at(position):
                centerPos = [
                    position[0] + self.titleRect.left,
                    position[1] + self.titleRect.top
                ]
                random_pos = pygame.Vector2(
                    randint(0, 1000), randint(0, 800)
                )
                self.stars.append([random_pos, centerPos, velocity, choice(starTextures)])

        self.volume = 0.5

        self.volume_text = f'A - {self.volume} - D'
        self.volume_render = self.smallFont.render(self.volume_text, False, (100, 100, 100))
        self.volume_render = self.to_texture(self.volume_render)
        self.volume_rect = self.volume_render.get_rect(center=(500, 750))
        
        self.volume_txt_render = self.smallFont.render('volume:', False, (100, 100, 100))
        self.volume_txt_render = self.to_texture(self.volume_txt_render)
        self.volume_txt_rect = self.volume_render.get_rect(centerx=self.volume_rect.centerx)
        self.volume_txt_rect.bottom = self.volume_rect.top
        
        #sound to test the volume

        self.feedback_sound = AudioHandler.sounds['volume_feedback']

        self.play_sound = AudioHandler.sounds['play']

        #indicate when game run
        #self.play_sound = pygame.mixer.Sound()

    def to_texture(self, surface):
        return Texture.from_surface(
            self.renderer, surface
        )

    def update(self):
        pass
    
    def switch_space(self):
        app = self.app
        app.crnt_state = 'space'
        app.state = app.states[app.crnt_state]

    def get_dt(self):
        fps = self.app.clock.get_fps()

        if fps == 0:
            return 0
        
        return 1 / fps

    def render(self):
        self.renderer.draw_color = (0, 0, 0, 255)
        self.renderer.clear()

        self.background.draw()

        starRect = self.stars[0][3].get_rect()
        starRect.width *= 0.3
        starRect.height *= 0.3

        if self.anim_wait > 0:
            self.anim_wait -= self.get_dt()

        for star in self.stars:
            starRect.center = star[0]

            if self.anim_wait < 0:
                difference = star[1] - star[0]

                star[0] += difference * 0.075

            star[3].draw(srcrect=None, dstrect=starRect)

        #self.logo.draw(srcrect=None, dstrect=self.logo_rect)
        #self.renderer.blit(self.to_texture(self.logo), pygame.Rect(75, 10, 1111 / 1.3, 248 / 1.3))

        if self.scale_anim:
            if self.scale < self.maxScale: 
                self.scale += self.speed
            else:
                self.scale_anim = False
        else:
            if self.scale > 1:
                self.scale -= self.speed
            else:
                if self.switch:
                    self.switch_space()

        if self.scale_anim_audio:
            if self.scale_audio < self.maxScaleAudio: 
                self.scale_audio += self.speedAudio
            else:
                self.scale_anim_audio = False
        else:
            if self.scale_audio > 1:
                self.scale_audio -= self.speedAudio


        scaledPlay = self.play_rect.copy()
        scaledPlay.width *= self.scale
        scaledPlay.height *= self.scale
        scaledPlay.center = self.play_rect.center

        self.press_rect.bottom = scaledPlay.top

        self.play_text.draw(srcrect=None, dstrect=scaledPlay)
        
        if scaledPlay.collidepoint(self.mp):
            self.play_text_green.draw(srcrect=None, dstrect=scaledPlay)
            Mouse.hovered = True
        
        self.press_space.draw(srcrect=None, dstrect=self.press_rect)

        scaledAudio = self.volume_rect.copy()
        scaledAudio.width *= self.scale_audio
        scaledAudio.height *= self.scale_audio
        scaledAudio.center = self.volume_rect.center

        self.volume_render.draw(srcrect=None, dstrect=scaledAudio)
        self.volume_txt_render.draw(srcrect=None, dstrect=self.volume_txt_rect)
        
    def play(self):
        app = self.app
        app.crnt_state = 'space'
        app.state = app.states[app.crnt_state]

    def update_volume(self, value):
        self.volume += value
        self.volume = round(self.volume, 2)
        if self.volume < 0:
            self.volume = 0.0
        if self.volume > 1:
            self.volume = 1.0

        self.volume_text = f'A - {self.volume} - D'
        self.volume_render = self.smallFont.render(self.volume_text, False, (100, 100, 100))
        self.volume_render = self.to_texture(self.volume_render)
        self.volume_rect = self.volume_render.get_rect(center=(500, 750))

        AudioHandler.set_volume(self.volume)

        pygame.mixer.music.set_volume(self.volume / 3)

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key in [K_SPACE, K_RETURN]:
                self.play_sound.play()
                self.scale_anim = True
                self.switch = True

            if event.key == K_a:
                self.scale_anim_audio = True
                self.update_volume(-0.1)
                self.feedback_sound.play()

            if event.key == K_d:
                self.scale_anim_audio = True
                self.update_volume(0.1)
                self.feedback_sound.play()

            if event.key == K_ESCAPE:
                pygame.quit()
                raise SystemExit

        if event.type == MOUSEMOTION:
            self.mp = event.pos
                    
        if event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                if Mouse.hovered:
                    self.play_sound.play()
                    self.scale_anim = True
                    self.switch = True
                    