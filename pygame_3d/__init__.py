import pygame
import pygame._sdl2
import random
import glm
import math
import numpy as np
from numba import jit, njit
from dataclasses import dataclass
import time
import opensimplex

def pygame_vec_to_glm_vec3(vec):
    return glm.vec3(vec.x, vec.y, vec.z)

def pygame_vec_to_glm_vec(vec):
    return glm.vec4(vec[0], vec[1], vec[2], 1)
    
@dataclass
class Face:
    vertices: list
    uvs: list   
    normals: list
    material: dict
    light: float
    vertices_length: int
    
class Camera:
    def __init__(self):
        self.position = glm.vec3(0.0, 0.0, 2)
        self.up = glm.vec3(0, 1, 0)
        self.orientation = glm.vec3(0, 0, -1)

        self.free_cam = False
        self.acceleration = glm.vec3(0, 0, 0)
        self.velocity = glm.vec3(0, 0, 0)
        self.damping = glm.vec3(0.98, 0.98, 0.98)

        self.speed = .1
        self.hidden = False
        self.sensitivity = 10

        self.accSpeed = self.speed * 0.25
        self.maxSpeed = 5

        self.t = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()

        # if keys[pygame.K_d]:
        #     self.position += self.speed * glm.normalize(glm.cross(self.orientation, self.up))
        # if keys[pygame.K_a]:
        #     self.position -= self.speed * glm.normalize(glm.cross(self.orientation, self.up))
        # if keys[pygame.K_w]:
        #     if self.free_cam:
        #         self.position -= self.speed * self.orientation
        #     else:
        #         self.acceleration -= self.accSpeed * self.orientation
        # if keys[pygame.K_s]:
        #     if self.free_cam:
        #         self.position += self.speed * self.orientation
        #     else:
        #         self.acceleration += (self.accSpeed * self.orientation) / 2

        # if keys[pygame.K_SPACE]:
        #     self.position += self.speed * self.up
        # if keys[pygame.K_LSHIFT]:
        #     self.position -= self.speed * self.up

        if self.hidden:
            mx, my = pygame.mouse.get_pos()
            rot_x = self.sensitivity * (my - 400) / 400
            rot_y = self.sensitivity * (mx - 500) / 500

            self.t += 1
            new_orientation = glm.rotate(self.orientation, glm.radians(rot_x / 1), glm.normalize(glm.cross(self.orientation, self.up)))

            # if (abs(glm.angle(new_orientation, self.up) - glm.radians(90.0)) <= glm.radians(85.0)):
            self.orientation = new_orientation

            self.orientation = glm.rotate(self.orientation, glm.radians(rot_y / 1), self.up)
            
            pygame.mouse.set_pos((500, 400))

    def update(self):
        self.handle_input()

        self.velocity += self.acceleration
        self.position += self.velocity
        self.velocity *= self.damping
        
        self.acceleration *= 0

        view = glm.mat4()

        view = glm.lookAt(self.position, self.position + self.orientation, self.up)
        return view

