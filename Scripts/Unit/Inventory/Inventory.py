from pygame.math import Vector2

class Inventory :
    def __init__(self, imgPro) :
        self.ITEM_COUNT = 10
        self.ROW_COUNT = 5
        self.showItem = False
        self.items = {}
        self.img = imgPro.getImage("Game", "Bag")
        self.position = Vector2(0, 0)

    def showItem(self) :
        self.showItem = not self.showItem 

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
    
    def drawItem(self, screen) :
        if self.showItem :
            screen.blit(self.img, self.position)
            for key in self.items.keys() :
                print(self.items[key].getInfo())
