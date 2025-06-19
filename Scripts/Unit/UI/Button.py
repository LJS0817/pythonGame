import pygame

# 간단한 UI 버튼
class Button :
    def __init__(self, img, icon, name, action) :
        self.img = img.copy()
        if icon != None :
            self.icon = pygame.transform.scale(icon, (icon.get_size()[0] * 1.75, icon.get_size()[1] * 1.75))
            img_rect = self.img.get_rect()
            icon_rect = self.icon.get_rect(center=img_rect.center)
            icon_rect.x -= 4
            self.img.blit(self.icon, icon_rect.topleft)
        self.rect = None
        self.name = name
        self.action = action

    def draw(self, screen, pos) :
        self.rect = self.img.get_rect(topleft=pos)
        screen.blit(self.img, self.rect)

    # 버튼을 누르면 콜백함수 호출
    def activate(self) :
        self.action()
            
