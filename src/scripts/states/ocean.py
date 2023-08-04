from .state import State
from src.scripts.entities.player import Player
from src.scripts.entities.planet import Planet
from src.scripts.entities.entity import Entity
from src.scripts.entities.asteroid import Asteroid
from src.scripts.particles import SpaceParticles
from src.scripts.controller import Controller
import math

import pygame_shaders

from copy import copy
import random

import opensimplex

import pygame
pygame.font.init()

class Enemy:
    def __init__(self, scene, position, shader):
        self.scene = scene
        self.position = position
        self.shader = shader

    def update(self):
        self.scene.surface.blit(pygame.transform.flip(self.image, bool(self.position.x < self.scene.player.position.x), False), self.position - self.scene.camera)

class Eel(Enemy):
    def __init__(self, scene, position):
        self.image = pygame.image.load("src/assets/eel.png")

        shader = pygame_shaders.Shader(pygame_shaders.DEFAULT_VERTEX_SHADER, pygame_shaders.DEFAULT_FRAGMENT_SHADER, self.image)
        self.speed = 0.5
        super().__init__(scene, position, shader)

    def update(self):
        direction = (self.position - self.scene.player.position).normalize()
        self.position -= direction * self.speed

        super().update()

class Missle:
    def __init__(self, scene, position, direction, angle):
        print(direction)
        self.scene = scene
        self.position = position
        self.direction = direction
        self.speed = 5
        self.missile = pygame.image.load("src/assets/missle.png")
        self.angle = ((180 / math.pi) * -angle)
        self.cached_particle_surfaces = {}

        size = 7
        if (size, size) not in self.cached_particle_surfaces.keys():
            surf = pygame.Surface((size, size))
            surf.set_colorkey((0, 0, 0))
            pygame.draw.circle(surf, (0, 0, 255), (size / 2, size / 2), size / 2, 2)
            self.cached_particle_surfaces[(size, size)] = surf

        s = self.cached_particle_surfaces[(size, size)] 

    def rot_center(image, angle, x, y):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

        return rotated_image, new_rect

    def update(self):
        self.position += self.direction * self.speed
        # img, rect = self.rot_center(self.missile, self.angle, *(self.position - self.scene.camera))
        self.scene.surface.blit(pygame.transform.rotate(self.missile, self.angle), self.position - self.scene.camera)

        if random.randrange(0, 5) == 1:
            s = self.cached_particle_surfaces[(7, 7)]
            self.scene.particles.append(Particle(self.scene, pygame.Vector2(self.position.x, self.position.y + 16), (0, -1), s))

class Tile:
    def __init__(self, scene, surface, position):
        self.scene = scene
        self.surface = surface
        self.position = position

    def update(self):
        self.scene.surface.blit(self.surface, self.position - self.scene.camera)

class Particle:
    def __init__(self, scene, position, veclocity, surface):
        self.scene = scene
        self.position = position
        self.veclocity = veclocity
        self.surface = surface

    def update(self):
        self.position += self.veclocity
        self.scene.surface.blit(self.surface, self.position - self.scene.camera)

class Player:
    def __init__(self, scene):
        self.scene = scene
        self.player_img = pygame.image.load("src/assets/player.png")

        self.rect = pygame.Rect(250, 200, 32, 32)
        self.flipped = False

        self.cached_particle_surfaces = {}

    @property
    def position(self):
        return pygame.Vector2(self.rect.x, self.rect.y)

    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.rect.x += 1
            self.flipped = False
        if keys[pygame.K_a]:
            self.rect.x -= 1
            self.flipped = True

        if keys[pygame.K_s]:
            self.rect.y += 1
        if keys[pygame.K_w]:
            self.rect.y -= 1

    def render(self):
        if random.randrange(0, 10) == 1:
            size = random.randrange(6, 15)
            if (size, size) not in self.cached_particle_surfaces.keys():
                surf = pygame.Surface((size, size))
                surf.set_colorkey((0, 0, 0))
                pygame.draw.circle(surf, (0, 0, 255), (size / 2, size / 2), size / 2, 2)
                self.cached_particle_surfaces[(size, size)] = surf

            s = self.cached_particle_surfaces[(size, size)] 

            self.scene.particles.append(Particle(self.scene, pygame.Vector2(self.rect.x + 32 * int(self.flipped), self.rect.y + 16), (0, -1), s))

        self.scene.surface.blit(pygame.transform.flip(self.player_img, self.flipped, False), (self.rect.x - self.scene.camera.x, self.rect.y - self.scene.camera.y))

