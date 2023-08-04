import glm
import random
from copy import copy
import random

from .entity import Entity

from pygame_3d import *
from src.scripts.rect3D import Rect3

class Planet(Entity):
    def __init__(self, scene, *args, **kwargs):
        super().__init__(*args, **kwargs)   
        self.scene = scene
        self.rotation = glm.vec3(1, 0, 0)
        self.position = glm.vec3(-10, 0, 0)
        self.direction = glm.vec3(-0.001, 0, 0)

        size = random.uniform(0.5, 1)
        self.scale = glm.vec3(size, size, size)

        self.planet_types = ["green", "red"]
        
        self.planet_data = {
            "green": {"water": -0.3, "water_color": (0, 0, 1), "land_color": (0.1, 0.8, 0.2)},
            "red": {"water": 0.1, "water_color": (79/255, 90/255, 87/255), "land_color": (87/255, 20/255, 17/255)} 
        }

        self.type = random.choice(self.planet_types)
        self.data = self.planet_data[self.type]

        for i, face in enumerate(self.faces):
            scale = -0.3
            vert = sum(self.vertices[face.vertices]) / len(face.vertices)
            vert *= scale

            n = opensimplex.noise3(*vert[0:3])
            c = opensimplex.noise3(*(vert[0:3] + np.array([100, 100, 100])))
            if n > self.data["water"]:
                face.material["color"] = self.data["water_color"]
            else:
                norms = self.normals[face.normals]
                adjust = []
                for i, norm in enumerate(norms):
                    x = list(norm)
                    x.append(0)
                    adjust.append(np.array(x))
                adjust = np.array(adjust)
                # self.vertices[face.vertices] += adjust / 10
                face.material["color"] = self.data["land_color"]
        
        self.origin_rect = Rect3.from_vertices(self.vertices)
        self.rect = copy(self.origin_rect)
        #doing this so on the first frame collision doesn't get detected
        self.rect.position = (1000, 1000, 1000)

    def render(self, *args, **kwargs):
        super().render(*args, **kwargs)
        self.degree+=0.2
        self.rect.position = (self.origin_rect.position + self.position)