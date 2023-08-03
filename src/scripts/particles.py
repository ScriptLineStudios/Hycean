import pygame
import pygame._sdl2
import glm
from .sprite import Sprite
from math import cos, sin
from random import uniform
from pygame_3d import Model


class SpaceParticles:
    def __init__(self, ScreenSize, renderer, starCount):
        self.stars = []
        
        self.ScreenSize = ScreenSize

        self.texture = pygame._sdl2.Texture.from_surface(
            renderer,
            pygame.image.load('src/assets/star.png')
        )
        
        # origin = (0, 0, 0)
        distance = 1
        for starN in range(starCount):
            direction = [
                cos(uniform(0.00, 6.28)) * distance,
                sin(uniform(0.00, 6.28)) * distance,
                cos(uniform(0.00, 6.28)) * distance
            ]
            
            star = Sprite(self.texture, direction) # , (32, 32)
            self.stars.append(star)
        

    def render(self, camera):
        for sprite in self.stars:
            matrix = camera
            projected = [
                sprite.position[0] / sprite[2],
                sprite.position[1] / sprite[2]
                ]
            
            sprite.draw(projected, 0.2)

    def render(self, matrix, light, camera):
        vertices = self.vertices.copy()

        self.position_matrix = glm.mat4()
        self.rotation_matrix = glm.mat4()

        self.position_matrix = glm.translate(self.position_matrix, self.position)
        self.rotation_matrix = glm.rotate(self.rotation_matrix, glm.radians(self.degree), self.rotation)

        for i, vertex in enumerate(vertices):
            v = glm.vec4(vertex)
            vertices[i] = (matrix * self.rotation_matrix * self.position_matrix) * v
            self.average_z += vertices[i][2]

        screen_vertices = Model.screen(Model.three_to_two(vertices))
    
    def render(self, matrix, camera):
        for sprite in self.stars:
            projected = glm.vec4(
                sprite.position[0], sprite.position[1], sprite.position[2], 1
            )
            
            projected = projected * matrix
            
            projected = [
                projected[0] / projected[2],
                projected[1] / projected[2]
                ]

            projected[0] /= 2
            projected[1] /= 2
            projected[0] += 1
            projected[1] += 1

            projected[0] *= self.ScreenSize[0]
            projected[1] *= self.ScreenSize[1]

            sprite.draw(projected, 0.1)