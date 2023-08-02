import glm
import random

from .entity import Entity

from pygame_3d import *

class Player(Entity):
    def __init__(self, scene, *args, **kwargs):
        super().__init__(*args, **kwargs)   
        self.scene = scene
        self.rotation = glm.vec3(1, 0, 0)
        # self.direction = glm.vec3(-0.01, 0, 0)

    def render(self, *args, **kwargs):
        super().render(*args, **kwargs)

        # if random.randrange(0, 40) == 10:
        #     p = Model("src/assets/models/spaceship/cube.obj", "src/assets/models/spaceship/cube.mtl")
        #     p.position = self.position
        #     self.scene.model_renderer.add_model(p)
        #     print(len(self.scene.model_renderer.models))



    