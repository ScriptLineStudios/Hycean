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

    def update(self):
        self.rect.position = self.position

    def render(self, *args, **kwargs):
        self.rotation_matrix = glm.mat4()
        self.rotation_matrix = glm.rotate(self.rotation_matrix, glm.radians(self.rot_x), glm.vec3(1, 0, 0))
        self.rotation_matrix = glm.rotate(self.rotation_matrix, glm.radians(self.rot_y), glm.vec3(0, 1, 0))
        self.rotation_matrix = glm.rotate(self.rotation_matrix, glm.radians(self.rot_z), glm.vec3(0, 0, 1))

        super().render(*args, **kwargs, use_rotate=False, always_draw=True)

        # if random.randrange(0, 40) == 10:
        #     p = Model("src/assets/models/spaceship/cube.obj", "src/assets/models/spaceship/cube.mtl")
        #     p.position = self.position
        #     self.scene.model_renderer.add_model(p)
        #     print(len(self.scene.model_renderer.models))



    