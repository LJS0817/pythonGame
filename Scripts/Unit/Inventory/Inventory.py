from pygame.math import Vector2
from Unit.UI.Button import Button
import pygame.transform

class Inventory :
    def __init__(self, imgPro) :
        self.ITEM_COUNT = 10
        self.ROW_COUNT = 5
        self.showItem = False
        self.items = { }

        self.background = pygame.Surface((1280, 600), pygame.SRCALPHA)
        self.background.fill((0, 0, 0, 128))
        self.img = imgPro.getImage("UI", "Inv_Bag")
        self.img = pygame.transform.scale(self.img, (self.img.get_width() * 8, self.img.get_height() * 8))
        self.btnImg = imgPro.getImage("UI", "Inv_Btn")
        self.btnImg = pygame.transform.scale(self.btnImg, (self.btnImg.get_size()[0] * 8, self.btnImg.get_size()[1] * 8))
        self.itemInfoImg = imgPro.getImage("UI", "Inv_Info")
        self.itemInfoImg = pygame.transform.scale(self.itemInfoImg, (self.itemInfoImg.get_width() * 8, self.itemInfoImg.get_height() * 8))
        self.buttons = [
            Button(self.btnImg, None, "close", self.showInventory),
            Button(self.btnImg, None, "sort", self.sortItem),
            Button(self.btnImg, None, "craft", lambda: print('craft Menu')),
        ]
        self.position = Vector2(-self.img.get_width() / 2, -self.img.get_height() / 2)
        
        self.sorted_item_keys = []  # 정렬된 키를 저장할 리스트
        self.sort_trigger = False   # 아이템 목록 변경 여부 플래그

    def showInventory(self) :
        self.showItem = not self.showItem 

    def isShowing(self) :
        return self.showItem

    def addItem(self, id, item, cnt) :
        if id in self.items :
            self.items[id].addCount(cnt)
        else :
            self.sorted_item_keys.append(id)
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

    def quicksort(self, arr):
        if len(arr) <= 1:
            return arr

        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        mid = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]

        return self.quicksort(left) + mid + self.quicksort(right)

    def sortItem(self) :
        self.sort_trigger = True

    def getKeys(self):
        if self.sort_trigger :
            self.sorted_item_keys = self.quicksort(list(self.items.keys()))
            self.sort_trigger = False
        return self.sorted_item_keys
    
    def drawItem(self, camera, screen) :
        if self.showItem :
            screen.blit(self.background, (0, 0))
            screen.blit(self.img, self.position + camera.getCenter())
            for i in range(len(self.getKeys())) :
                if self.items[self.getKeys()[i]].icon.get_rect().collidepoint(pygame.mouse.get_pos()) :
                    print("ASDAS")
                    count_surface = self.font.render(str(self.items[self.getKeys()[i]].name), True, (84, 56, 35))
                    count_pos = count_surface.get_rect(center=(30, 20) )
                    self.itemInfoImg.blit(count_surface, count_pos)
                self.items[self.getKeys()[i]].draw(screen, self.position + camera.getCenter() + Vector2(48 + 104* i, 136))
            for i in range(len(self.buttons)) :
                self.buttons[i].draw(screen, Vector2(self.position.x + camera.getCenter().x + self.img.get_rect().right, self.position.y + camera.getCenter().y + 100 + 80 * i))
            screen.blit(self.itemInfoImg, self.position + camera.getCenter() - Vector2(self.itemInfoImg.get_width() - 8, -80))