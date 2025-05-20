import pygame

class MapTile :
    def __init__(self, imgPro) :
        self.imgs = [imgPro.getImage("Map", "Block"), 
                     imgPro.getAnimatedImage("Map", "Ground"), 
                     imgPro.getImage("Map", "Path"),
                     imgPro.getImage("Map", "Hero"),]
        self.scale = 32
        self.padding = 4
        self.halfScale = self.scale / 2
        self.tileType = {
            "Block" : 0,
            "Normal" : 1,
            "Path" : 2,
            "Hero" : 3,
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
    
    def getTile(self, idx) :
        return self.imgs[int(idx)]
