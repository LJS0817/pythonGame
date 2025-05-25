import pygame

class Item:
    def __init__(self, font, name, icon_surface, usable=False, callback=None):
        self.name = name
        self.icon = icon_surface
        self.usable = usable
        self.callback = callback

        self.count = 0
        self.font = font
        self.rect = None

        self.countFont = self.font.getFont(18)
        self.titleFont = self.font.getFont(20)

    def drawTitle(self, surface, pos) :
        titleFont = self.titleFont.render(str(self.name), True, (84, 56, 35))
        title_pos = titleFont.get_rect(topleft=pos)
        surface.blit(titleFont, title_pos)

    def drawFont(self, surface, pos, tPos) :
        self.drawTitle(surface, pos + tPos)

    def draw(self, surface, pos):
        # pygame.draw.rect(surface, (0, 0, 255), (pos.x, pos.y, 64, 64))
        self.rect = self.icon.get_rect(topleft=pos)
        surface.blit(self.icon, self.rect)

        cntFont = self.countFont.render(str(self.count), True, (84, 56, 35))
        count_pos = cntFont.get_rect(center=(pos.x + 32, pos.y + 80) )
        surface.blit(cntFont, count_pos)

    def getInfo(self) :
        return f'{self.name}, {self.description}'
    
    def addCount(self, cnt) :
        self.count += cnt

    def use(self, cnt, hero) :
        if self.usable :
            self.callback(hero)
        self.addCount(-cnt)

    def remove(self) :
        self.count = 0
    
    def isEmpty(self) :
        return self.count < 1