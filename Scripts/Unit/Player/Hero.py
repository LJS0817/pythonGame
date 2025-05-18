from ..Unit import Unit
from pygame.math import Vector2
import pygame

class Hero(Unit):
    def __init__(self, center) :
        super().__init__()
        self.position = center
        self.prevPos = None
        # self.velocity = Vector2(0, 0)
        # self.speed = 100
        # self.moveTarget = Vector2(0, 0)
    
    def Update(self, input, mapMng, dt):
        self.Move(input, mapMng, dt)

    def Move(self, input, mapMng, dt) :
        if input.isKeyPressed(pygame.K_d) :
            self.position.x += 1
            print(self.position)
            print(self.prevPos)

        if(self.prevPos == None or self.prevPos != self.position) :
            print("IN")
            mapMng.setMapIndex(self.position, "Normal")
            self.prevPos = Vector2.copy(self.position)
        # if input.isMousePressed(0) :
        #     self.moveTarget = input.getMousePosition()
        # if self.position != self.moveTarget :
        #     self.position = Vector2.move_towards(self.position, self.moveTarget, 10)
            
        # input.camera.smoothMove(self.position)
        pass
        

    def Draw(self, camera, screen):
        pygame.draw.circle(screen, "red", self.position - camera.getPosition(), 40)
        pass

    def Clipping(self):
        pass