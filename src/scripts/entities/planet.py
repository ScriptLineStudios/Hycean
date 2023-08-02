import glm
import random

from .entity import Entity

from pygame_3d import *

class Planet(Entity):
    def __init__(self, scene, *args, **kwargs):
        super().__init__(*args, **kwargs)   
        self.scene = scene
        self.rotation = glm.vec3(1, 0, 0)
        self.position = glm.vec3(-10, 0, 0)
        self.direction = glm.vec3(-0.001, 0, 0)

        for i, face in enumerate(self.faces):
            scale = -0.3
            vert = sum(self.vertices[face.vertices]) / len(face.vertices)
            vert *= scale

            n = opensimplex.noise3(*vert[0:3])
            c = opensimplex.noise3(*(vert[0:3] + np.array([100, 100, 100])))
            if c > 0.4:
                face.material["color"] = (1, 1, 1)
            else:
                if n > 0:
                    face.material["color"] = (0, 0, 1)
                    if n > 0.4:
                        face.material["color"] = (0, 0, 0.6)

                else:
                    norms = self.normals[face.normals]
                    adjust = []
                    for i, norm in enumerate(norms):
                        x = list(norm)
                        x.append(0)
                        adjust.append(np.array(x))
                    adjust = np.array(adjust)
                    self.vertices[face.vertices] += adjust / 10
                    face.material["color"] = (0.1, 0.8, 0.2)

    def render(self, *args, **kwargs):
        super().render(*args, **kwargs)

    