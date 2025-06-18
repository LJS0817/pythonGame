import pygame

class InputMng :
    def __init__(self, cam) :
        self.keys = pygame.key.get_pressed()
        self.mouse = pygame.mouse
        self.camera = cam
        self.mouseDownEvent = [False, False]
        self.keyEvents = {}

    # Down, Up을 위한 이벤트 감지 업데이트
    def UpdateEvent(self, event) :
        if event.type == pygame.KEYDOWN :
            self.keyEvents[event.key] = True
        if event.type == pygame.KEYUP :
            self.keyEvents[event.key] = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouseDownEvent[0] = event.button == 1
            self.mouseDownEvent[1] = event.button == 3

    # Pressed를 위한 업데이트     
    def Update(self) :
        self.keys = pygame.key.get_pressed()

    # 이벤트 초기화를 위해서 업데이트와 렌더링이 끝난 이후에 호출
    def lateUpdate(self):
        self.keyEvents.clear()
        if self.mouseDownEvent[0] or self.mouseDownEvent[1] :
            self.mouseDownEvent = [False, False]

    # 현재 프레임에서 해당 버튼이 눌린 이벤트가 발생했는지 확인
    def isMouseDown(self, btn) :
        return self.mouseDownEvent[btn]

    # KEYDOWN 이벤트는 입력된 순간 True, 그 다음 프레임부터는 False
    def isKeyDown(self, key) :
        return key in self.keyEvents and self.keyEvents[key]
    
    # KEYUP 이벤트는 손을 뗀 순간 True, 그 다음 프레임부터는 False
    def isKeyUp(self, key) :
        return key in self.keyEvents and not self.keyEvents[key]
    
    # 키가 누르고 있는 상태인지 확인
    def isKeyPressed(self, key) :
        return self.keys[key]
    
     # 마우스 버튼이 누르고 있는 상태인지 확인
    def isMousePressed(self, btn) :
        return self.mouse.get_pressed()[btn]
    
    # 카메라 위치를 고려한 월드 마우스 좌표를 반환
    def getMousePosition(self) :
        return self.mouse.get_pos() + self.camera.getPosition()