import pygame

# 화면 객체를 관리하는 객체
class SceneState:
    def __init__(self, sceneList, startIndex=0):
        self.list = sceneList

        for i in range(len(sceneList)):
            self.list[i].setId(i)

        self.curIndex = startIndex
        self.getCurrentScene().start()

    # 테스트를 위해서 화면 전환
    def increaseIndex(self) :
        return self.curIndex + 1
    
    # 스페이스바를 누르면 다음 화면으로 전환
    def sceneChanger(self, input) :
        if input.isKeyDown(pygame.K_SPACE) :
            self.changeScene(self.increaseIndex())
    
    # 실제 화면 전환 로직
    # 이전 화면의 상태를 초기화하고
    # 바뀔 화면의 상태롤 초기화하여 불러온다
    def changeScene(self, idx) :
        self.getCurrentScene().dispose()
        if idx >= len(self.list) :
            idx = 0
        self.curIndex = idx
        print(f"changeScene  {self.getCurrentScene().getName()}")
        self.getCurrentScene().start()

    # 현재 화면 상태 반환
    def getCurrentScene(self) :
        return self.list[self.curIndex]