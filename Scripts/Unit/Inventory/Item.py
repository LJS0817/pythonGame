import pygame

class Item:
    def __init__(self, font, name, icon_surface, description=""):
        self.name = name
        self.icon = icon_surface
        self.description = description 
        
        self.count = 0
        self.font = font
        self.rect = None

        self.countFont = self.font.getFont(18)
        self.titleFont = self.font.getFont(20)
        self.descFont = self.font.getFont(18)

    def drawTitle(self, surface, pos) :
        titleFont = self.titleFont.render(str(self.name), True, (84, 56, 35))
        title_pos = titleFont.get_rect(topleft=pos)
        surface.blit(titleFont, title_pos)

    def drawDesc(self, surface, pos) :
        descFont = self.descFont.render(str(self.description), True, (84, 56, 35))
        desc_pos = descFont.get_rect(topleft=pos)
        surface.blit(descFont, desc_pos)

    def drawFont(self, surface, pos, tPos, dPos) :
        self.drawTitle(surface, pos + tPos)
        self.drawDesc(surface, pos + dPos)

    def draw(self, surface, pos):
        pygame.draw.rect(surface, (0, 0, 255), (pos.x, pos.y, 64, 64))
        self.rect = self.icon.get_rect(topleft=pos)
        surface.blit(self.icon, self.rect)

        cntFont = self.countFont.render(str(self.count), True, (84, 56, 35))
        count_pos = cntFont.get_rect(center=(pos.x + 32, pos.y + 80) )
        surface.blit(cntFont, count_pos)

    def getInfo(self) :
        return f'{self.name}, {self.description}'
    
    def addCount(self, cnt) :
        self.count += cnt
    
    def isEmpty(self) :
        return self.count < 1