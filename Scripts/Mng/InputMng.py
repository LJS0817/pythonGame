import pygame

class InputMng :
    def __init__(self, cam) :
        self.keys = pygame.key.get_pressed()
        self.mouse = pygame.mouse
        self.camera = cam
        self.mouseDownEvent = [False, False]

    def UpdateEvent(self, event) :
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouseDownEvent[0] = event.button == 1
            self.mouseDownEvent[1] = event.button == 3

    def Update(self) :
        self.keys = pygame.key.get_pressed()

    def lateUpdate(self):
        if self.mouseDownEvent[0] :
            self.mouseDownEvent = [False, False]

    def isMouseDown(self, btn) :
        return self.mouseDownEvent[btn]
    
    def isKeyPressed(self, key) :
        return self.keys[key]
    
    def isMousePressed(self, btn) :
        return self.mouse.get_pressed()[btn]
    
    def getMousePosition(self) :
        return self.mouse.get_pos() + self.camera.getPosition()