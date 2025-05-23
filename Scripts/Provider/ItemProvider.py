import pygame.transform
import random
from Unit.Inventory.Item import Item

class ItemProvider :
    def __init__(self, imgPro, font) :
        self.itemList = {
            "1" : Item(font, "Log", pygame.transform.scale(imgPro.getImage("Game", "Log"), (64, 64)), "Can Make Something"),
            "2" : Item(font, "Stone", pygame.transform.scale(imgPro.getImage("Game", "Stone"), (64, 64)), "Can Break Something"),
            "3" : Item(font, "Rope", pygame.transform.scale(imgPro.getImage("Game", "Rope"), (64, 64)), "Can Tie Something"),
        }
        self.itemCount = len(self.itemList)
        
    def getItemCount(self) :
        return self.itemCount

    def getItem(self, id) :
        return self.itemList[id]
    
    def getRandomlyItem(self) :
        return self.itemList[self.itemList.keys()[[self.getItemCount() * random.random()]]]