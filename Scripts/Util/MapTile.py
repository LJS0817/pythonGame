import pygame

class MapTile :
    def __init__(self, imgPro) :
        # 타일 종류 이미지 리스트
        self.imgs = [imgPro.getAnimatedImage("Map", "Block", 6), 
                     imgPro.getAnimatedImage("Map", "Ground", 6), 
                     imgPro.getAnimatedImage("Map", "River", 6), 
                     imgPro.getAnimatedImage("Map", "Path", 6),
                     imgPro.getAnimatedImage("Map", "Hero", 6),]
        # 타일 이미지 정보
        self.scale = 32
        self.padding = 4
        self.halfScale = self.scale / 2

        # 타일 타입
        self.tileType = {
            "Block" : 0,
            "Normal" : 1,
            "River" : 2,
            "Path" : 3,
            "Hero" : 4,
        }

    # 타일 이미지 변환
    def resize(self, scale) :
        for i in range(len(self.imgs)) :
            for j in range(len(self.imgs[i])) :
                self.imgs[i][j] = pygame.transform.scale(self.imgs[i][j], (scale, scale))

        self.padding = scale / self.scale * self.padding
        self.scale = scale
        self.halfScale = self.scale / 2

    # 이미지에 포함된 여백 제외
    def getSizeWithoutPadding(self) :
        return self.scale - self.padding
    
    # 빈 공간 없이 출력하기 위해서 이동한 정도
    def getShift(self) :
        return self.halfScale - (self.padding * 0.5)
    
    # 이미지 애니메이션을 위한 이미지 반환
    def getTile(self, idx, aniIndex = 0) :
        return self.imgs[int(idx)][aniIndex]
