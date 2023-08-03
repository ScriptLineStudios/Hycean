from .state import State
from src.scripts.entities.player import Player
from src.scripts.entities.planet import Planet
from src.scripts.entities.entity import Entity
from src.scripts.particles import SpaceParticles
from src.scripts.controller import Controller

from copy import copy
import random

import glm

from pygame_3d import *

# make separate class for 3D and 2D part of the game
class Space(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        #put actual here
        ScreenSize = (1000, 800)

        self.background_image = pygame.image.load("src/assets/Space Background.png")
        self.background_image = pygame._sdl2.Texture.from_surface(self.renderer, self.background_image)

        self.camera = Camera()
        self.original_matrix = None

        self.model_renderer = ModelRenderer(self.camera)
        self.camera.orientation = glm.vec3(1, -0.1, -0.02)
        #self.camera.position = glm.vec3(0, 0, 0)
        self.cam_target_position = glm.vec3(3.1, 1.2, 0)
        self.camera.position = self.cam_target_position
        self.last_orientation = glm.vec3(0, 0,0)

        self.player = Player(self, "src/assets/models/spaceship/spaceship_high2.obj", "src/assets/models/spaceship/spaceship_high2.mtl")


        self.map = {}

        self.map_texture = pygame.Surface((1000, 1000))
        self.map_texture.fill((0, 0, 0))

        self.obstacles = []
        self.controller = Controller(self, self.renderer, ScreenSize)

        for x in range(10):
            self.planet2 = Planet(self, "src/assets/models/planet/planet.obj", "src/assets/models/planet/planet.mtl")
            x, y = random.randrange(-500, 500), random.randrange(-500, 500)
            self.planet2.position = glm.vec3(x, 0, y)
            self.model_renderer.add_model(self.planet2)
            self.obstacles.append(self.planet2)

            x += 500
            y += 500
            
            pygame.draw.circle(self.map_texture, (0, 0, 255), (x, y), 4)

        pygame.draw.circle(self.map_texture, (150, 200, 255), (500, 500), 4)
        pygame.image.save(self.map_texture, "map.png")

        self.model_renderer.add_model(self.player)

        self.SpaceParticles = SpaceParticles((1000, 800), self.renderer, 100)

    def update(self):
        self.controller.update()

        self.player.update()
        self.camera.position.x -= glm.normalize(self.camera.orientation).x / 3
        self.camera.position.z -= glm.normalize(self.camera.orientation).z / 3
        self.camera.position.y -= glm.normalize(self.camera.orientation).y / 5

        # self.player.position.x = (self.camera.position.x - self.camera.orientation.x * 2) - 1
        # self.player.position.z = (self.camera.position.z - self.camera.orientation.z * 2)
        # self.player.position.y = self.camera.position.y - 2
        # keys = pygame.key.get_pressed()

        # if keys[pygame.K_d]:
        #     self.player.rot_x += 1
        #     self.camera.orientation = glm.rotate(self.camera.orientation, glm.radians(0.5), self.camera.up)

        # if keys[pygame.K_a]:
        #     self.player.rot_x -= 1
        #     self.camera.orientation = glm.rotate(self.camera.orientation, glm.radians(-0.5), self.camera.up)

        # if keys[pygame.K_w]:
        #     self.player.rot_z -= 1
        #     self.camera.position.y += 0.4

        # if keys[pygame.K_s]:
        #     self.player.rot_z += 1
        #     self.camera.position.y -= 0.4

        self.player.rot_x += -self.player.rot_x / 100
        self.player.rot_z += -self.player.rot_z / 100

        for obstacle in self.obstacles:
            obstacleRect = copy(obstacle.rect)
            
            if self.player.rect.collide_rect(obstacleRect):
                print('Player - Planet collision detected')

    def render(self):
        self.map_texture.fill((100, 100, 100))
        self.renderer.draw_color = (0, 0, 0, 255)
        self.renderer.clear()

        pygame.draw.circle(self.map_texture, (150, 200, 255), (self.camera.position.x + 500, self.camera.position.z + 500), 15)
        pygame.draw.line(self.map_texture, (150, 200, 255), (self.camera.position.x + 500, self.camera.position.z + 500), 
        (self.camera.position.x + 500 - self.camera.orientation.x * 100, self.camera.position.z + 500 - self.camera.orientation.z * 100), 5)

        self.renderer.blit(self.background_image, pygame.Rect(0, 0, 1000, 800))

        self.last_orientation = glm.vec3(self.camera.orientation.x, self.camera.orientation.y, self.camera.orientation.z) 
        matrix = self.model_renderer.update_camera()
        if self.original_matrix is None:
            self.original_matrix = matrix

        self.model_renderer.sort_models()
        # self.SpaceParticles.render(matrix, self.camera)


        for model in self.model_renderer.models:
            if type(model) != Player:
                self.model_renderer.render_model(model, self.renderer, matrix)
            else:
                self.model_renderer.render_model(model, self.renderer, self.original_matrix)

            if type(model) == Planet:
                pygame.draw.circle(self.map_texture, (0, 0, 255), (model.position.x + 500, model.position.z + 500), 15)

        # self.player.position_matrix = self.pos
        # self.player.rotation_matrix = self.rot


        self.renderer.blit(pygame._sdl2.Texture.from_surface(self.renderer, self.map_texture), pygame.Rect(0, 0, 200, 200))

    def handle_event(self, event):
        self.controller.handle_event(event)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pygame.mouse.set_pos((500, 400))
                pygame.mouse.set_visible(self.camera.hidden)
                self.camera.hidden = not self.camera.hidden

            if event.button == 2:
                print(self.camera.position)
                print(self.camera.orientation)
