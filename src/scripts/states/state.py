class State:
    def __init__(self, app, renderer):
        self.renderer = renderer
        self.app = app

    def start(self):
        pass

    def stop(self):
        pass

    def update(self):
        pass

    def render(self):
        pass

    def handle_event(self, event):
        # optional
        pass