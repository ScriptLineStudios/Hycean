import pygame
import pygame._sdl2

from src.scripts.entities.planet import Planet
from src.scripts.audio_handler import AudioHandler

import math
import threading

class AI:
    def __init__(self):
        pass
        
    @staticmethod
    def say(text):
        self.engine.say(text)
        self.engine.runAndWait()

    def speak(self, text):
        pass
        #I dont this this is gonna work :(

class Button:
    def __init__(self, app, text, position=None):
        self.app = app
        self.small_font = pygame.font.Font("src/assets/prstartk.ttf", 16)
        self.text = text
        self.surface = self.small_font.render(self.text, False, (255, 255, 255))
        self.position = position

    def render(self, surface):
        mp = pygame.mouse.get_pos()

        self.global_rect = pygame.Rect(*(self.position + pygame.Vector2(700, 0)), self.surface.get_width(), self.surface.get_height())
        if pygame.Rect(*(self.position + pygame.Vector2(700, 0)), self.surface.get_width(), self.surface.get_height()).collidepoint(mp):
            surface.blit(pygame.transform.scale(self.surface, (self.surface.get_width() * 1.5, self.surface.get_height() * 1.2)), self.position)
        else:
            surface.blit(self.surface, self.position)

    def on_click(self):
        if self.app.crnt_state == "space":
            print(f"Locating: {self.material}")
            
            for model in self.app.state.model_renderer.models:
                if type(model) == Planet:
                    if model.primary_material:
                        if model.primary_material[0] == self.material:
                            self.app.state.gps = pygame.Vector2(model.position.x + 500, model.position.z + 500)
                            self.app.ui.ai.speak(f"I have updated your map. The nearest source of {self.material} is {int(pygame.Vector2(model.position.x + 500, model.position.z + 500).distance_to(pygame.Vector2(self.app.state.player.position.x + 500, self.app.state.player.position.z + 500)))}kilometers away")
                            self.app.ui.gps.play()
                            self.app.ui.computer_active = False
                            break

class UI:
    def __init__(self, app, renderer):
        self.app = app
        self.renderer = renderer
        self.computer_ui = pygame.image.load("src/assets/computer.png")
        self.door_ui = pygame.image.load("src/assets/door.png")

        self.computer_texture = pygame._sdl2.Texture.from_surface(self.renderer, self.computer_ui)
        self.door_texture = pygame._sdl2.Texture.from_surface(self.renderer, self.door_ui)
        
        self.click = AudioHandler.sounds['click']
        self.gps = AudioHandler.sounds['gps']
        
        self.computer_rect = pygame.Rect(0, 0, 1, 1)

        self.time = 0
        self.clicked = False
        self.computer_active = False

        self.surface = pygame.Surface((800, 800))

        self.font = pygame.font.Font("src/assets/prstartk.ttf", 32)
        self.small_font = pygame.font.Font("src/assets/prstartk.ttf", 16)

        self.buttons = []
        self.ai = AI()
        self.panel_x = 1000

    def render(self):
        self.surface.fill((40, 40, 40, 255))
        self.time += 0.1
        off = math.sin(self.time) * 5

        self.computer_rect = pygame.Rect(864 - off/2, 70 - off/2, 64 + off, 64 + off)

        self.buttons = []

        if self.app.crnt_state == "space":
            self.renderer.blit(self.computer_texture, self.computer_rect)
            if self.computer_active:
                text = self.font.render("System", False, (255, 255, 255))
                resources = self.small_font.render("Needed Resources\n", False, (255, 255, 255))

                self.surface.blit(text, (5, 6))
                self.surface.blit(resources, (5, 6 + text.get_height() * 1.5))
                
                for i, key in enumerate(self.app.needed_resources_stable.keys()):
                    needed_resources = f"{key}: {self.app.collected_materials[key]}/{self.app.needed_resources_stable[key]}\n"
                    if self.app.collected_materials[key] >= self.app.needed_resources_stable[key]:
                        t = self.small_font.render(needed_resources, False, "green")
                    else:
                        t = self.small_font.render(needed_resources, False, "white")
                    self.surface.blit(t, (5, 100 + i * t.get_height() * 3.5))
                    b = Button(self.app, "locate", pygame.Vector2(10, 100 + i * t.get_height() * 3.5 + 25))
                    b.material = key
                    self.buttons.append(b)

                for button in self.buttons:
                    button.render(self.surface)

                if self.panel_x > 700:
                    self.panel_x -= 20
                self.renderer.blit(pygame._sdl2.Texture.from_surface(self.renderer, self.surface), pygame.Rect(self.panel_x, 0, 800, 800))
            else:
                if self.panel_x < 1000:
                    self.panel_x += 20
                self.renderer.blit(pygame._sdl2.Texture.from_surface(self.renderer, self.surface), pygame.Rect(self.panel_x, 0, 800, 800))
        else:
            try:
                if self.app.collected_materials[self.app.state.material] >= self.app.needed_resources_stable[self.app.state.material]:
                    text = self.font.render(f"Goal: Find {self.app.current_resource} ({self.app.collected_materials[self.app.state.material]}/{self.app.needed_resources_stable[self.app.state.material]})", False, (0, 255, 0))
                
                else:
                    text = self.font.render(f"Goal: Find {self.app.current_resource} ({self.app.collected_materials[self.app.state.material]}/{self.app.needed_resources_stable[self.app.state.material]})", False, (255, 255, 255))
                rect = pygame.Rect(500, 400, text.get_width(), text.get_height())
                rect.center = rect.topleft
                rect.y = 760 - rect.height
                self.renderer.blit(pygame._sdl2.Texture.from_surface(self.renderer, text), rect)
            except Exception as e:
                pass
            self.renderer.blit(self.door_texture, self.computer_rect)

    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.app.crnt_state == "space":
                    mp = pygame.Vector2(pygame.mouse.get_pos())
                    if self.computer_rect.collidepoint(mp):
                        self.click.play()
                        self.clicked = True
                        self.computer_active = True

                    for button in self.buttons:
                        if button.global_rect.collidepoint(mp):
                            button.on_click()
                else:
                    mp = pygame.Vector2(pygame.mouse.get_pos())
                    if self.computer_rect.collidepoint(mp):
                        self.click.play()
                        self.clicked = True
                        pygame.mixer.fadeout(10)
                        pygame.mixer.music.load("src/sfx/ambientspacemusic.mp3")
                        pygame.mixer.music.play(-1)
                        self.app.crnt_state = "space"
                        self.app.state = self.app.states[self.app.crnt_state]