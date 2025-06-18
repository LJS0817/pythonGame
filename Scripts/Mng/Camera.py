from pygame.math import Vector2

class Camera :
    def __init__(self, width, height):
        self.size = Vector2(width, height)
        self.position = Vector2(-width / 2, -height / 2)

    # 카메라 위치 반환
    def getPosition(self) :
        return self.position

    # 화면 중앙
    def getCenter(self) :
        return self.size / 2
    
    # 기본적인 카메라 위치 이동
    def setPosition(self, pos) :
        self.position = pos - self.getCenter()

    # 카메라 이동 시 Lerp를 사용하여 부드러운 이동 구현
    def smoothMove(self, pos) :
        self.position = Vector2.lerp(self.position, pos - self.getCenter(), 0.1)