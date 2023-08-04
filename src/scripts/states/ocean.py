from .state import State
from src.scripts.entities.player import Player
from src.scripts.entities.planet import Planet
from src.scripts.entities.entity import Entity
from src.scripts.entities.asteroid import Asteroid
from src.scripts.particles import SpaceParticles
from src.scripts.controller import Controller

from copy import copy
import random

import pygame
pygame.font.init()

class Player:
    def __init__(self, scene):
        self.scene = scene
        self.player_img = pygame.image.load("src/assets/player.png")
        self.player_img.set_colorkey((255, 255, 255))

        self.rect = pygame.Rect(250, 200, 32, 32)

    def update(self):
        pass

    def render(self):
        self.scene.surface.blit(self.player_img, (self.rect.x, self.rect.y))

class Ocean(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = Player(self)

        self.colors = {
            "blue": (10, 20, 100, 255),
            "red": (100, 20, 10, 255),
            "green": (40, 200, 60, 255)
        }

        self.color = "blue"

        self.surface = pygame.Surface((500, 400))
        
    def update(self):
        self.player.update()

    def render(self):
        self.renderer.draw_color = self.colors[self.color]
        self.renderer.clear()
        self.surface.fill(self.colors[self.color])

        self.player.render()

        self.renderer.blit(pygame._sdl2.Texture.from_surface(self.renderer, self.surface), pygame.Rect(0, 0, 1000, 800))


    