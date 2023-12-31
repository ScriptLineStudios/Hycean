from .state import State
from src.scripts.states import *

from src.scripts.entities.player import Player
import math
import time

from src.scripts.audio_handler import AudioHandler

import random

import opensimplex
opensimplex.seed(int(time.time()))

import pygame
pygame.font.init()



class Chest:
    def __init__(self, scene, position):
        self.scene = scene
        self.position = position
        self.rect = pygame.Rect(*self.position, 32, 32)
        self.image = pygame.image.load("src/assets/chest.png")

    def update(self):
        self.scene.surface.blit(self.image, self.position - self.scene.camera)

class EnemyBullet:
    def __init__(self, scene, position, direction):
        self.scene = scene
        self.position = position
        self.direction = direction
        self.image = pygame.image.load("src/assets/bullet.png")
        self.lifetime = 100

        size = (self.lifetime / 100) * 16
        self.cache = self.scene.glow(size * 2)

    def render(self):
        self.lifetime -= 0.1

        size = (self.lifetime / 100) * 16

        self.scene.lighting.blit(self.cache, self.position - self.scene.camera + pygame.Vector2(-5, -4), special_flags=pygame.BLEND_RGBA_ADD)

        self.position += self.direction * 2
        self.scene.surface.blit(self.image, self.position - self.scene.camera)

        if pygame.Rect(*self.position, 16, 16).colliderect(self.scene.player.rect):
            self.scene.player.take_damage(1)
            self.lifetime = -1