class Ocean(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.player = Player(self)

        self.colors = {
            "blue": (0, 27, 63, 255),
            "red": (100, 20, 10, 255),
            "green": (40, 200, 60, 255)
        }

        self.time = 0

        self.screen_shake = 0

        self.color = "blue"

        self.surface = pygame.Surface((500, 400))
        self.particles = []
        self.missiles = []

        self.rock = pygame.transform.scale(pygame.image.load("src/assets/rock.png"), (32, 32))
        self.rock.set_colorkey((255, 255, 255))

        self.chunks = {}
        self.splash_speed = 0.003

        self.camera = pygame.Vector2(0, 0)

        self.screen_shader = pygame_shaders.Shader(pygame_shaders.DEFAULT_VERTEX_SHADER, "src/assets/shaders/fragment.glsl", self.surface)

        self.water_surface = pygame.Surface((100, 100))
        self.water_surface.fill((255, 0, 0))
        self.water_shader = pygame_shaders.Shader(pygame_shaders.DEFAULT_VERTEX_SHADER, "src/assets/shaders/water.glsl", self.water_surface)

        self.enemies = [Eel(self, pygame.Vector2(10, 10))]

        blocks = []
        for x in range(32):
            for y in range(32):
                val = opensimplex.noise2(x / 32, y / 32)

                if val < -0.4:
                    blocks.append(Tile(self, self.rock, pygame.Vector2(x * 32, y * 32)))   

        self.chunks[(0, 0)] = blocks 

    def update(self):
        self.player.update()

    def render(self):
        self.renderer.draw_color = self.colors[self.color]
        self.renderer.clear()
        self.surface.fill(self.colors[self.color])

        self.camera += (pygame.Vector2(self.player.rect.x, self.player.rect.y) - self.camera - pygame.Vector2(250, 200)) / 5

        for block in self.chunks[(0, 0)]:
            block.update()

        for missile in self.missiles:
            missile.update()

        for particle in self.particles:
            particle.update()

        for enemy in self.enemies:
            enemy.update()

        self.screen_shader.send("time", self.time)
        self.screen_shader.send("speed", self.splash_speed)

        self.splash_speed = max(self.splash_speed - 0.0001, 0.003)
        print(self.splash_speed)

        self.water_shader.send("time", self.time)

        self.player.render()
        self.time += 0.01
        # self.surface = self.shader.render_direct()
        dx, dy = 0, 0
        if self.screen_shake > 0:
            self.camera.x += random.uniform(-8, 8)
            self.camera.y += random.uniform(-8, 8)

            self.screen_shake -= 1
            
        self.screen_shader.render_direct(pygame.Rect(dx, dy, 1000, 800))
        self.renderer.blit(pygame._sdl2.Texture.from_surface(self.renderer, pygame.transform.flip(self.surface, False, True)), pygame.Rect(dx, dy, 1000, 800))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mp = pygame.Vector2(pygame.mouse.get_pos()) / 2
                player = pygame.Vector2(self.player.rect.x, self.player.rect.y)
                direction = (mp - player)
                self.missiles.append(Missle(self, player, direction.normalize(), math.atan2(direction.y, direction.x)))
                self.screen_shake = 50
                self.time += 0.5
                self.splash_speed += 0.009

    