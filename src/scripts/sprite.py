import pygame


class Sprite:
    def __init__(self, texture, position, size=None):
        self.position = position

        self.texture = texture
        if size != None:
            self.rect = pygame.Rect(0, 0, size[0], size[1])
        else:
            self.rect = self.texture.get_rect()

    def draw(self, position, normalizedZ):
        scaleRect = self.rect.copy()
        scaleRect.center = position
        scaleRect.width *= normalizedZ
        scaleRect.height *= normalizedZ

        self.texture.draw(srcrect=None, dstrect=scaleRect)
    
    def draw_debug(self, renderer):
        pass


