import pygame

class InputMng :
    def __init__(self, cam) :
        self.keys = pygame.key.get_pressed()
        self.mouse = pygame.mouse
        self.camera = cam
        pass

    def Update(self) :
        self.keys = pygame.key.get_pressed()
    
    def isKeyPressed(self, key) :
        return self.keys[key]
    
    def isMousePressed(self, btn) :
        return self.mouse.get_pressed()[btn]
    
    def getMousePosition(self) :
        return self.mouse.get_pos() + self.camera.getPosition()