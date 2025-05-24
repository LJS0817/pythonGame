from Scenes.Scene import Scene
from Unit.Player.Hero import Hero
from Mng.MapMng import MapMng
from Mng.UIMng import UIMng
from Provider.ItemProvider import ItemProvider

class GameMng(Scene):
    def __init__(self, imageProvider=None):
        super().__init__(self, "GameScene")
        if(imageProvider != None) :
            self.ui = UIMng(imageProvider)
            self.itemProvider = ItemProvider(imageProvider, self.ui)
            self.map = MapMng(32, 32, imageProvider)
            self.hero = Hero(self.map.center, imageProvider, self.itemProvider, self.ui)
        
    def Update(self, input, camera, dt):
        self.map.Update(input, camera, dt)
        self.hero.Update(input, self.map, dt)

    def Draw(self, camera, screen):
        # fill the screen with a color to wipe away anything from last frame
        screen.fill((47, 65, 88))
        self.map.Draw(camera, screen)
        self.hero.Draw(camera, screen)

    def start(self) :
        self.__init__()

    def dispose(self) :
        pass