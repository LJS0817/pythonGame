from ..Unit import Unit
from Unit.UI.HeroUI import HeroUI
from pygame.math import Vector2
from Unit.Inventory.Inventory import Inventory
import pygame

class Hero(Unit):
    def __init__(self, center, imgPro, itemPro, uiMng) :
        super().__init__()
        self.position = center
        self.prevPos = None
        self.path = None
        self.targetIndex = 0
        self.itemProvider = itemPro

        self.moveTime = 0
        self.moveLimitTime = 0.4

        self.font = uiMng
        self.bag = Inventory(imgPro, self.font)
        self.UI = HeroUI(imgPro)
        self.SP = 1
    
    def Update(self, input, mapMng, dt):
        if input.isKeyDown(pygame.K_a) :
            self.bag.addItem("1", self.itemProvider.getItem("1"), 1)
        if input.isKeyDown(pygame.K_s) :
            self.bag.addItem("2", self.itemProvider.getItem("2"), 1)
        if input.isKeyDown(pygame.K_d) :
            self.bag.addItem("3", self.itemProvider.getItem("3"), 1)
        if input.isKeyDown(pygame.K_w) :
            self.bag.sortItem()
        if input.isKeyDown(pygame.K_i) :
            self.showInventory()
        self.Move(input, mapMng, dt)
        
        if input.isMouseDown(0) :
            if self.bag.isShowing() :
                for btn in self.bag.buttons :
                    if btn.rect.collidepoint(input.mouse.get_pos()) :
                        btn.activate()

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
        if not self.bag.isShowing() :

            if input.isMouseDown(1):
                if not mapMng.isSameTarget(input.getMousePosition()) :
                    mapMng.setMapIndex(mapMng.getHex(input.getMousePosition().x, input.getMousePosition().y), -1)

            if input.isMouseDown(0):
                if not mapMng.isSameTarget(input.getMousePosition()) : 
                    if self.path != None :
                        for i in range(self.targetIndex, len(self.path)) :
                                p = Vector2(self.path[i][0], self.path[i][1])
                                mapMng.setMapIndex(p, mapMng.getMapChangeIndex((p.x, p.y)))
                    self.path = mapMng.findPath(self.position, input.getMousePosition(), self.path)
                    self.targetIndex = 0
            self.FollowPath(dt)

        if(self.prevPos == None or self.prevPos != self.position) :
            print("IN")
            if self.prevPos != None : 
                mapMng.setMapIndex(self.prevPos, mapMng.getMapChangeIndex((self.prevPos.x, self.prevPos.y)))
            mapMng.setMapIndexWithSplash(self.position, "Hero")
            self.prevPos = Vector2.copy(self.position)

        input.camera.smoothMove(mapMng.toWorldPosition(self.position))
        
    def showInventory(self) :
        self.bag.showInventory()

    def Draw(self, camera, screen):
        self.bag.drawItem(camera, screen)
        self.UI.Draw(camera, screen)
        pass

    def Clipping(self):
        pass