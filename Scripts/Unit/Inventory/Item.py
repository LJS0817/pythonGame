import pygame

class Item:
    def __init__(self, font, name, icon_surface, usable=False, callback=None):
        self.name = name
        self.icon = icon_surface

        # 사용가능한 아이템인지
        self.usable = usable

        # 사용가능한 아이템이면 호출
        self.callback = callback

        # 개수
        self.count = 0
        self.font = font
        self.rect = None

        self.countFont = self.font.getFont(18)
        self.titleFont = self.font.getFont(20)

    # 아이템 이름 출력을 위한 함수
    def drawTitle(self, surface, pos) :
        titleFont = self.titleFont.render(str(self.name), True, (84, 56, 35))
        title_pos = titleFont.get_rect(topleft=pos)
        surface.blit(titleFont, title_pos)

    # 이름 출력 함수
    def drawFont(self, surface, pos, tPos) :
        self.drawTitle(surface, pos + tPos)

    # 렌더링
    def draw(self, surface, pos):
        # 디버깅용 배경
        # pygame.draw.rect(surface, (0, 0, 255), (pos.x, pos.y, 64, 64))
        
        self.rect = self.icon.get_rect(topleft=pos)
        surface.blit(self.icon, self.rect)

        cntFont = self.countFont.render(str(self.count), True, (84, 56, 35))
        count_pos = cntFont.get_rect(center=(pos.x + 32, pos.y + 80) )
        surface.blit(cntFont, count_pos)

    # 디버깅용 출력
    def getInfo(self) :
        return f'{self.name}, {self.description}'
    
    # 개수 확인용
    def enoughCount(self, cnt) :
        return self.count >= cnt
    
    # 아이템 추가
    def addCount(self, cnt) :
        self.count += cnt

    # 아이템 사용 addCount 재활용
    def use(self, cnt, hero) :
        if self.usable :
            self.callback(hero)
        self.addCount(-cnt)

    # 아이템 제거
    def remove(self) :
        self.count = 0
    
    # 아이템 제거를 위해서 사용
    def isEmpty(self) :
        return self.count < 1