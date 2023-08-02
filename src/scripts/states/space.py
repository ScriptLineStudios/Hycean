from .state import State
from src.scripts.entities.player import Player
from src.scripts.entities.planet import Planet
from src.scripts.entities.entity import Entity

import glm

from pygame_3d import *

# make separate class for 3D and 2D part of the game
class Space(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.background_image = pygame.image.load("src/assets/Space Background.png")
        self.background_image = pygame._sdl2.Texture.from_surface(self.renderer, self.background_image)

        self.camera = Camera()
        self.model_renderer = ModelRenderer(self.camera)
        self.camera.orientation = glm.vec3(     0.860336,     0.509041,   -0.0264359 )
        self.camera.position = glm.vec3(      3.77888,      4.04609,      2.04851 )

        self.player = Player(self, "src/assets/models/spaceship/spaceship_high2.obj", "src/assets/models/spaceship/spaceship_high2.mtl")
        self.planet = Planet(self, "src/assets/models/planet/planet.obj", "src/assets/models/planet/planet.mtl")

        self.model_renderer.add_model(self.player)
        self.model_renderer.add_model(self.planet)


    def update(self):
        self.camera.position += self.player.direction

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.player.degree -= 1
        if keys[pygame.K_a]:
            self.player.degree += 1

    def render(self):
        self.renderer.draw_color = (0, 0, 0, 255)
        self.renderer.clear()
        
        self.renderer.blit(self.background_image, pygame.Rect(0, 0, 1000, 800))
        
        matrix = self.model_renderer.update_camera()
        self.model_renderer.sort_models()

        for model in self.model_renderer.models:
            self.model_renderer.render_model(model, self.renderer, matrix)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                pygame.mouse.set_pos((500, 400))
                pygame.mouse.set_visible(self.camera.hidden)
                self.camera.hidden = not self.camera.hidden
