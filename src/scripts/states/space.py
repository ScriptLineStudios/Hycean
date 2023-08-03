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
        self.model_renderer = ModelRenderer(self.camera)
        self.camera.orientation = glm.vec3(1, -0.1, -0.02)
        #self.camera.position = glm.vec3(0, 0, 0)
        self.camera.position = glm.vec3(3.1, 1.2, 0)

        self.player = Player(self, "src/assets/models/spaceship/spaceship_high2.obj", "src/assets/models/spaceship/spaceship_high2.mtl")

        self.controller = Controller(self.renderer, ScreenSize)

        self.map = {}

        self.map_texture = pygame.Surface((1000, 1000))
        self.map_texture.fill((0, 0, 0))

        for x in range(10):
            self.planet2 = Planet(self, "src/assets/models/planet/planet.obj", "src/assets/models/planet/planet.mtl")
            x, y = random.randrange(-500, 500), random.randrange(-500, 500)
            self.planet2.position = glm.vec3(x, 0, y)
            self.model_renderer.add_model(self.planet2)

            x += 500
            y += 500
            
            pygame.draw.circle(self.map_texture, (0, 0, 255), (x, y), 4)

        pygame.draw.circle(self.map_texture, (150, 200, 255), (500, 500), 4)
        pygame.image.save(self.map_texture, "map.png")

        self.model_renderer.add_model(self.player)

        self.SpaceParticles = SpaceParticles((1000, 800), self.renderer, 100)

    def update(self):
        self.controller.update()

        self.player.position = copy(self.camera.position)

        direction = glm.vec3(
            self.camera.orientation[0], 
            self.camera.orientation[1],
            self.camera.orientation[2]
            )

        self.player.position.x -= direction[0] * 3.4
        self.player.position.y -= direction[1] * 1.4 + 2
        
        self.player.position.z -= direction[2] * 2

    def render(self):
        self.map_texture.fill((100, 100, 100))
        self.renderer.draw_color = (0, 0, 0, 255)
        self.renderer.clear()

        pygame.draw.circle(self.map_texture, (150, 200, 255), (self.camera.position.x + 500, self.camera.position.z + 500), 15)
        pygame.draw.line(self.map_texture, (150, 200, 255), (self.camera.position.x + 500, self.camera.position.z + 500), 
        (self.camera.position.x + 500 - self.camera.orientation.x * 100, self.camera.position.z + 500 - self.camera.orientation.z * 100), 5)

        self.renderer.blit(self.background_image, pygame.Rect(0, 0, 1000, 800))

        matrix = self.model_renderer.update_camera()
        self.model_renderer.sort_models()

        self.SpaceParticles.render(matrix, self.camera)

        for model in self.model_renderer.models:
            self.model_renderer.render_model(model, self.renderer, matrix)

            if type(model) == Planet:
                pygame.draw.circle(self.map_texture, (0, 0, 255), (model.position.x + 500, model.position.z + 500), 15)

        self.controller.draw_debug()

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
