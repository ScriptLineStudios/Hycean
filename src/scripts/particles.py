import pygame
from pygame._sdl2 import Texture
from pygame._sdl2 import Texture
import glm
from random import uniform, choice
from pygame_3d import *
from math import cos, sin
from .sprite import Sprite


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
        
        # origin = (0, 0, 0)
        self.vertices = []
        distance = 10000
        for starN in range(starCount):
            direction = glm.vec3(
                cos(uniform(0.00, 6.28)) * distance,
                sin(uniform(0.00, 6.28)) * distance,
                cos(uniform(0.00, 6.28)) * distance
            )
            
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


class JetFire:
    def __init__(self, ScreenSize, renderer):
        self.fire = []
        
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
        self.vertices = np.array(self.vertices, dtype=np.double)

        self.original_vertices = self.vertices.copy()

        self.position_matrix = glm.mat4()
        self.position = glm.vec3()

        self.rotation_matrix = glm.mat4()
        self.scale_matrix = glm.mat4()

        self.degree = 0

        self.life_time = 50 # in frames

    @staticmethod
    def screen(v):
        return np.column_stack((((v[:, 0] + 1) / 2) * 1000, (1 - (v[:, 1] + 1) / 2) * 800))

    @staticmethod
    def three_to_two(v):
        return np.column_stack(((v[:, 0] / (v[:, 2] + 1)), (v[:, 1] / (v[:, 2] + 1))))
    
    def add_particle(self, position):
        self.timers.append(self.life_time)
        self.original_vertices = list(self.original_vertices)
        self.original_vertices.append(position)
        self.vertices = list(self.vertices)
        self.vertices.append(position)

        self.vertices = np.array(self.vertices, dtype=np.double)
        self.original_vertices = np.array(self.original_vertices, dtype=np.double)

        self.fire.append(Sprite(choice(self.textures), position))

    def update(self):
        to_remove = []
        for index, timer in enumerate(self.timers):
            # REMOVE BREAK so it starts removing
            break
            self.timers[index] -= 1
            if self.timers[index] <= 0:
                self.timers.pop(index)
                to_remove.append(index)
                self.fire.pop(index)

        #it would be awesome if i could remove elements from numpy array in any good way💀
        #self.vertices = np.delete(self.vertices, to_remove)
        #print(self.vertices, to_remove)
        #self.original_vertices = np.delete(self.original_vertices, to_remove)
                


    def render(self, matrix):
        self.update()
        vertices = self.vertices

        self.position_matrix = glm.mat4()
        self.position_matrix = glm.translate(self.position_matrix, self.position)

        self.rotation_matrix = glm.mat4()

        for i, vertex in enumerate(vertices):
            v = glm.vec3(
                self.original_vertices[i]
            )

            # = self.scale_matrix * (matrix * self.position_matrix * self.rotation_matrix) * v
            vertices[i] = self.scale_matrix * (matrix * self.position_matrix * self.rotation_matrix) * v

        screen_vertices = self.screen(self.three_to_two(vertices))
        
        for i, vertex in enumerate(screen_vertices):
            if vertices[i][2] < 0.0:
                continue
            self.fire[i].position = vertex
            self.fire[i].draw(vertex, 0.2)


#NOT FUNCTIONING, can be removed
class SpaceParticles:
    def __init__(self, ScreenSize, renderer, starCount):
        self.stars = []
        
        self.ScreenSize = ScreenSize

        self.texture = Texture.from_surface(
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