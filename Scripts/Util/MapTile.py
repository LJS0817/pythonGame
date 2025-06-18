import pygame

class MapTile :
    def __init__(self, imgPro) :
        self.imgs = [imgPro.getAnimatedImage("Map", "Block", 6), 
                     imgPro.getAnimatedImage("Map", "Ground", 6), 
                     imgPro.getAnimatedImage("Map", "River", 6), 
                     imgPro.getAnimatedImage("Map", "Path", 6),
                     imgPro.getAnimatedImage("Map", "Hero", 6),]
        self.scale = 32
        self.padding = 4
        self.halfScale = self.scale / 2
        self.tileType = {
            "Block" : 0,
            "Normal" : 1,
            "River" : 2,
            "Path" : 3,
            "Hero" : 4,
        }

    def resize(self, scale) :
        for i in range(len(self.imgs)) :
            for j in range(len(self.imgs[i])) :
                self.imgs[i][j] = pygame.transform.scale(self.imgs[i][j], (scale, scale))

        self.padding = scale / self.scale * self.padding
        self.scale = scale
        self.halfScale = self.scale / 2

    def getSizeWithoutPadding(self) :
        return self.scale - self.padding
    
    def getShift(self) :
        return self.halfScale - (self.padding * 0.5)
    
    def getTile(self, idx, aniIndex = 0) :
        return self.imgs[int(idx)][aniIndex]
