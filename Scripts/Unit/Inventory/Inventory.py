from pygame.math import Vector2
import pygame.transform

class Inventory :
    def __init__(self, imgPro) :
        self.ITEM_COUNT = 10
        self.ROW_COUNT = 5
        self.showItem = False
        self.items = {
            
        }
        self.img = imgPro.getImage("UI", "Inv_Bag")
        self.img = pygame.transform.scale(self.img, (self.img.get_width() * 8, self.img.get_height() * 8))
        self.position = Vector2(-self.img.get_width() / 2, -self.img.get_height() / 2)

    def showInventory(self) :
        self.showItem = not self.showItem 

    def isShowing(self) :
        return self.showItem

    def addItem(self, id, item, cnt) :
        if id in self.items :
            self.items[id].addCount(cnt)
        else :
            self.items[id] = item
            self.addItem(id, item, cnt)

    def removeItem(self, id) :
        if id in self.items :
            del self.items[id]

    def useItem(self, id, cnt) :
        if id in self.items :
            self.items[id].use(cnt)
            if self.items[id].isEmpty() :
                self.removeItem(id)
    
    def drawItem(self, camera, screen) :
        if self.showItem :
            screen.blit(self.img, self.position + camera.getCenter())
            for i in len(list(self.items.keys())) :
                self.items[self.items.keys()[i]].draw(screen, self.position + camera.getCenter() + Vector2(55, 145))