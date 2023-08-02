from .state import State

from pygame_3d import *

# make separate class for 3D and 2D part of the game
class Space(State):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.background_image = pygame.image.load("src/assets/Space Background.png")
        self.background_image = pygame._sdl2.Texture.from_surface(self.renderer, self.background_image)

    def update(self):
        ...

    def render(self, renderer):
        renderer.draw_color = (0, 0, 0, 255)
        renderer.clear()
        
        renderer.blit(self.background_image, pygame.Rect(0, 0, 1000, 800))
        
    def handle_event(self, event):
        # optional
        pass