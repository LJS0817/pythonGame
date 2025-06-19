from Scenes.Scene import Scene
from Mng.UIMng import UIMng
from Provider.ItemProvider import ItemProvider

class MenuMng(Scene):
    def __init__(self, imageProvider=None):
        super().__init__(self, "MenuScene")
        # 객체 초기화
        if(imageProvider != None) :
            self.ui = UIMng(imageProvider)
            self.itemProvider = ItemProvider(imageProvider, self.ui)
    # 업데이트
    def Update(self, input, camera, dt):
        pass

    # 렌더링
    def Draw(self, camera, screen):
        screen.fill((47, 65, 88))
        pass

    # 씬 변경 후, 진입 시 호출
    def start(self) :
        self.__init__()

    # 씬 변경 시에 호출
    def dispose(self) :
        pass