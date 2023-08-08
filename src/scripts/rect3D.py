import pygame
from pygame.locals import *
from dataclasses import dataclass
from math import cos, sin, radians
from json import load
#from src.3dengine import Face


@dataclass
class Face:
    vertices: list
    color: pygame.Color
    width: int = -1
    height: int = -1


# when pygame.Rect3 and pygame.FRect3 for pygame-ce
class Rect3:
    def __init__(self, x, y, z, width, height, depth):
        self._x = x
        self._y = y
        self._z = z

        self.width = width
        self.height = height
        self.depth = depth

        self._position = [x, y, z]
        self.size = (width, height, depth)
        
        self.update_vertices(x, y, z, width, height, depth)
        
        redColor = pygame.Color('red')
        self.faces = [
            # Front
            Face([1, 0, 3], redColor),
            Face([1, 2, 3], redColor),
            # Back
            Face([5, 6, 7], redColor),
            Face([5, 4, 7], redColor),
            # Left
            Face([1, 0, 4], redColor),
            Face([1, 4, 5], redColor),
            # Right
            Face([3, 2, 7], redColor),
            Face([2, 6, 7], redColor),
            # Top
            Face([0, 4, 7], redColor),
            Face([0, 7, 3], redColor),
            # Bottom
            Face([2, 5, 6], redColor),
            Face([2, 1, 5], redColor),
        ]
    
    @classmethod
    def from_vertices(cls, vertices):
        #that's not good for the performance I think💀😭
        xVerts = [vertex[0] for vertex in vertices]
        yVerts = [vertex[1] for vertex in vertices]
        zVerts = [vertex[2] for vertex in vertices]
        
        minX = min(xVerts)
        minY = min(yVerts)
        minZ = min(zVerts)

        maxX = max(xVerts)
        maxY = max(yVerts)
        maxZ = max(zVerts)

        width = maxX - minX
        height = maxY - minY
        depth = maxZ - minZ

        return Rect3(minX, minY, minZ, width, height, depth)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        # when setting value to position, also updating all these
        self._x = value[0]
        self._y = value[1]
        self._z = value[2]

        self.update_vertices(
            self._x, self._y, self._z,
            self.width, self.height, self.depth
        )

        self._position = [value[0], value[1], value[2]]

    @property
    def center(self):
        center = [
            self._x + self.width / 2,
            self._y + self.height / 2,
            self._z + self.depth / 2
        ]
        return center

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

        self.update_vertices(
            self._x, self._y, self._z,
            self.width, self.height, self.depth
        )

        self._position[0] = value
        
    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

        self.update_vertices(
            self._x, self._y, self._z,
            self.width, self.height, self.depth
        )

        self._position[1] = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value

        self.update_vertices(
            self._x, self._y, self._z,
            self.width, self.height, self.depth
        )

        self._position[1] = value

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, value):
        self._z = value

        self.update_vertices(
            self._x, self._y, self._z,
            self.width, self.height, self.depth
        )

        self._position[2] = value

    def collide_rect(self, other):
        collision = [False, False, False]

        # x collision
        if self._x < other.x + other.width and self._x + self.width > other.x:
            collision[0] = True

        #y collision
        if self._y < other.y + other.height and self._y + self.height > other.y:
            collision[1] = True

        #z collision
        if self._z < other.z + other.depth and self._z + self.depth > other.z:
            collision[2] = True

        if all(collision):
            return True
        else:
            return False

    def collide_point(self, point):
        collision = [False, False, False]

        # x collision
        if self._x < point.x and self._x + self.width > point.x:
            collision[0] = True

        #y collision
        if self._y < point.y and self._y + self.height > point.y:
            collision[1] = True

        #z collision
        if self._z < point.z and self._z + self.depth > point.z:
            collision[2] = True

        if all(collision):
            return True
        else:
            return False

    
    def draw_debug(self, camera):
        #*imagine here drawing faces (for debug)*💀
        ...
    

    def update_size(self, width, height, depth):
        self.size = (width, height, depth)

        self.update_vertices(self._x, self._y, self._z, width, height, depth)

    def update_vertices(self, x, y, z, width, height, depth):
        self.vertices = [
            (x, y, z),
            (x, y + height, z),
            (x + width, y + height, z),
            (x + width, y, z),
            (x, y, z + depth),
            (x, y + height, z + depth),
            (x + width, y + height, z + depth),
            (x + width, y, z + depth),
        ]
        

def ray_to_rect(position, direction, rect, steps):
    #haven't tested
    #if used for picking up objects, add id or func argument to rect3
    position = pygame.Vector3(position)
    rayDir = pygame.Vector3(
        cos(radians(direction[0])),
        sin(radians(direction[1])),
        cos(radians(direction[2])), # is that right?
        )
    
    for step in range(steps):
        collision = rect.collide_point(position)

        if collision:
            return position
        
        position += rayDir

    return False


def load_obstacles(file):
    rects = []
    with open(file, 'r') as file:
        for rect in load(file):
            position = rect['position']
            size = rect['size']
            rect = Rect3(
                position[0], position[1], position[2], 
                size[0], size[1], size[2]
            )
            rects.append(rect)

    return rects