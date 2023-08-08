import pygame
from pygame._sdl2 import Texture
from pygame._sdl2 import Texture
import glm
from random import uniform, choice
from pygame_3d import *
from math import cos, sin
from .sprite import Sprite
from copy import copy


class Stars:
    def __init__(self, ScreenSize, renderer, starCount):
        self.stars = []
        
        self.ScreenSize = ScreenSize

        self.images = [
            pygame.image.load('src/assets/stars/star1.png'),
            pygame.image.load('src/assets/stars/star2.png'),
            pygame.image.load('src/assets/stars/star3.png'),
            pygame.image.load('src/assets/stars/star4.png'),
            pygame.image.load('src/assets/stars/star5.png'),
        ]
        self.textures = []
        for image in self.images:
            texture = Texture.from_surface(
                renderer, image
            )
            self.textures.append(texture)
        
        easterEgg = pygame.image.load('src/assets/pg_chad.png')
        self.easterEgg = Texture.from_surface(
                renderer, easterEgg
        )

        # origin = (0, 0, 0)
        self.vertices = []
        distance = 10000
        easterEggAdd = True
        for starN in range(starCount):
            direction = glm.vec3(
                cos(uniform(0.00, 6.28)) * distance,
                sin(uniform(0.00, 6.28)) * distance,
                cos(uniform(0.00, 6.28)) * distance
            )

            if easterEggAdd:
                self.vertices.append(direction)
                self.stars.append(Sprite(self.easterEgg, direction))
                easterEggAdd = False
                continue
            
            self.vertices.append(direction)
            self.stars.append(Sprite(choice(self.textures), direction))


            
        self.vertices = np.array(self.vertices, dtype=np.double)

        self.original_vertices = self.vertices.copy()

        self.position_matrix = glm.mat4()
        self.position = glm.vec3()

        self.rotation_matrix = glm.mat4()
        self.scale_matrix = glm.mat4()

        self.degree = 0

    @staticmethod
    def screen(v):
        return np.column_stack((((v[:, 0] + 1) / 2) * 1000, (1 - (v[:, 1] + 1) / 2) * 800))

    @staticmethod
    def three_to_two(v):
        return np.column_stack(((v[:, 0] / (v[:, 2] + 1)), (v[:, 1] / (v[:, 2] + 1))))

    def render(self, matrix):
        vertices = self.vertices

        self.position_matrix = glm.mat4()
        self.position_matrix = glm.translate(self.position_matrix, self.position)

        self.rotation_matrix = glm.mat4()

        for i, vertex in enumerate(vertices):
            v = glm.vec3(
                self.original_vertices[i]
            )
            vertices[i] = self.scale_matrix * (matrix * self.position_matrix * self.rotation_matrix) * v

        screen_vertices = self.screen(self.three_to_two(vertices))
        
        for i, vertex in enumerate(screen_vertices):
            self.stars[i].position = vertex
            self.stars[i].draw(vertex, 0.2)


class JetFlame:
    def __init__(self, ScreenSize, renderer):
        self.flame = []
        
        self.ScreenSize = ScreenSize

        self.images = [
            pygame.image.load('src/assets/fire/fire1.png'),
            pygame.image.load('src/assets/fire/fire2.png'),
            pygame.image.load('src/assets/fire/fire3.png'),
        ]
        self.textures = []
        for image in self.images:
            texture = Texture.from_surface(
                renderer, image
            )
            self.textures.append(texture)
        
        self.timers = []
        self.vertices = []

        self.original_vertices = copy(self.vertices)

        self.position_matrix = glm.mat4()
        self.position = glm.vec3()

        self.rotation_matrix = glm.mat4()
        self.scale_matrix = glm.mat4()

        self.degree = 0

        self.life_time = 100 # in frames

        #please don't ask what is this💀
        self.timers.append(100000000)
        self.original_vertices.append((100000, 100000, 100000))
        self.vertices.append((100000, 100000, 100000))

        self.flame.append(Sprite(choice(self.textures), (100000, 100000, 100000)))

    @staticmethod
    def screen(v):
        return np.column_stack((((v[:, 0] + 1) / 2) * 1000, (1 - (v[:, 1] + 1) / 2) * 800))

    @staticmethod
    def three_to_two(v):
        return np.column_stack(((v[:, 0] / (v[:, 2] + 1)), (v[:, 1] / (v[:, 2] + 1))))
    
    def add_particle(self, position):
        self.timers.append(self.life_time)
        self.original_vertices.append(position)
        self.vertices.append(position)

        self.flame.append(Sprite(choice(self.textures), position))

    def clear(self):
        self.timers = []
        self.original_vertices = []
        self.vertices = []
        self.flame = []

        #please don't ask what is this💀
        self.timers.append(100000000)
        self.original_vertices.append((100000, 100000, 100000))
        self.vertices.append((100000, 100000, 100000))

        self.flame.append(Sprite(choice(self.textures), (100000, 100000, 100000)))


    def update(self):
        for index, timer in enumerate(self.timers):

            self.timers[index] -= 1
            if self.timers[index] <= 0:
                self.timers.pop(index)
                self.original_vertices.pop(index)
                self.vertices.pop(index)
                self.flame.pop(index)


    def render(self, matrix):
        self.update()
        vertices = np.array(self.vertices, dtype=np.double)
        original_vertices = np.array(self.original_vertices, dtype=np.double)



        self.position_matrix = glm.mat4()
        self.position_matrix = glm.translate(self.position_matrix, self.position)

        self.rotation_matrix = glm.mat4()

        for i, vertex in enumerate(vertices):
            v = glm.vec3(
                original_vertices[i]
            )

            # = self.scale_matrix * (matrix * self.position_matrix * self.rotation_matrix) * v
            vertices[i] = self.scale_matrix * (matrix * self.position_matrix * self.rotation_matrix) * v

        screen_vertices = self.screen(self.three_to_two(vertices))
        
        for i, vertex in enumerate(screen_vertices):
            if vertices[i][2] < 0.0:
                continue
            if i == 0:  # do not ask what is this
                continue
            self.flame[i].position = vertex
            self.flame[i].draw(vertex, 0.2)