import Unit
from pygame.math import Vector2

# 맵에 저장되는 타일 객체
class Tile:
    def __init__(self, tileT, pos, index, scale) :
        self.position = Vector2(pos[0], pos[1])
        self.index = index
        # 현재 타일 타입
        self.tileType = tileT
        # 타일 변경 시에 사용되는 목적 타입
        self.targetTileType = tileT
        # 월드포인트 위치
        self.center = self.position + Vector2(scale * 0.5, scale * 0.5)

        # 뒤집히는 시간
        self.aniTime = 0
        self.aniLimitTime = 0.05
        self.aniIndex = 0

        # 뒤집히는 애니메이션 최대 인덱스
        self.MAX_INDEX = 6
        
        # 바뀔 때 3번쨰 인덱스부터 타입 변경
        self.SWITCH_INDEX = 3
        # 변경 시 호출
        self.callback = None
        
    # 변경하기 위한 업데이트
    def Update(self, dt):
        if(self.aniIndex != 0) :
            self.aniTime += dt
            if(self.aniTime >= self.aniLimitTime) :
                self.aniTime = 0
                self.aniIndex += 1
                # 변경해야한다면
                if(self.aniIndex == self.SWITCH_INDEX and self.tileType != self.targetTileType) :
                    self.tileType = self.targetTileType
                if(self.aniIndex >= self.MAX_INDEX) :
                    self.aniIndex = 0
                    self.callback()
                    self.callback = None

    def Draw(self, tile, camera, screen):
        if self.tileType > -1 :
            screen.blit(tile.getTile(self.tileType, self.aniIndex), self.position - camera.getPosition())

    # 타일 변경
    def setTileType(self, t, callback) :
        # 목적 타일이 같다면 반환
        if t == self.targetTileType : return
        self.aniIndex = 1
        self.aniTime = 0
        self.callback = callback
        self.targetTileType = t

    # 현재 타일 타입 반환
    def getTileType(self) :
        return self.tileType

