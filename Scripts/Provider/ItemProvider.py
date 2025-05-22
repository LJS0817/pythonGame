import pygame.transform
import random
from Unit.Inventory.Item import Item

class ItemProvider :
    def __init__(self, imgPro) :
        self.itemList = {
            "1" : Item("Test", pygame.transform.scale(imgPro.getImage("Game", "Stick"), (48, 48)), "123456"),
            "2" : Item("Test", pygame.transform.scale(imgPro.getImage("Game", "Stick"), (48, 48)), "123456"),
            "3" : Item("Test", pygame.transform.scale(imgPro.getImage("Game", "Stick"), (48, 48)), "123456"),
        }
        self.itemCount = len(self.itemList)
        
    def getItem(self, id) :
        return self.itemList[id]
    
    def getRandomlyItem(self) :
        return self.itemList[self.itemList.keys()[[self.itemCount * random.random()]]]