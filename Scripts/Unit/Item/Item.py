import pygame

class Item:
    def __init__(self, name, icon_surface, description=""):
        self.name = name                # 아이템 이름
        self.icon = icon_surface        # pygame.Surface 타입 아이콘
        self.description = description  # 아이템 설명 (툴팁용 등)

    def draw(self, surface, pos):
        rect = self.icon.get_rect(topleft=pos)
        surface.blit(self.icon, rect)
