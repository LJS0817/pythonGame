import pygame

class Button :
    def __init__(self, img, name, action) :
        self.img = img
        self.rect = None
        self.name = name
        self.action = action

    def draw(self, screen, pos) :
        self.pos = pos
        self.rect = self.img.get_rect(topleft=pos)
        screen.blit(self.img, self.rect)

    def activate(self) :
        self.action()
            
