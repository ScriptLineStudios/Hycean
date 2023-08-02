import glm

from pygame_3d import *

class Entity(Model):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.direction = glm.vec3(0.0, 0.0, 0.0)

    def render(self, *args, **kwargs):
        self.position += self.direction
        super().render(*args, **kwargs)


