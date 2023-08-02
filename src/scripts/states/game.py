from .state import State


# make separate class for 3D and 2D part of the game
class Game(State):
    def __init__(self):
        super().__init__()

    def update(self):
        ...

    def render(self, renderer):
        renderer.draw_color = (255, 0, 0, 255)
        renderer.clear()
        
    def handle_event(self, event):
        # optional
        pass