from pygame import Vector2

# 일부 객체를 상속을 위한 클래스
class Unit:
    def __init__(self):
        self.position = Vector2(0, 0)
        self.scale = Vector2(1, 1)
    
    def Update(self, dt):
        pass

    def Draw(self, camera, screen):
        pass

    def Clipping(self):
        pass