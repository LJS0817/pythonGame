from Scenes.Scene import Scene
from Unit.Player.Hero import Hero
from Mng.MapMng import MapMng

class GameMng(Scene):
    def __init__(self, imageProvider=None):
        super().__init__(self, "GameScene")
        if(imageProvider != None) :
            self.map = MapMng(32, 32, imageProvider)
            self.hero = Hero(self.map.center)
        
    def Update(self, input, camera, dt):
        self.map.Update(input, camera, dt)
        self.hero.Update(input, self.map, dt)

    def Draw(self, camera, screen):
        # fill the screen with a color to wipe away anything from last frame
        screen.fill("purple")
        self.map.Draw(camera, screen)
        self.hero.Draw(camera, screen)

    def start(self) :
        self.__init__()

    def dispose(self) :
        pass