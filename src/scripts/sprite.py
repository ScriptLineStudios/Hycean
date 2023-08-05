import pygame
from pygame._sdl2 import Texture
import glm
from random import uniform, choice
from pygame_3d import *
from math import cos, sin


#should change the name, it's just a 2d image in 3d space scaled by Z
#haven't tested, hope it works🤞
class Sprite:
    def __init__(self, texture, position, size=None):
        self.position = position

        self.texture = texture
        if size != None:
            self.rect = pygame.Rect(0, 0, size[0], size[1])
        else:
            self.rect = self.texture.get_rect()

    def draw(self, position, normalizedZ):
        scaleRect = self.rect.copy()
        scaleRect.center = position
        scaleRect.width *= normalizedZ
        scaleRect.height *= normalizedZ

        self.texture.draw(srcrect=None, dstrect=scaleRect)
    
    def draw_debug(self, renderer):
        pass


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

    def render(self, matrix, camera):
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