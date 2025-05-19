from ..Unit import Unit
from pygame.math import Vector2
import pygame

class Hero(Unit):
    def __init__(self, center) :
        super().__init__()
        self.position = center
        self.prevPos = None
        self.path = None
        self.targetIndex = 0

        self.moveTime = 0
        self.moveLimitTime = 0.4
    
    def Update(self, input, mapMng, dt):
        self.Move(input, mapMng, dt)

    def FollowPath(self, dt) :
        if self.path == None : return
        self.moveTime += dt
        if self.moveTime >= self.moveLimitTime :
            self.moveTime = 0
            self.position = Vector2(self.path[self.targetIndex][0], self.path[self.targetIndex][1])
            self.targetIndex += 1
            if self.targetIndex >= len(self.path) :
                self.targetIndex = 0
                self.path = None

    def Move(self, input, mapMng, dt) :
        if input.isMousePressed(0):
           self.path = mapMng.findPath(self.position, input.getMousePosition(), self.path)
           self.targetIndex = 0
        
        self.FollowPath(dt)

        if(self.prevPos == None or self.prevPos != self.position) :
            print("IN")
            if self.prevPos != None : mapMng.setMapIndex(self.prevPos, mapMng.getMapChangeIndex((self.prevPos.x, self.prevPos.y)))
            mapMng.setMapIndexWithSplash(self.position, "Hero")
            self.prevPos = Vector2.copy(self.position)

        # if input.isMousePressed(0) :
        #     self.moveTarget = input.getMousePosition()
        # if self.position != self.moveTarget :
        #     self.position = Vector2.move_towards(self.position, self.moveTarget, 10)
            
        input.camera.smoothMove(mapMng.toWorldPosition(self.position))
        # pass
        

    def Draw(self, camera, screen):
        # pygame.draw.circle(screen, "red", Vector2(0, 0) - camera.getPosition(), 40)
        pass

    def Clipping(self):
        pass