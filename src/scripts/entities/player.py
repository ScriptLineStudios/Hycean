import glm
import random

from .entity import Entity

from pygame_3d import *
from src.scripts.rect3D import Rect3

class Player(Entity):
    def __init__(self, scene, *args, **kwargs):
        super().__init__(*args, **kwargs)   
        self.scene = scene
        self.rotation = glm.vec3(-1, 0, 0)
        self.rot_x = 0
        self.rot_y = 0
        self.rot_z = 0

        self.direction = glm.vec3(0, 0, 0)

        self.orientation = glm.vec3(0, 0, -1)

        self.rect = Rect3.from_vertices(self.vertices)

        self.flame_id = 0

        self.flames = [pygame.image.load("src/assets/fire1.png"), pygame.image.load("src/assets/fire2.png"), pygame.image.load("src/assets/fire3.png")]
        for i, flame in enumerate(self.flames):
            flame.set_colorkey((255, 255, 255))
            flame = pygame.transform.flip(flame, False, True)
            self.flames[i] = pygame._sdl2.Texture.from_surface(self.scene.renderer, flame)

    def update(self, RectPosition):
        self.rect.position = RectPosition

    def render(self, *args, **kwargs):
        self.rotation_matrix = glm.mat4()
        self.rotation_matrix = glm.rotate(self.rotation_matrix, glm.radians(self.rot_x), glm.vec3(1, 0, 0))
        self.rotation_matrix = glm.rotate(self.rotation_matrix, glm.radians(self.rot_y), glm.vec3(0, 1, 0))
        self.rotation_matrix = glm.rotate(self.rotation_matrix, glm.radians(self.rot_z), glm.vec3(0, 0, 1))


        super().render(*args, **kwargs, use_rotate=False, always_draw=True)
        # self.scene.renderer.blit(self.flames[0], pygame.Rect(460, 550, 64, 64), angle=-self.rot_x / 100)
        if self.scene.moving:
            self.flames[self.flame_id // 7].draw(None, pygame.Rect(460, 550, 64, 64), angle=self.rot_x)
            self.flame_id += 1
            if self.flame_id > len(self.flames) * 7 - 1:
                self.flame_id = 0


    