class Model:
    @staticmethod
    def parse_material(f):
        material = {}
        while True:
            try:
                line = next(f).strip()
            except StopIteration:
                break
            if line.startswith("Kd"):
                color = line.split(" ")[1:]
                material["color"] = (float(color[0]) + random.uniform(-0.01, 0.01), 
                float(color[1]) + random.uniform(-0.01, 0.01), 
                float(color[2]) + random.uniform(-0.01, 0.01))
            if line.startswith("map_Kd"):
                path = line.split(" ")[1]
                try:
                    material["image"] = pygame.surfarray.pixels3d(pygame.image.load(path))
                except:
                    pass
            if not line:
                break
        return material

    @staticmethod   
    def parse_mtl_file(mtl_file):
        materials = {}
        lines = []
        with open(mtl_file, "r") as f:
            line = ""
            while True:
                try:
                    line = next(f).strip()
                except StopIteration:
                    break
                if line.startswith("newmtl"):
                    name = line.split(" ")[1]
                    material = Model.parse_material(f)
                    materials[name] = material
        return materials

    @staticmethod
    def parse_obj_file(obj_file, materials):
        vertices = []
        vertex_normals = []
        vertex_textures = []
        faces = []
        current_material = {}
        with open(obj_file, "r") as f:
            line = ""
            while True:
                try:
                    line = next(f).strip()
                    if line.startswith("v "):
                        vertex = line.split(" ")[1:]
                        vertex = pygame.Vector3([float(v) for v in vertex])
                        # vertex.z += 2
                        vertices.append(pygame_vec_to_glm_vec(pygame.Vector3(vertex.x, vertex.y, vertex.z)))
                    
                    if line.startswith("vt "):
                        vt = line.split(" ")[1:]
                        vertex_textures.append(pygame.Vector2([float(v) for v in vt]))

                    if line.startswith("vn "):
                        vn = line.split(" ")[1:]
                        vertex_normals.append(pygame.Vector3([float(v) for v in vn]))
                    
                    if line.startswith("usemtl "):
                        current_material = materials[line.split("usemtl ")[1]]
                    if line.startswith("f "):
                        vs, vts, vns = [], [], []
                        for point in line.split(" ")[1:]:
                            if "//" not in line:
                                v, vt, vn = point.split("/")
                                v, vt, vn = int(v), int(vt), int(vn)
                                vs.append(v - 1)
                                vts.append(vt - 1)
                                vns.append(vn - 1)
                            else:
                                v, vn = point.split("//")
                                v, vn = int(v), int(vn)
                                vs.append(v - 1)
                                vns.append(vn - 1)
                        
                        faces.append(Face(vs, vts, vns, current_material.copy(), random.uniform(-0.02, 0.02), len(vs)))
                except StopIteration:
                    break
        return vertices, vertex_textures, vertex_normals, faces

    def __init__(self, obj_file, mtl_file):
        self.materials = self.parse_mtl_file(mtl_file)
        self.vertices, self.uvs, self.normals, self.faces = self.parse_obj_file(obj_file, self.materials)
        self.vertices = np.array(self.vertices, dtype=np.double)
        self.uvs = np.array(self.uvs)
        self.normals = np.array(self.normals)
        self.faces = np.array(self.faces)

        self.original_vertices = self.vertices.copy()

        self.position_matrix = glm.mat4()
        self.position = glm.vec3()

        self.rotation_matrix = glm.mat4()
        self.rotation = glm.vec3(1, 1, 1)
        self.scale = glm.vec3(1, 1, 1)
        self.scale_matrix = glm.mat4()

        self.average_z = 0
        self.degree = 0

        vertices = self.vertices.copy()
        for i, vertex in enumerate(vertices):
            v = glm.vec4(vertex)
            vertices[i] = self.scale_matrix * (glm.mat4() * self.position_matrix * self.rotation_matrix) * v
            self.average_z += vertices[i][2]

        self.average_z /= len(vertices)

    @staticmethod
    #commented for now so it's faster to debug
    # @jit(nopython=True, fastmath=True, nogil=True)
    def screen(v):
        return np.column_stack((((v[:, 0] + 1) / 2) * 1000, (1 - (v[:, 1] + 1) / 2) * 800))

    @staticmethod
    # @jit(nopython=True, fastmath=True, nogil=True)
    def three_to_two(v):
        return np.column_stack(((v[:, 0] / (v[:, 2] + 1)), (v[:, 1] / (v[:, 2] + 1))))

    @staticmethod
    #@jit(nopython=True, fastmath=True, nogil=True)
    def color(_color):
        off = 0
        _color = np.array([
            int(float(_color[0]) * 255), 
            int(float(_color[1]) * 255), 
            int(float(_color[2]) * 255),
        ])
        return _color

    @staticmethod
    def calculate_culling(cam, vertices):
        V0 = glm.vec3(vertices[0][0:3])
        P = glm.normalize(-cam)
        N = glm.cross((glm.vec3(vertices[1][0:3]) - glm.vec3(vertices[0][0:3])), (glm.vec3(vertices[2][0:3]) - glm.vec3(vertices[1][0:3])))
        return glm.dot(glm.normalize(V0 - P), N)

    def render_face(self, display, face, vertices, old_vertices, light, screen_vertices, camera):
        # if glm.distance(self.position, camera.position) < 5:
        z = sum([old_vertices[j][2] for j in face.vertices]) / face.vertices_length
        if z < 0.7:
            return

        normals = self.normals[face.normals]
        d = glm.max(glm.dot(glm.vec3(normals[0]), -light), 0.0)
        color = glm.vec3(face.material["color"])

        if d > 0.4:
            # pygame.draw.polygon(display, Model.color(color * d), vertices[face.vertices])
            color = Model.color(color * d)
            r = int(color[0])
            g = int(color[1])
            b = int(color[2])
            a = 255

            display.draw_color = r, g, b, a

            if len(screen_vertices[face.vertices]) == 3:
                display.fill_triangle(screen_vertices[face.vertices][0], screen_vertices[face.vertices][1], screen_vertices[face.vertices][2])
        else:
            # pygame.draw.polygon(display, Model.color((color * (d + 0.2 + face.light))), vertices[face.vertices])
            color = Model.color((color * (d + 0.2 + face.light)))
            r = int(color[0])
            g = int(color[1])
            b = int(color[2])
            a = 255

            display.draw_color = r, g, b, a
        
            if len(screen_vertices[face.vertices]) == 3:
                display.fill_triangle(screen_vertices[face.vertices][0], screen_vertices[face.vertices][1], screen_vertices[face.vertices][2])


    def render(self, display, matrix, light, camera, use_rotate=True, always_draw=False):
        vertices = self.vertices
        old_vertices = vertices

        self.scale_matrix = glm.mat4()

        self.position_matrix = glm.mat4()
        self.position_matrix = glm.translate(self.position_matrix, self.position)
        self.scale_matrix = glm.scale(self.scale_matrix, self.scale)

        if use_rotate:
            self.rotation_matrix = glm.mat4()
            self.rotation_matrix = glm.rotate(self.rotation_matrix, glm.radians(self.degree), self.rotation)

        for i, vertex in enumerate(vertices):
            v = glm.vec4(self.original_vertices[i])
            vertices[i] = self.scale_matrix * (matrix * self.position_matrix * self.rotation_matrix) * v
            self.average_z += vertices[i][2]

        self.average_z /= len(vertices)

        if glm.distance(self.position, camera.position) < 100 or always_draw:
            screen_vertices = self.screen(self.three_to_two(vertices))
            self.faces = sorted(
                self.faces, 
                key=lambda face: -sum([vertices[j][2] for j in face.vertices]) / face.vertices_length
            )
            for face in self.faces:
                cull = self.calculate_culling(camera.orientation, vertices[face.vertices]) # By fist culling we can save on Z calculations
                if cull < 0:
                    self.render_face(display, face, vertices, old_vertices, light, screen_vertices, camera)

class ModelRenderer:
    def __init__(self, camera):
        self.camera = camera
        self.models = []
        self.light = glm.normalize(glm.vec3(-1, -1, -1))

    def add_model(self, model):
        self.models.append(model)

    def remove_model(self, model):
        self.models.pop(self.models.index(model))
    
    def render_model(self, model, renderer, matrix):
        model.average_z = 0
        model.render(renderer, matrix, self.light, self.camera)

    def sort_models(self):
        self.models = sorted(self.models, key=lambda model: -model.average_z)

    def update_camera(self):
        return self.camera.update()

    def draw(self, renderer): #Mostly a convinece function, user will probably want to have a custom updater.
        matrix = self.update_camera()
        self.sort_models()

        for model in self.models:
            self.render_model(model, renderer, matrix)