import glm
import random
from copy import copy
import random

from .entity import Entity

from pygame_3d import *
from src.scripts.rect3D import Rect3

class Asteroid(Entity):
    def __init__(self, scene, *args, **kwargs):
        super().__init__("src/assets/models/asteroid/asteroid.obj", "src/assets/models/asteroid/asteroid.mtl")   
        self.lifetime = 500

        self.rect = Rect3.from_vertices(self.vertices)

    def render(self, *args, **kwargs):
        self.rect.position = self.position
        super().render(*args, **kwargs)
