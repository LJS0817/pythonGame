from ..Unit import Unit
from Unit.UI.HeroUI import HeroUI
from Provider.EventProvider import EventProvider
from pygame.math import Vector2
from Unit.Inventory.Inventory import Inventory
from Unit.UI.FadeOutEffect import FadeEffect
import pygame

class Hero(Unit):
    def __init__(self, center, imgPro, itemPro, uiMng) :
        super().__init__()
        self.position = center
        self.worldPosition = None
        self.prevPos = None
        self.path = None
        self.targetIndex = 0
        self.itemProvider = itemPro
        self.eventProvider = EventProvider(uiMng, imgPro, itemPro)

        self.moveTime = 0
        self.moveLimitTime = 0.4

        self.font = uiMng
        self.bag = Inventory(imgPro, self.font, self)
        self.UI = HeroUI(imgPro)
        self.ApLimit = 4
        self.AP = self.ApLimit + 1
        self.ap_effects = []

    def Update(self, input, mapMng, dt):
        if input.isKeyDown(pygame.K_q) :
            self.changeAP(self.ApLimit)
        if input.isKeyDown(pygame.K_a) :
            self.bag.addItem("1", self.itemProvider.getItem("1"), 1)
        if input.isKeyDown(pygame.K_s) :
            self.bag.addItem("2", self.itemProvider.getItem("2"), 1)
        if input.isKeyDown(pygame.K_d) :
            self.bag.addItem("3", self.itemProvider.getItem("3"), 1)
        if input.isKeyDown(pygame.K_f) :
            self.bag.addItem("4", self.itemProvider.getItem("4"), 1)
        if input.isKeyDown(pygame.K_i) :
            self.showInventory()
        self.Move(input, mapMng, dt)
        self.ap_effects = [fx for fx in self.ap_effects if fx.update(dt)]
        
        self.bag.update(input)

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

    def clearPath(self, mapMng) :
        if self.path != None :
            for i in range(self.targetIndex, len(self.path)) :
                p = Vector2(self.path[i][0], self.path[i][1])
                mapMng.setMapIndex(p, mapMng.getMapChangeIndex((p.x, p.y)))
            self.path = None

    def changeAP(self, cnt) :
        self.AP += cnt
        if self.AP > self.ApLimit :
            self.AP = self.ApLimit
        self.UI.setAp(self.AP / self.ApLimit if self.AP > 0 else 0)

        text = self.font.getFont(24).render(f"{cnt} AP", True, (255, 255, 255))
        self.ap_effects.append(FadeEffect(text, self.worldPosition.copy())) 

    def Move(self, input, mapMng, dt) :
        if not self.bag.isShowing() :
            if input.isMouseDown(1):
                if not mapMng.isSameTarget(input.getMousePosition()) :
                    mapMng.setMapIndex(mapMng.getHex(input.getMousePosition().x, input.getMousePosition().y), -1)

            if input.isMouseDown(0):
                if self.eventProvider.isShowing() :
                    self.eventProvider.handle_click(pygame.mouse.get_pos(), self)
                elif self.path == None and mapMng.getHex(input.getMousePosition().x, input.getMousePosition().y) == self.position : 
                    self.eventProvider.generateEvents(input.camera.getPosition(), self.bag)
                elif not mapMng.isSameTarget(input.getMousePosition()) and self.AP > 0 :
                    self.setTileNearestTile(mapMng)
                    self.path = mapMng.findPath(self.position, input.getMousePosition(), self.path)
                    self.targetIndex = 0

            self.FollowPath(dt)

        if(self.prevPos == None or self.prevPos != self.position) :
            if self.prevPos != None : 
                mapMng.setMapIndex(self.prevPos, mapMng.getMapChangeIndex((self.prevPos.x, self.prevPos.y)))
            mapMng.setMapIndexWithSplash(self.position, "Hero")
            self.worldPosition = mapMng.toWorldPosition(self.position)
            self.changeAP(-1)
            if self.AP <= 0 :
                self.AP = 0
                self.setTileNearestTile(mapMng)
            self.prevPos = Vector2.copy(self.position)

        input.camera.smoothMove(self.worldPosition)
        
    def setTileNearestTile(self, mapMng) :
        if self.path != None :
            if self.targetIndex < len(self.path) :
                pos = self.path[self.targetIndex]
                idx = mapMng.getMapChangeIndex(pos)
                pos = Vector2(pos[0], pos[1])
                print(idx, pos)
                if idx == 0 and mapMng.getMapIndex(pos) == 2 :
                    mapMng.setMapIndex(pos, 1)
            self.clearPath(mapMng)

    def showInventory(self) :
        self.bag.showInventory()

    def Draw(self, camera, screen):
        for fx in list(self.ap_effects):
            fx.draw(screen, camera)
        self.eventProvider.draw(screen, camera.size)
        self.bag.drawItem(camera, screen)
        self.UI.Draw(camera, screen)

    def Clipping(self):
        pass