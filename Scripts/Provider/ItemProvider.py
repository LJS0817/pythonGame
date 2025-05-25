import pygame.transform
import random
from Unit.Inventory.Item import Item

class ItemProvider :
    def __init__(self, imgPro, font) :

        def mushroom_effect(hero):
            print("Mushroom used! +1 AP")
            hero.changeAP(1)

        self.itemList = {
            "1" : Item(font, "Log", pygame.transform.scale(imgPro.getImage("Game", "Log"), (64, 64))),
            "2" : Item(font, "Stone", pygame.transform.scale(imgPro.getImage("Game", "Stone"), (64, 64))),
            "3" : Item(font, "Rope", pygame.transform.scale(imgPro.getImage("Game", "Rope"), (64, 64))),
            "4" : Item(font, "Mushroom", pygame.transform.scale(imgPro.getImage("Game", "Mushroom"), (64, 64)), True, mushroom_effect),
            "5" : Item(font, "Ax", pygame.transform.scale(imgPro.getImage("Game", "Ax"), (64, 64))),
        }
        self.itemCount = len(self.itemList)
        
    def getItemCount(self) :
        return self.itemCount

    def getItem(self, id) :
        return self.itemList[id]
    
    def getRandomlyItem(self) :
        return self.itemList[self.itemList.keys()[[self.getItemCount() * random.random()]]]