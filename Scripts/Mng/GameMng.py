from Scenes.Scene import Scene
from Unit.Player.Hero import Hero
from Mng.MapMng import MapMng
from Mng.UIMng import UIMng
from Provider.ItemProvider import ItemProvider

class GameMng(Scene):
    def __init__(self, imageProvider=None):
        super().__init__(self, "GameScene")
        # 객체 초기화
        if(imageProvider != None) :
            self.ui = UIMng(imageProvider)
            self.itemProvider = ItemProvider(imageProvider, self.ui)
            self.map = MapMng(32, 32, imageProvider)
            self.hero = Hero(self.map.center, imageProvider, self.itemProvider, self.ui)
        
    # 업데이트
    def Update(self, input, camera, dt):
        self.map.Update(input, camera, dt)
        self.hero.Update(input, self.map, dt)

    # 렌더링
    def Draw(self, camera, screen):
        screen.fill((47, 65, 88))
        self.map.Draw(camera, screen)
        self.hero.Draw(camera, screen)

    # 씬 변경 후, 진입 시 호출
    def start(self) :
        self.__init__()

    # 씬 변경 시에 호출
    def dispose(self) :
        pass