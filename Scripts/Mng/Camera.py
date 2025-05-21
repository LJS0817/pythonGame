from pygame.math import Vector2

class Camera :
    def __init__(self, width, height):
        self.size = Vector2(width, height)
        self.position = Vector2(-width / 2, -height / 2)

    def getPosition(self) :
        return self.position

    def getCenter(self) :
        return self.size / 2
    
    def setPosition(self, pos) :
        self.position = pos - self.getCenter()

    def smoothMove(self, pos) :
        self.position = Vector2.lerp(self.position, pos - self.getCenter(), 0.1)