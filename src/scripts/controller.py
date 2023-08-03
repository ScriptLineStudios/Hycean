import pygame
from pygame import Vector2
from pygame.locals import *


class Controller:
    def __init__(self, renderer, ScreenSize):
        self.renderer = renderer
        self.ScreenSize = ScreenSize
        self.position = Vector2(0, 0)

        self.center = Vector2(
            self.ScreenSize[0] // 2,
            self.ScreenSize[1] // 2
        )

        self.angle = (1, 0.8)
        self.angle_p_pix = Vector2(
            self.angle[0] / self.ScreenSize[0],
            self.angle[1] / self.ScreenSize[1]
        )

    
        self.disable = False

    def update(self):
        direction = self.position - self.center
        self.angleMove = direction.elementwise() * self.angle_p_pix

        #print(self.angleMove)
        if False:#direction != (0, 0)  
            move = direction.normalize()
    
            move = move.elementwise() * self.angle

            self.position = self.position - move
            pygame.mouse.set_pos(self.position - move)

    def draw_debug(self):
        self.renderer.draw_color = (0, 255, 0, 255)

        hLine = (
            (0, self.center[1]),
            (self.ScreenSize[0], self.center[1])
        )
        vLine = (
            (self.center[0], 0),
            (self.center[0], self.ScreenSize[1])
        )
        
        

        self.renderer.draw_line(self.center, self.position)
        self.renderer.draw_line(hLine[0], hLine[1])
        self.renderer.draw_line(vLine[0], vLine[1])

    def handle_event(self, event):
        if event.type == MOUSEMOTION:
            self.position = Vector2(event.pos)