import pygame
from Util.Event import Event
import random

class EventProvider:
    def __init__(self, font, imgPro, itemPro):
        self.imgPro = imgPro
        self.itemPro = itemPro
        self.events = []  # 현재 생성된 이벤트
        self.eventLimit = 3
        self.last_generated_pos = None

        self.card_size = (300, 150)
        self.card_spacing = 30

        self.font = font.getFont(24)
        self.card_template = pygame.Surface(self.card_size)
        self.card_template.set_alpha(185)
        self.card_template.fill((50, 50, 50))

        self.effects = [
            {
                "desc": "You found a Log (+1)",
                "type": "Item",
                "value": {
                    "id": "1",
                    "item": itemPro.getItem("1")
                }
            },
            {
                "desc": "You found a Rope (+1)",
                "type": "Item",
                "value": {
                    "id": "3",
                    "item": itemPro.getItem("3")
                }
            },
            {
                "desc": "You found a Stone (+1)",
                "type": "Item",
                "value": {
                    "id": "2",
                    "item": itemPro.getItem("2")
                }
            },
            {
                "desc": "You gained +1 AP!",
                "type": "AP",
                "value": 1
            },
            {
                "desc": "Nothing happens.",
                "type": None,
                "value": 0
            }
        ]
        self.enable = False
    
    def isShowing(self) :
        return self.enable

    def generateEvents(self, currentPos, inven, isNearRiver):
        self.enable = True
        self.last_generated_pos = currentPos
        self.events.clear()

        custom_effects = self.effects.copy()
        if inven.hasItem("1") and inven.hasItem("2") and inven.hasItem("3"):
            custom_effects.append({
                "desc": "Create Ax",
                "type": "Craft",
                "value": {
                    "id": "5",
                    "item": self.itemPro.getItem("5"),
                    "use" : ["1", "2", "3"]
                }
            })
            
        if inven.hasEnoughItem("1", 2) and inven.hasItem("3"):
            custom_effects.append({
                "desc": "Create Fishing Rod",
                "type": "Craft",
                "value": {
                    "id": "6",
                    "item": self.itemPro.getItem("6"),
                    "use" : ["1", "1", "3"]
                }
            })

        if inven.hasItem("6") and isNearRiver:
            custom_effects.append({
                "desc": "Go Fishing",
                "type": "Item",
                "value": {
                    "id": "7",
                    "item": self.itemPro.getItem("7")
                }
            })

        if inven.hasItem("7") :
            custom_effects.append({
                "desc": "Cook Fish",
                "type": "Craft",
                "value": {
                    "id": "8",
                    "item": self.itemPro.getItem("8"),
                    "use" : ["7"]
                }
            })
        for _ in range(self.eventLimit):
            effect = random.choice(custom_effects)
            event = Event(effect["desc"], self.font, effect["type"], effect["value"])
            self.events.append(event)

    def handle_click(self, mouse_pos, hero):
        for event in self.events[:]:
            if event.rect and event.rect.collidepoint(mouse_pos) and not event.applied:
                event.apply(hero)
                event.applied = True
                self.events.clear()
                self.enable = False

    def draw(self, screen, screen_size):
        if not self.events:
            return  # 이벤트가 없으면 아무것도 그리지 않음

        # 배경 어둡게 처리
        overlay = pygame.Surface(screen_size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        total_width = len(self.events) * self.card_size[0] + (len(self.events) - 1) * self.card_spacing
        start_x = (screen_size[0] - total_width) // 2
        y = (screen_size[1] - self.card_size[1]) // 2

        for i, event in enumerate(self.events):
            card = self.card_template.copy()
            # 텍스트 중앙 정렬 계산
            text_w, text_h = event.text_surface.get_size()
            text_area_x = 10
            text_area_w = self.card_size[0] - text_area_x - 10

            text_x = text_area_x + (text_area_w - text_w) // 2
            text_y = (self.card_size[1] - text_h) // 2

            card.blit(event.text_surface, (text_x, text_y))

            x = start_x + i * (self.card_size[0] + self.card_spacing)
            screen.blit(card, (x, y))

            event.rect = pygame.Rect(x, y, *self.card_size)
