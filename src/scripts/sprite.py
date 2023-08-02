import pygame


#should change the name, it's just a 2d image in 3d space scaled by Z
#haven't tested, hope it works🤞
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