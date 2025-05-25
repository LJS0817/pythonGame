import Unit
from pygame.math import Vector2

class Tile:
    def __init__(self, tileT, pos, index, scale) :
        self.position = Vector2(pos[0], pos[1])
        self.index = index
        self.tileType = tileT
        self.targetTileType = tileT
        self.center = self.position + Vector2(scale * 0.5, scale * 0.5)
        self.aniTime = 0
        self.aniLimitTime = 0.05
        self.aniIndex = 0

        self.MAX_INDEX = 6
        self.SWITCH_INDEX = 3
        self.callback = None
        
    def Update(self, dt):
        if(self.aniIndex != 0) :
            self.aniTime += dt
            if(self.aniTime >= self.aniLimitTime) :
                self.aniTime = 0
                self.aniIndex += 1
                if(self.aniIndex == self.SWITCH_INDEX and self.tileType != self.targetTileType) :
                    self.tileType = self.targetTileType
                if(self.aniIndex >= self.MAX_INDEX) :
                    self.aniIndex = 0
                    self.callback()
                    self.callback = None

    def Draw(self, tile, camera, screen):
        if self.tileType > -1 :
            screen.blit(tile.getTile(self.tileType, self.aniIndex), self.position - camera.getPosition())

    def setTileType(self, t, callback) :
        if t == self.targetTileType : return
        self.aniIndex = 1
        self.aniTime = 0
        self.callback = callback
        self.targetTileType = t

    def getTileType(self) :
        return self.tileType

