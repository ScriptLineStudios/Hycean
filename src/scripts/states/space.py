from .state import State
from src.scripts.entities.player import Player

from pygame_3d import *

# make separate class for 3D and 2D part of the game
class Space(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.background_image = pygame.image.load("src/assets/Space Background.png")
        self.background_image = pygame._sdl2.Texture.from_surface(self.renderer, self.background_image)

        self.player = Player("src/assets/models/spaceship/spaceship_high2.obj", "src/assets/models/spaceship/spaceship_high2.mtl")
        self.camera = Camera()
        self.model_renderer = ModelRenderer(self.camera)

        self.model_renderer.add_model(self.player)

    def update(self):
        ...

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