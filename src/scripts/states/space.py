from .state import State
from src.scripts.entities.player import Player
from src.scripts.entities.planet import Planet
from src.scripts.entities.entity import Entity
from src.scripts.entities.asteroid import Asteroid
from src.scripts.particles import Stars, JetFlame
from src.scripts.controller import Controller
from src.scripts.land_indicator import LandIndicator
from src.scripts.audio_handler import AudioHandler
from src.scripts.tutorial import Tutorial
from src.scripts.states import Ocean

from copy import copy
import random

import pygame
from pygame.locals import *

pygame.font.init()

import glm

from pygame_3d import *

# make separate class for 3D and 2D part of the game
class Space(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ScreenSize = (1000, 800)
        
        self.music = pygame.mixer.music.load("src/sfx/ambientspacemusic.mp3")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)

        self.engine_sound = AudioHandler.sounds['engine']
        self.engine_sound.set_volume(0.4)

        self.land_sound = AudioHandler.sounds['land']
        self.land_sound.set_volume(0.4)
        #put actual here

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
        self.controller = Controller(self, self.renderer, self.ScreenSize)

        for x in range(15):
            self.planet2 = Planet(self, "src/assets/models/planet/planet.obj", "src/assets/models/planet/planet.mtl")
            self.planet2.id = x
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

        self.LandIndicator = LandIndicator(self.renderer, self.ScreenSize)

        self.Stars = Stars(self.ScreenSize, self.renderer, 100)
        self.JetFlame = JetFlame(self.ScreenSize, self.renderer)
        self.moving = False
        self.acceleration = 0

        self.Tutorial = Tutorial(self.renderer, self.app)

        self.game_over = False
        self.cutscene = False
        self.cutscene_surface = pygame.Surface((500, 400), pygame.SRCALPHA)
        self.cutscene_surface.fill((0, 0, 0, 0))
        self.cutscene_size = 1

        self.gps = None
        self.t = 0
        self.cutscene_complete = False

    def update_player_rect(self):
        playerPos = pygame.Vector3(self.camera.position)

        orientation = pygame.Vector3(
            glm.normalize(self.camera.orientation)
        )

        up = pygame.Vector3(0, 1, 0)
        right = orientation.copy()
        right = right.cross(up)

        playerPos -= orientation * 5

        return playerPos

    def update(self):
        self.controller.update()

        if self.moving:
            self.acceleration = min(self.acceleration + 0.1, 2)
        else:
            self.acceleration = max(self.acceleration - 0.005, 0)


        self.camera.position.x -= glm.normalize(self.camera.orientation).x / 7 * self.acceleration
        self.camera.position.z -= glm.normalize(self.camera.orientation).z / 7 * self.acceleration
        self.camera.position.y -= glm.normalize(self.camera.orientation).y / 5 * self.acceleration

        playerPos = self.update_player_rect()

        #playerPos.x -= glm.normalize(self.camera.orientation).x * 5
        #playerPos.z -= glm.normalize(self.camera.orientation).z * 5
        #playerPos.y -= glm.normalize(self.camera.orientation).y * 5

        #playerPos.z += 0.5
        #playerPos.y -= 3

        # if self.moving:
            # self.JetFlame.add_particle(playerPos)

        self.player.update(playerPos)
        
        if self.Tutorial.finished:
            if random.randrange(0, 200) == 4:
                #print("asteroid")
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

            elif type(obstacle) == Asteroid:
                if not self.cutscene:
                    distance = glm.distance2(obstacle.position, (self.camera.position))
                    if distance < 0.4:
                        self.GameOverSwitch(obstacle)


    def GameOverSwitch(self, obstacle):
        self.engine_sound.fadeout(40)
        app = self.app
        app.crnt_state = 'game_over'
        app.state = app.states[app.crnt_state]
        app.state.update_screen()
        self.obstacles.remove(obstacle)

    def restart(self):
        # when "R" is pressed in game over state, calls this function
        self.model_renderer = ModelRenderer(self.camera)
        self.camera.orientation = glm.vec3(1, -0.1, -0.02)

        self.cam_target_position = glm.vec3(3.1, 1.2, 0)
        self.camera.position = self.cam_target_position
        self.last_orientation = glm.vec3(0, 0,0)

        self.obstacles = []
        self.model_renderer.models.clear()

        self.model_renderer.add_model(self.player)

        self.JetFlame.clear()

        self.camera.acceleration *= 0
        self.camera.velocity *= 0

        self.gps = None
        self.app.needed_resources = copy(self.app.needed_resources_stable)

        for x in range(15):
            self.planet2 = Planet(self, "src/assets/models/planet/planet.obj", "src/assets/models/planet/planet.mtl")
            self.planet2.id = x
            x, y = random.randrange(-500, 500), random.randrange(-500, 500)
            self.planet2.position = glm.vec3(x, 0, y)
            self.model_renderer.add_model(self.planet2)
            self.obstacles.append(self.planet2)

            x += 500
            y += 500
            
            pygame.draw.circle(self.map_texture, (0, 0, 255), (x, y), 4)

        self.LandIndicator = LandIndicator(self.renderer, self.ScreenSize)

    def render(self):
        self.t += 1
        self.map_texture.fill((10, 10, 10))
        self.renderer.draw_color = (0, 0, 0, 255)
        self.renderer.clear()

        pygame.draw.circle(self.map_texture, (150, 200, 255), (self.camera.position.x + 500, self.camera.position.z + 500), 15)
        pygame.draw.line(self.map_texture, (150, 200, 255), (self.camera.position.x + 500, self.camera.position.z + 500), 
        (self.camera.position.x + 500 - self.camera.orientation.x * 100, self.camera.position.z + 500 - self.camera.orientation.z * 100), 5)

        self.last_orientation = glm.vec3(self.camera.orientation.x, self.camera.orientation.y, self.camera.orientation.z) 
        matrix = self.model_renderer.update_camera()
        if self.original_matrix is None:
            self.original_matrix = matrix

        self.model_renderer.sort_models()
        self.Stars.render(matrix)

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
        
        if self.gps is not None:
            pygame.draw.line(self.map_texture, (0, 200, 0), (self.camera.position.x + 500, self.camera.position.z + 500), self.gps, 9)

        self.JetFlame.render(matrix)

        self.LandIndicator.draw()

        if self.cutscene:
            self.cutscene_size += (self.cutscene_size / 16)
            if self.cutscene_size > 2000:
                self.cutscene_complete = True
            pygame.draw.circle(self.cutscene_surface, (255, 255, 255), (250, 200), self.cutscene_size)
            self.renderer.blit(pygame._sdl2.Texture.from_surface(self.renderer, self.cutscene_surface), pygame.Rect(0, 0, 1000, 800))

        if self.cutscene_complete:
            ocean = None
            if not (ocean := self.app.oceans.get(self.LandIndicator.planet.primary_material[0], False)):
                ocean = Ocean(self.app, self.renderer, color=self.LandIndicator.planet.type, material=self.LandIndicator.planet.primary_material[0])
                self.app.oceans[self.LandIndicator.planet.primary_material[0]] = ocean

            self.app.states[f"ocean_{self.LandIndicator.planet.id}"] = ocean
            self.app.crnt_state = f"ocean_{self.LandIndicator.planet.id}"
            
            self.app.current_resource = self.LandIndicator.planet.primary_material[0]

            self.cutscene = False
            self.cutscene_surface = pygame.Surface((500, 400), pygame.SRCALPHA)
            self.cutscene_surface.fill((0, 0, 0, 0))
            self.cutscene_size = 1
            self.cutscene_complete = False
    
            self.camera.hidden = False

            pygame.mouse.set_visible(True)

            self.app.state = self.app.states[self.app.crnt_state]
            self.app.state.start()

        self.Tutorial.draw()

        text = self.font.render(f"x: {int(self.camera.position.x)} y: {int(self.camera.position.y)} z: {int(self.camera.position.z)}", False, (255, 255, 255))
        self.renderer.blit(pygame._sdl2.Texture.from_surface(self.renderer, text), pygame.Rect(0, 210, text.get_width(), text.get_height()))
        self.renderer.blit(pygame._sdl2.Texture.from_surface(self.renderer, self.map_texture), pygame.Rect(0, 0, 200, 200))

    def handle_event(self, event):
        self.controller.handle_event(event)
        self.Tutorial.handle_event(event)

        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                self.game_over = True

            if event.key == K_RETURN:
                if self.LandIndicator.planet is not None:
                    #print(f"Its cutscene time {self.LandIndicator.planet}")
                    self.cutscene = True
                    self.camera.hidden = False

                    pygame.mouse.set_visible(True)
                    
                    self.land_sound.play()
                    for obstacle in self.obstacles[:]:
                        if type(obstacle) == Asteroid:
                            self.obstacles.remove(obstacle)

            if event.key == K_ESCAPE:
                pygame.mouse.set_visible(self.camera.hidden)
                self.camera.hidden = not self.camera.hidden
            
            if event.key == K_LSHIFT:
                self.engine_sound.play(-1)
                self.moving = True

        if event.type == KEYUP:
            if event.key == K_LSHIFT:
                self.engine_sound.fadeout(40)
                self.moving = False

        if event.type == MOUSEBUTTONDOWN:
            mp = pygame.mouse.get_pos()
            if event.button == 1 and mp[0] < 700:
                pygame.mouse.set_pos((500, 400))
                pygame.mouse.set_visible(self.camera.hidden)
                self.camera.hidden = not self.camera.hidden

            if event.button == 3:
                self.engine_sound.play(-1)
                self.moving = True

        elif event.type == MOUSEBUTTONUP:
            if event.button == 3:
                self.engine_sound.fadeout(40)
                self.moving = False
