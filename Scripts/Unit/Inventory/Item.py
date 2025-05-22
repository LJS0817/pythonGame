import pygame

class Item:
    def __init__(self, font, name, icon_surface, description=""):
        self.name = name                # 아이템 이름
        self.icon = icon_surface        # pygame.Surface 타입 아이콘
        self.description = description  # 아이템 설명 (툴팁용 등)
        self.count = 0
        self.font = font

    def draw(self, surface, pos):
        pygame.draw.rect(surface, (0, 0, 255), (pos.x, pos.y, 64, 64))
        surface.blit(self.icon, pos)

        count_surface = self.font.render(str(self.count), True, (84, 56, 35))
        # 중심 아래에 텍스트 배치
        count_pos = count_surface.get_rect(center=(pos.x + 32, pos.y + 80) )
        surface.blit(count_surface, count_pos)

    def getInfo(self) :
        return f'{self.name}, {self.description}'
    
    def addCount(self, cnt) :
        self.count += cnt
    
    def isEmpty(self) :
        return self.count < 1