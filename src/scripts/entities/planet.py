import glm
import random
from copy import copy
import random

import time

from .entity import Entity

from pygame_3d import *
from src.scripts.rect3D import Rect3

class Planet(Entity):
    def __init__(self, scene, *args, **kwargs):
        super().__init__(*args, **kwargs)   
        self.scene = scene
        self.app = self.scene.app

        self.rotation = glm.vec3(1, 0, 0)
        self.position = glm.vec3(-10, 0, 0)
        self.direction = glm.vec3(-0.001, 0, 0)

        size = random.uniform(0.5, 1)
        self.scale = glm.vec3(size, size, size)

        #gotta come up with an method to distribute materials
        try:
            self.primary_material = random.choice(list(self.app.needed_resources.items()))
            del self.app.needed_resources[self.primary_material[0]]
        except:
            self.primary_material = (None, None)
            
        self.planet_types = ["blue", "red"]
        
        self.planet_data = {
            "blue": {"water": -0.3, "water_color": (0, 0, 1), "land_color": (0.1, 0.8, 0.2)},
            "red": {"water": 0.1, "water_color": (79/255, 90/255, 87/255), "land_color": (87/255, 20/255, 17/255)} 
        }

        self.type = random.choice(self.planet_types)
        self.data = self.planet_data[self.type]

        opensimplex.seed(random.randrange(-1000, 1000))
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
        
        ScaleRect = 35
        self.origin_rect.width += ScaleRect
        self.origin_rect.height += ScaleRect
        self.origin_rect.depth += ScaleRect
        self.origin_rect.x -= ScaleRect * 0.5
        self.origin_rect.y -= ScaleRect * 0.5
        self.origin_rect.z -= ScaleRect * 0.5

        self.rect = copy(self.origin_rect)
        #doing this so on the first frame collision doesn't get detected
        self.rect.position = (1000, 1000, 1000)

    def render(self, *args, **kwargs):
        super().render(*args, **kwargs)
        self.degree += 0.2

        self.rect.position = (self.origin_rect.position + self.position)
        self.rect.size = self.origin_rect.size