class Enemy:
    def __init__(self, scene, position, shader, images):
        self.scene = scene
        self.position = position
        self.shader = shader
        self.images = images
        self.originals = self.images.copy()
        self.index = 0
        self.health = 50
        self.cooldown = 0
        self.direction = pygame.Vector2(0, 0)
        self.flipped_y = False
        self.death_rotation = 0

    @staticmethod
    #Kindly borrowed from https://github.com/pygame-community/pygame-ce/issues/1847#issuecomment-1445321115
    def solid_overlay(surf, overlay_color=(255, 255, 255)):
        return pygame.mask.from_surface(surf).to_surface(setcolor=overlay_color,
                                                 unsetcolor=(0, 0, 0, 0))

    def take_damage(self, damage, missile):
        self.health -= damage
        AudioHandler.sounds["hurt"].play()
        sx, sy = self.images[self.index // 8].get_size()
        for x in range(20):
            subsurf = self.images[self.index // 8].subsurface(random.randrange(0, sx - 5), random.randrange(0, sy - 5), 4, 4)
            self.scene.particles.append(Particle(self.scene, self.position.copy(), pygame.Vector2(missile.direction.x + random.normalvariate(0, 0.7), missile.direction.y + random.normalvariate(0, 0.7)), subsurf))
        self.cooldown = 4
        for i, image in enumerate(self.images):
            self.images[i] = self.solid_overlay(image)
        self.direction = missile.direction

        try:
            if random.randrange(0, 5) == 2:
                self.scene.particles.append(Material(self.scene.material, self.scene, self.position.copy(), -pygame.Vector2(self.direction.x + random.normalvariate(0, 0.3), self.direction.y + random.normalvariate(0, 0.3)), None))
        except:
            pass

    def update(self):
        if self.cooldown > 0:
            self.position += self.direction * 10
            self.cooldown -= 1
            if self.cooldown == 1:
                for i, image in enumerate(self.images):
                    self.images[i] = self.originals[i]
        self.index += 1
        if self.index > len(self.images) * 8 - 1: 
            self.index = 0
        self.scene.surface.blit(pygame.transform.flip(self.images[self.index // 8], bool(self.position.x < self.scene.player.position.x), self.flipped_y), self.position - self.scene.camera)        

class Octo(Enemy):
    def __init__(self, scene, position):
        self.image = pygame.image.load("src/assets/anglerfish.png")

        self.speed = 1.5
        self.reverse = 1
        self.timeout = 0

        self.images = [pygame.image.load("src/assets/octo1.png"), pygame.image.load("src/assets/octo2.png"), pygame.image.load("src/assets/octo3.png")]
        self.index = 0

        super().__init__(scene, position, None, self.images)

    def update(self):
        direction = (self.position - self.scene.player.position).normalize()
        rect = pygame.Rect(*(self.position), 32, 16)
        if self.reverse == 1:
            if rect.colliderect(self.scene.player.rect):
                self.scene.player.take_damage(5)
                self.reverse = -1
                self.timeout = 50

        if self.timeout > 0:
            self.timeout -= 1
        else:
            self.reverse = 1

        self.position -= self.reverse * (direction) * self.speed

        self.flipped_y = bool(self.position.y > self.scene.player.position.y)

        if random.randrange(0, 100) == 5:
            self.scene.enemy_bullets.append(EnemyBullet(self.scene, self.position.copy(), (self.scene.player.position - self.position).normalize()))

        super().update()


class Anglerfish(Enemy):
    def __init__(self, scene, position):
        self.image = pygame.image.load("src/assets/anglerfish.png")

        self.speed = 0.8
        self.reverse = 1
        self.timeout = 0

        self.images = [pygame.image.load("src/assets/anglerfish1.png"), pygame.image.load("src/assets/anglerfish2.png"), pygame.image.load("src/assets/anglerfish3.png")]
        self.index = 0
        super().__init__(scene, position, None, self.images)

        self.s = self.scene.glow(100)

    def update(self):
        direction = (self.position - self.scene.player.position).normalize()
        rect = pygame.Rect(*(self.position), 32, 16)
        if self.reverse == 1:
            if rect.colliderect(self.scene.player.rect):
                self.scene.player.take_damage(5)
                self.reverse = -1
                self.timeout = 50

        if self.timeout > 0:
            self.timeout -= 1
        else:
            self.reverse = 1

        self.position -= self.reverse * direction * self.speed

        self.scene.lighting.blit(self.s, self.position - self.scene.camera + pygame.Vector2(-37, -37), special_flags=pygame.BLEND_RGBA_ADD)

        super().update()

class Blob(Enemy):
    def __init__(self, scene, position):
        self.image = pygame.image.load("src/assets/eel.png")

        self.speed = 2.0
        self.reverse = 1
        self.timeout = 0

        self.images = [pygame.image.load("src/assets/blob1.png"), pygame.image.load("src/assets/blob2.png"), pygame.image.load("src/assets/blob3.png")]
        self.index = 0
        super().__init__(scene, position, None, self.images)

    def update(self):
        self.direction_offset = pygame.Vector2(random.uniform(-3, 3), random.uniform(-3, 3))
        direction = (self.position - (self.scene.player.position + self.direction_offset)).normalize()

        rect = pygame.Rect(*(self.position), 32, 16)
        if self.reverse == 1:
            if rect.colliderect(self.scene.player.rect):
                self.scene.player.take_damage(5)
                self.reverse = -1
                self.timeout = random.randrange(40, 70)

        if self.timeout > 0:
            self.timeout -= 1
        else:
            self.reverse = 1

        self.position -= self.reverse * direction * self.speed

        super().update()

class Eel(Enemy):
    def __init__(self, scene, position):
        self.image = pygame.image.load("src/assets/eel.png")

        self.speed = 0.5
        self.reverse = 1
        self.timeout = 0

        self.images = [pygame.image.load("src/assets/eel-sheet1.png"), pygame.image.load("src/assets/eel-sheet2.png"), pygame.image.load("src/assets/eel-sheet3.png")]
        self.index = 0
        super().__init__(scene, position, None, self.images)

    def update(self):
        direction = (self.position - self.scene.player.position).normalize()

        rect = pygame.Rect(*(self.position), 32, 16)
        if self.reverse == 1:
            if rect.colliderect(self.scene.player.rect):
                self.scene.player.take_damage(5)
                self.reverse = -1
                self.timeout = 50

        if self.timeout > 0:
            self.timeout -= 1
        else:
            self.reverse = 1

        self.position -= self.reverse * direction * self.speed

        super().update()

class Missle:
    def __init__(self, scene, position, direction, angle):
        #print(direction)
        self.scene = scene
        self.position = position
        self.direction = direction
        self.speed = 5
        self.missile = pygame.image.load("src/assets/missle.png")
        self.angle = ((180 / math.pi) * -angle)
        self.cached_particle_surfaces = {}

        self.life_time = 500

        size = 7
        if (size, size) not in self.cached_particle_surfaces.keys():
            surf = pygame.Surface((size, size))
            surf.set_colorkey((0, 0, 0))
            pygame.draw.circle(surf, (162, 220, 199), (size / 2, size / 2), size / 2, 2)
            self.cached_particle_surfaces[(size, size)] = surf

        s = self.cached_particle_surfaces[(size, size)] 

    def rot_center(image, angle, x, y):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

        return rotated_image, new_rect

    def update(self):
        self.life_time -= 1
        self.position += self.direction * self.speed
        # img, rect = self.rot_center(self.missile, self.angle, *(self.position - self.scene.camera))
        self.scene.surface.blit(pygame.transform.rotate(self.missile, self.angle), self.position - self.scene.camera)

        if random.randrange(0, 5) == 1:
            s = self.cached_particle_surfaces[(7, 7)]
            self.scene.particles.append(Particle(self.scene, pygame.Vector2(self.position.x, self.position.y + 16), (0, -1), s))

class Tile:
    def __init__(self, scene, surface, position, material=None):
        self.scene = scene
        self.surface = surface
        self.position = position
        self.rect = pygame.Rect(*self.position, 16, 16)
        self.material = material
        self.remove = False

    def update(self, missiles):
        for missile in missiles:
            if self.rect.colliderect(pygame.Rect(missile.position.x, missile.position.y, 16, 16)):
                missiles.remove(missile)
                self.scene.explosion.set_volume(0.3)
                self.scene.explosion.play()

                sx, sy = self.surface.get_size()
                for i in range(random.randrange(20, 40)):
                    subsurf = self.surface.subsurface(random.randrange(0, sx - 5), random.randrange(0, sy - 5), 4, 4)
                    self.scene.particles.append(Particle(self.scene, pygame.Vector2(self.position.x + 16, self.position.y + 16), -pygame.Vector2(missile.direction.x + random.normalvariate(0, 0.1), missile.direction.y + random.normalvariate(0, 0.1)) * random.randrange(1, 4), pygame.transform.scale(subsurf, (2, 2))))
                
                # self.scene.circles.append([pygame.Vector2(self.position.x + 16, self.position.y + 16), 5])

                if self.material:
                    self.remove = True
                    sx, sy = self.surface.get_size()

                    for x in range(random.randrange(1, 4)):
                        subsurf = self.surface.subsurface(random.randrange(0, sx - 5), random.randrange(0, sy - 5), 4, 4)

                        self.scene.particles.append(Material(self.scene.material, self.scene, self.position.copy(), pygame.Vector2(missile.direction.x + random.normalvariate(0, 0.3), missile.direction.y + random.normalvariate(0, 0.3)), subsurf))

        self.scene.surface.blit(self.surface, self.position - self.scene.camera)

class Particle:
    def __init__(self, scene, position, veclocity, surface):
        self.scene = scene
        self.position = position
        self.veclocity = veclocity
        self.surface = surface
        self.lifetime = random.normalvariate(100, 10)
        self.remove = False

    def update(self):
        self.lifetime -= 1
        self.position += self.veclocity
        self.scene.surface.blit(self.surface, self.position - self.scene.camera)

class Material(Particle):
    def __init__(self, tp, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image = pygame.image.load(f"src/assets/{tp.lower()}.png")
        self.surface = self.image
        self.rotation = 0
        
    def update(self):
        self.rotation += 1
        self.position -= self.veclocity
        self.scene.surface.blit(pygame.transform.rotate(self.image, self.rotation), self.position - self.scene.camera)

        if pygame.Rect(*self.position, 16, 16).colliderect(self.scene.player.rect):
            # self.scene.app.needed_resources_stable[self.scene.material] -= 1
            self.scene.app.collected_materials[self.scene.material] += 1
            self.remove = True
            AudioHandler.sounds["pickup"].set_volume(0.2)
            AudioHandler.sounds["pickup"].play()

class Player:
    def __init__(self, scene):
        self.scene = scene
        self.player_img = pygame.Surface((32, 32), pygame.SRCALPHA)
        img = pygame.image.load("src/assets/player.png")
        self.player_img.blit(img, (0, 0))
        self.original = self.player_img.copy()

        self.rect = pygame.FRect(250, 200, 32, 32)
        self.flipped = False

        self.cached_particle_surfaces = {}

        self.health = 100
        self.max_health = 100
        self.damage = 0
        self.moving = False

        self.acceleration = pygame.Vector2(0, 0)

    @staticmethod
    #Kindly borrowed from https://github.com/pygame-community/pygame-ce/issues/1847#issuecomment-1445321115
    def solid_overlay(surf, overlay_color=(255, 255, 255)):
        return pygame.mask.from_surface(surf).to_surface(setcolor=overlay_color,
                                                 unsetcolor=(0, 0, 0, 0))

    def take_damage(self, amount):
        self.health -= amount
        self.scene.screen_shake += 10
        self.player_img = self.solid_overlay(self.player_img)

        self.scene.splash_speed += 0.01
        self.damage = 5

    @property
    def position(self):
        return pygame.Vector2(self.rect.x, self.rect.y)

    def update(self, tiles):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.acceleration.x += 0.4
            self.flipped = False
            self.moving = True
        if keys[pygame.K_a]:
            self.acceleration.x -= 0.4
            self.flipped = True
            self.moving = True

        if keys[pygame.K_s]:
            self.acceleration.y += 0.4
        if keys[pygame.K_w]:
            self.acceleration.y -= 0.4

        self.rect.x += self.acceleration.x
        index = -1
        if (index := self.rect.collidelist(tiles)) != -1:
            if self.acceleration.x > 0:
                self.rect.right = tiles[index].left
            if self.acceleration.x < 0:
                self.rect.left = tiles[index].right

        self.rect.y += self.acceleration.y
        if (index := self.rect.collidelist(tiles)) != -1:
            if self.acceleration.y > 0:
                self.rect.bottom = tiles[index].top
            if self.acceleration.y < 0:
                self.rect.top = tiles[index].bottom
        
        self.acceleration.x += -self.acceleration.x / 100
        self.acceleration.y += -self.acceleration.y / 100

        self.acceleration.x = pygame.math.clamp(self.acceleration.x, -1.3, 1.3)
        self.acceleration.y = pygame.math.clamp(self.acceleration.y, -1.3, 1.3)

    def render(self):
        if self.damage > 0:
            self.damage -= 1
            if self.damage == 1:
                self.player_img = self.original

        if random.randrange(0, 10) == 1 and self.moving:
            size = random.randrange(6, 15)
            if (size, size) not in self.cached_particle_surfaces.keys():
                surf = pygame.Surface((size, size))
                surf.set_colorkey((0, 0, 0))
                pygame.draw.circle(surf, (162, 220, 199), (size / 2, size / 2), size / 2, 2)
                self.cached_particle_surfaces[(size, size)] = surf

            s = self.cached_particle_surfaces[(size, size)] 

            self.scene.particles.append(Particle(self.scene, pygame.Vector2(self.rect.x + 32 * int(self.flipped), self.rect.y + 16), (0, -2), s))

        self.scene.surface.blit(pygame.transform.flip(
            pygame.transform.scale(self.player_img, (self.player_img.get_width() - abs(self.acceleration.y)*4, self.player_img.get_height() - abs(self.acceleration.x)*4)), 
            self.flipped, False), (self.rect.x - self.scene.camera.x, self.rect.y - self.scene.camera.y))
        self.moving = False


class Ocean(State):
    def __init__(self, *args, material, color="blue", **kwargs):
        super().__init__(*args, **kwargs)
        opensimplex.seed(int(time.time()))

        pygame.mixer.music.fadeout(10)
        pygame.mixer.music.load("src/sfx/music.ogg")
        pygame.mixer.music.play(-1)

        self.player = Player(self)
        self.light = pygame.transform.scale(pygame.image.load("src/assets/light.png"), (100, 90))
        self.material = material
        self.colors = {
            "blue": (0, 27, 63, 255),
            "red": (100, 20, 10, 255),
            "green": (40, 200, 60, 255)
        }

        self.explosion = AudioHandler.sounds['explosion']

        self.resources = [
            "Aluminum",
            "Fiber",
            "Titanium",
            "Bronze",
            "Steel",
            "Silver",
        ]

        self.materials = {x: pygame.image.load(f"src/assets/{x.lower()}_ore.png") for x in self.resources}
        for x in self.materials.keys():
            self.materials[x] = pygame.transform.scale(self.materials[x], (32,32))
            self.materials[x].set_colorkey((255, 255, 255))

        self.time = 0

        self.screen_shake = 0

        self.color = color

        self.surface = pygame.Surface((500, 400))
        self.particles = []
        self.missiles = []

        self.rock = pygame.transform.scale(pygame.image.load("src/assets/rock.png"), (32, 32))
        self.rock.set_colorkey((255, 255, 255))

        self.chunks = {}
        self.splash_speed = 0.003

        self.camera = pygame.Vector2(0, 0)

        self.enemies = [Octo(self, pygame.Vector2(10, 10)), Anglerfish(self, pygame.Vector2(-10, 10))]

        self.enemy_bullets = []
        self.circles = []

        self.chest_spawned = False
        self.potential_positions = []
        self.generate_chunks()

        self.missile_timer = 5
        self.crnt_timer = 0

        self.safety = False
        self.ticks = 0

        self.enemy_choices = {
            "blue": [Anglerfish, Eel, Anglerfish, Eel, Octo],
            "red": [Blob, Blob],
        }

        self.light_index = 0

        self.lighting = pygame.Surface((1000, 800))
        self.lighting.set_colorkey((0, 0, 0))

    def glow(self, size):
        lighting_surface = pygame.Surface((size, size))
        lighting_surface.set_colorkey((0,0,0))
        lighting_surface.blit(pygame.transform.scale(self.light, (size, size)), 
            (0, 0), special_flags=pygame.BLEND_RGBA_ADD)
        return lighting_surface

    def generate_chunks(self):
        for chunk_x in range(-8, 8):
            for chunk_y in range(-8, 8):
                chunk = []
                if chunk_x != 0 and chunk_y != 0:
                    for x in range(16):
                        for y in range(16):
                            col = opensimplex.noise2((x + chunk_x * 16) / 20, (y + chunk_y * 16) / 20)
                            if col > 0.3:
                                if self.material:
                                    ore = opensimplex.noise2(((x + 398479237) + chunk_x * 16) / 20, ((y + 984798327) + chunk_y * 16) / 20)
                                    if ore > 0.1:
                                        chunk.append(Tile(self, self.materials[self.material], pygame.Vector2((x + chunk_x * 16) * 16, (y + chunk_y * 16) * 16), material=self.material))
                                
                                    else:
                                        chunk.append(Tile(self, self.rock, pygame.Vector2((x + chunk_x * 16) * 16, (y + chunk_y * 16) * 16)))
                                else:
                                    chunk.append(Tile(self, self.rock, pygame.Vector2((x + chunk_x * 16) * 16, (y + chunk_y * 16) * 16)))

                self.chunks[(chunk_x, chunk_y)] = chunk

    def update(self):
        pass

    def render(self):
        self.ticks += 1
        self.renderer.draw_color = self.colors[self.color]
        self.renderer.clear()
        self.surface.fill(self.colors[self.color])
        self.lighting.fill((0, 0, 0))
        self.camera += (pygame.Vector2(self.player.rect.x, self.player.rect.y) - self.camera - pygame.Vector2(250, 200)) / 5

        blocks = []
        cx, cy = self.player.position // 16 // 16
        for x in range(-2, 2):
            for y in range(-2, 2):
                try:
                    removal = False
                    for block in self.chunks[(cx + x, cy + y)]:
                        if block.position.distance_to(self.player.position) < 300:
                            block.update(self.missiles)
                            blocks.append(block.rect)
                            if block.remove:
                                self.chunks[(x + cx, y + cy)].remove(block)
                                removal = True

                except KeyError:
                    pass

        if random.randrange(0, 4000) < 10:
            self.enemies.append(random.choice(self.enemy_choices[self.color])(self, self.player.position + pygame.Vector2(random.randrange(-400, 400), random.randrange(-400, 400))))

        mp = pygame.Vector2(pygame.mouse.get_pos()) / 2

        for particle in self.particles:
            if particle.lifetime > 0:
                particle.update()
            else:
                self.particles.remove(particle)

            if particle.remove:
                self.particles.remove(particle)

        for circle in self.circles:
            circle[1] += 10
            if circle[1] > 25:
                self.circles.remove(circle)
            pygame.draw.circle(self.surface, (255, 255, 255), (circle[0].x, circle[0].y) - self.camera, circle[1])

        for missile in self.missiles:
            missile.update()

        for bullet in self.enemy_bullets:
            if bullet.lifetime > 2:
                bullet.render()
            else:
                self.enemy_bullets.remove(bullet)

        for enemy in self.enemies:
            for missile in self.missiles:
                rect = pygame.Rect(missile.position.x, missile.position.y, 16, 16)
                enemy_rect = pygame.Rect(enemy.position.x, enemy.position.y, 16, 16)
                if rect.colliderect(enemy_rect):
                    enemy.take_damage(15, missile)
                    self.missiles.remove(missile)
            if enemy.health <= 0:
                self.enemies.remove(enemy)
            enemy.update()

        
        self.crnt_timer += 1


        self.splash_speed = max(self.splash_speed - 0.0001, 0.003)

        self.player.update(blocks)
        self.player.render()
        self.time += 0.01
        # self.surface = self.shader.render_direct()
        dx, dy = 0, 0
        if self.screen_shake > 0:
            self.camera.x += random.uniform(-8, 8)
            self.camera.y += random.uniform(-8, 8)

            self.screen_shake -= 1
        

        pygame.draw.rect(self.surface, (255, 0, 0), (250 - (self.player.max_health / 2), 20, self.player.health, 20))
        pygame.draw.rect(self.surface, (0, 0, 0), (250 - (self.player.max_health / 2), 20, self.player.max_health, 20), 3)

        sin = math.sin(self.time) * 20
        s = self.glow(800)

        # pygame.image.save(s, "light.png")

        self.lighting.blit(s, (-150, -90), special_flags=pygame.BLEND_RGBA_ADD)
        
        self.surface.blit(self.lighting, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)


        if self.player.health <= 0:
            self.app.crnt_state = "game_over"
            
            g = GameOver(self.app, self.renderer)
            AudioHandler.sounds["death"].play()

            g.ocean = True
            g.ocean_surface = self.surface.copy()
            g.update_screen()
            self.app.state = g

        tex = pygame._sdl2.Texture.from_surface(self.renderer, pygame.transform.flip(self.surface, False, False))
        # self.renderer.target = tex
        # self.renderer.blit(, pygame.Rect(dx, dy, 1000, 800))
        # self.renderer.draw_quad((0, 0), (1000, 0), (0, 800), (1000, 800))

        cos =  math.cos(self.time) * 20
        tex.draw_quad((0, 0), (1020 + cos, 0), (1000, 800), (0, 800), p1_uv=(0.0, 0.0), p2_uv=(1.0, 0.0), p3_uv=(1.0, 1.0), p4_uv=(0.0, 1.0))
    
    def handle_event(self, event):

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.missle_count = len(self.missiles)
                if self.crnt_timer >= self.missile_timer:
                    AudioHandler.sounds["missile"].set_volume(100.3)
                    AudioHandler.sounds["missile"].play()
                    mp = pygame.Vector2(pygame.mouse.get_pos()) / 2
                    player = pygame.Vector2(self.player.rect.x - self.camera.x, self.player.rect.y - self.camera.y)
                    direction = (mp - player)
                    self.missiles.append(Missle(self, player + self.camera, direction.normalize(), math.atan2(direction.y, direction.x)))
                    self.screen_shake = 20
                    self.time += 0.5
                    self.splash_speed += 0.009
                    
                    self.crnt_timer = 0
        