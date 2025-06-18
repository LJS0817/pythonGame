import pygame.transform
import random
from Unit.Inventory.Item import Item

class ItemProvider :
    def __init__(self, imgPro, font) :

        def mushroom_effect(hero):
            print("Mushroom used! +1 AP")
            hero.changeAP(1)

        def fish_effect(hero):
            print("Raw Fish used! -2 AP")
            hero.changeAP(-2)

        def cooked_fish_effect(hero):
            print("Cooked Fish used! +2 AP")
            hero.changeAP(2)

        self.itemList = {
            "1" : Item(font, "Log", pygame.transform.scale(imgPro.getImage("Game", "Log"), (64, 64))),
            "2" : Item(font, "Stone", pygame.transform.scale(imgPro.getImage("Game", "Stone"), (64, 64))),
            "3" : Item(font, "Rope", pygame.transform.scale(imgPro.getImage("Game", "Rope"), (64, 64))),
            "4" : Item(font, "Mushroom", pygame.transform.scale(imgPro.getImage("Game", "Mushroom"), (64, 64)), True, mushroom_effect),
            "5" : Item(font, "Ax", pygame.transform.scale(imgPro.getImage("Game", "Ax"), (64, 64))),
            "6" : Item(font, "Fishing Rod", pygame.transform.scale(imgPro.getImage("Game", "Rod"), (64, 64))),
            "7" : Item(font, "Fish", pygame.transform.scale(imgPro.getImage("Game", "Fish"), (64, 64)), True, fish_effect),
            "8" : Item(font, "Cooked Fish", pygame.transform.scale(imgPro.getImage("Game", "cFish"), (64, 64)), True, cooked_fish_effect),
        }
        self.itemCount = len(self.itemList)
        
    def getItemCount(self) :
        return self.itemCount

    def getItem(self, id) :
        return self.itemList[id]
    
    def getRandomlyItem(self) :
        return self.itemList[self.itemList.keys()[[self.getItemCount() * random.random()]]]