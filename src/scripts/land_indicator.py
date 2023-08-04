import pygame
from pygame._sdl2 import Texture


class LandIndicator:
    def __init__(self, renderer, ScreenSize):
        self.texture = Texture.from_surface(
            renderer,
            pygame.image.load('src/assets/LandIndicator.png')
        )

        self.rect = self.texture.get_rect(center=(500, 700))

        self.planet = None
        self.distance = 0
        self.min_distance = 0
        self.max_distance = 25
        self.max_distance -= self.min_distance

    def draw(self):
        scaleFactor = self.distance / self.max_distance
        if scaleFactor > 1:
            scaleFactor = 1
        scaleFactor = abs(1 - scaleFactor)

        ScaledRect = self.rect.copy()
        ScaledRect.width *= scaleFactor
        ScaledRect.height *= scaleFactor
        ScaledRect.center = self.rect.center
        
        if self.planet != None:
            self.texture.draw(srcrect=None, dstrect=ScaledRect)
    
    def update_planet(self, planet, distance):
        self.planet = planet
        self.distance = distance