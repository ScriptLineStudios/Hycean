from .state import State
from src.scripts.entities.player import Player
from src.scripts.entities.planet import Planet
from src.scripts.entities.entity import Entity
from src.scripts.entities.asteroid import Asteroid
from src.scripts.particles import SpaceParticles
from src.scripts.controller import Controller
from src.scripts.land_indicator import LandIndicator

from copy import copy
import random

import pygame
pygame.font.init()

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

        self.font = pygame.font.Font("src/assets/yoster.ttf", 32)

        self.map = {}

        self.map_texture = pygame.Surface((1000, 1000))
        self.map_texture.fill((0, 0, 0))

        self.obstacles = []
        self.controller = Controller(self, self.renderer, ScreenSize)

        for x in range(15):
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

        self.LandIndicator = LandIndicator(self.renderer, ScreenSize)

        self.SpaceParticles = SpaceParticles((1000, 800), self.renderer, 100)
        self.moving = False
        self.acceleration = 0

        self.game_over = False

    def update(self):
        self.controller.update()

        if self.moving:
            self.acceleration = min(self.acceleration + 0.1, 2)
        else:
            self.acceleration = max(self.acceleration - 0.01, 0)


        playerPos = copy(self.camera.position)
        playerPos.x -= glm.normalize(self.camera.orientation).x * 1.5
        playerPos.z -= glm.normalize(self.camera.orientation).z * 1.5
        playerPos.y -= glm.normalize(self.camera.orientation).y * 1

        self.player.update(playerPos)

        self.camera.position.x -= glm.normalize(self.camera.orientation).x / 7 * self.acceleration
        self.camera.position.z -= glm.normalize(self.camera.orientation).z / 7 * self.acceleration
        self.camera.position.y -= glm.normalize(self.camera.orientation).y / 5 * self.acceleration


        if random.randrange(0, 400) == 4:
            x, y = random.randrange(15, 30), 0
            asteroid = Asteroid(self)
            asteroid.position = glm.vec3(self.camera.position.x - glm.normalize(self.camera.orientation).x * x, 0, self.camera.position.z - glm.normalize(self.camera.orientation).z * x)
            direction = glm.normalize(asteroid.position - self.camera.position)
            asteroid.direction = -direction / 10

            self.obstacles.append(asteroid)
            self.model_renderer.add_model(asteroid)

        self.player.rot_x += -self.player.rot_x / 50
        self.player.rot_z += -self.player.rot_z / 50

        self.LandIndicator.planet = None
        for obstacle in self.obstacles:
            if type(obstacle) == Planet:
                obstacleRect = copy(obstacle.rect)
                
                if self.player.rect.collide_rect(obstacleRect):
                    diffVec = pygame.Vector3(self.player.rect.position) - obstacleRect.center
                    distance = diffVec.length()

                    self.LandIndicator.update_planet(obstacle, distance)

            if type(obstacle) == Asteroid:
                obstacleRect = copy(obstacle.rect)
                diffVec = pygame.Vector3(self.player.rect.center) - obstacleRect.center
                distance = diffVec.length()

                if distance < 2.5:
                    print('collision')

        

    def render(self):
        self.map_texture.fill((10, 10, 10))
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
             
            if type(model) == Asteroid:
                model.lifetime -= 1
                if model.lifetime <= 0:
                    self.model_renderer.remove_model(model)
                    
            if type(model) == Planet:
                if glm.distance(model.position, self.camera.position) < 30:
                    surf = pygame.Surface((40, 40))
                    surf.fill((0, 0, 255))

                pygame.draw.circle(self.map_texture, model.type, (model.position.x + 500, model.position.z + 500), 15)

        self.LandIndicator.draw()

        # self.player.position_matrix = self.pos
        # self.player.rotation_matrix = self.rot

        # text = self.font.render("""Needed Materials\nXenthium Alloy\nStarsteel Composite\nQuasarium Plating\nNebulonite Core\nIonite Infused Titanium\nGalaxyrium Mesh\nPlasma-forged Exoalloy\nCelestium Reinforcements\nVoidium Matrix\nMeteorium Resonators""", False, (255, 255, 255))
        # self.renderer.blit(pygame._sdl2.Texture.from_surface(self.renderer, text), pygame.Rect(0, 210, text.get_width(), text.get_height()))
        self.renderer.blit(pygame._sdl2.Texture.from_surface(self.renderer, self.map_texture), pygame.Rect(0, 0, 200, 200))

    def handle_event(self, event):
        self.controller.handle_event(event)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.game_over = True
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pygame.mouse.set_pos((500, 400))
                pygame.mouse.set_visible(self.camera.hidden)
                self.camera.hidden = not self.camera.hidden

            if event.button == 3:
                self.moving = True

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:
                self.moving = False
