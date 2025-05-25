from pygame.math import Vector2
from Unit.UI.Button import Button
import pygame.transform

class Inventory :
    def __init__(self, imgPro, font, hero) :
        self.ITEM_COUNT = 10
        self.ROW_COUNT = 5
        self.hero = hero
        self.showItem = False
        self.items = { }
        self.font = font
        self.itemTitleFont = font.getFont(20)
        self.selectedItem = None
        self.itemMenuFixedPos = None
        self.selectedMenu = None
        self.selectedItemKey = None

        self.background = pygame.Surface((1280, 600), pygame.SRCALPHA)
        self.background.fill((0, 0, 0, 128))
        self.img = imgPro.getImage("UI", "Inv_Bag")
        self.img = pygame.transform.scale(self.img, (self.img.get_width() * 8, self.img.get_height() * 8))
        self.btnImg = imgPro.getImage("UI", "Inv_Btn")
        self.btnImg = pygame.transform.scale(self.btnImg, (self.btnImg.get_size()[0] * 8, self.btnImg.get_size()[1] * 8))

        # self.itemInfoImg = imgPro.getImage("UI", "Inv_Info")
        # self.itemInfoImg = pygame.transform.scale(self.itemInfoImg, (self.itemInfoImg.get_width() * 8, self.itemInfoImg.get_height() * 8))
        
        self.buttons = [
            Button(self.btnImg, imgPro.getImage("UI", "Close"), "close", self.showInventory),
            Button(self.btnImg, imgPro.getImage("UI", "Sort"), "Sort", self.sortItem),
            # Button(self.btnImg, imgPro.getImage("UI", "Craft"), "craft", lambda: print('craft Menu')),
        ]
        self.position = Vector2(-self.img.get_width() / 2, -self.img.get_height() / 2)
        
        self.sorted_item_keys = []  # 정렬된 키를 저장할 리스트
        self.sort_trigger = False   # 아이템 목록 변경 여부 플래그

    def showInventory(self) :
        self.showItem = not self.showItem 
        if not self.showItem :
            self.selectedItem = None
            self.itemMenuFixedPos = None
            self.selectedMenu = None

    def isShowing(self) :
        return self.showItem

    def addItem(self, id, item, cnt) :
        if self.hasItem(id) :
            self.items[id].addCount(cnt)
        else :
            self.sorted_item_keys.append(id)
            self.items[id] = item
            self.addItem(id, item, cnt)

    def removeItem(self, id) :
        if self.hasItem(id) :
            self.items[id].remove()
            del self.items[id]
            self.sorted_item_keys = list(self.items.keys())

    def useItem(self, id, cnt) :
        if self.hasItem(id) :
            self.items[id].use(cnt, self.hero)
            if self.items[id].isEmpty() :
                self.removeItem(id)

    def hasItem(self, id) :
        return id in self.items

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

    def showItemMenu(self, screen) :
        if self.selectedItem != None :
            box = self.itemTitleFont.render(str(self.selectedItem.name), True, (212, 185, 165))
            box_pos = box.get_rect(topleft=pygame.mouse.get_pos() if self.itemMenuFixedPos == None else self.itemMenuFixedPos)
            box_pos.move_ip(Vector2(20, 10))
            aPos = box_pos.inflate(20 * 2, 10 * 2)
            a = pygame.Surface(aPos.size)
            a.set_alpha(205)
            a.fill((0, 0, 0))
            screen.blit(a, aPos)
            screen.blit(box, box_pos)

            menu_items = ["Use", "Drop"] if self.selectedItem.usable else ["Drop"]
            menu_rects = []
            menu_x = aPos.left
            menu_y = aPos.bottom + 5
            menu_width = aPos.width
            menu_height = 28
            total_menu_rect = aPos.copy()

            for i, label in enumerate(menu_items):
                rect = pygame.Rect(menu_x, menu_y + i * menu_height, menu_width, menu_height)
                item_bg = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
                item_bg.fill((0, 0, 0, 205))
                screen.blit(item_bg, rect.topleft)

                label_surf = self.itemTitleFont.render(label, True, (255, 255, 255))
                label_rect = label_surf.get_rect(center=rect.center)
                screen.blit(label_surf, label_rect)
                menu_rects.append(rect)

                total_menu_rect.union_ip(rect)
            if self.selectedMenu != None :
                self.selectedMenu = None
            for rect, label in zip(menu_rects, menu_items):
                if rect.collidepoint(pygame.mouse.get_pos()):
                        self.selectedMenu = label
   
            if self.itemMenuFixedPos != None and not total_menu_rect.collidepoint(pygame.mouse.get_pos()) :
                self.itemMenuFixedPos = None

    def subMenuAction(self) :
        if self.selectedMenu != None :
            if self.selectedMenu == "Drop" :
                self.removeItem(self.selectedItemKey)
                self.selectedItemKey = None
                self.selectedItem = None
                self.selectedMenu = None
                self.itemMenuFixedPos = None

            elif self.selectedMenu == "Use" :
                self.useItem(self.selectedItemKey, 1)
                self.selectedItemKey = None
                self.selectedItem = None
                self.selectedMenu = None
                self.itemMenuFixedPos = None

    def update(self, input) :
        if self.showItem :
            if input.isMouseDown(0) :
                self.subMenuAction()
                if self.selectedItem != None :
                    self.itemMenuFixedPos = pygame.mouse.get_pos()
                for btn in self.buttons :
                    if btn.rect.collidepoint(input.mouse.get_pos()) :
                        btn.activate()

    
    def drawItem(self, camera, screen) :
        if self.showItem :
            screen.blit(self.background, (0, 0))
            screen.blit(self.img, self.position + camera.getCenter())
            
            # r = self.itemInfoImg.get_rect(topleft = self.position + camera.getCenter() - Vector2(self.itemInfoImg.get_width() - 8, -80))
            # screen.blit(self.itemInfoImg, r)

            if self.selectedItem != None and self.itemMenuFixedPos == None :
                self.selectedItem = None

            for i in range(len(self.getKeys())) :
                self.items[self.getKeys()[i]].draw(screen, self.position + camera.getCenter() + Vector2(48 + 104* i, 136))
                if self.itemMenuFixedPos == None and self.items[self.getKeys()[i]].rect.collidepoint(pygame.mouse.get_pos()) :
                    self.selectedItemKey = self.getKeys()[i]
                    self.selectedItem = self.items[self.selectedItemKey]
                elif i == len(self.getKeys()) - 1 and self.selectedItem == None and self.itemMenuFixedPos != None :
                    self.itemMenuFixedPos = None
            self.showItemMenu(screen)
            for i in range(len(self.buttons)) :
                self.buttons[i].draw(screen, Vector2(self.position.x + camera.getCenter().x + self.img.get_rect().right, self.position.y + camera.getCenter().y + 100 + 80 * i))