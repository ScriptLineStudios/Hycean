import pygame
import pygame._sdl2
from pygame.locals import *
from .state import State


class Game(State):
    def __init__(self):
        super().__init__()

    def update(self):
        ...

    def render(self, renderer):
        renderer.draw_color = (255, 0, 0, 255)
        renderer.clear()
        