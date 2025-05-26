from pygame.math import Vector2
from Util.MapTile import MapTile
from Unit.Tile import Tile
from Provider.PathProvider import PathProvider
import math

class MapMng :
    def __init__(self, mapSizeX, mapSizeY, imgProvider):
        self.size = Vector2(mapSizeX, mapSizeY)
        self.tile = MapTile(imgProvider)
        self.tile.resize(96)
        self.mapChanged = {}
        self.mapSwitched = {}
        self.offset = (self.size * 0.5)
        self.offset.x *= (self.tile.scale - self.tile.getShift() / 2)
        self.offset.y *= self.tile.getSizeWithoutPadding()
        self.center = Vector2(int(self.size.x / 2), int(self.size.y / 2))

        self.mosueGridPos = Vector2(0, 0)
        self.pathProvider = PathProvider()
        self.SQRT3 = math.sqrt(3)
        self.map = []
        for y in range(mapSizeY) :
            self.map.append([])
            for x in range(mapSizeX) :
                offsetY = 0 if x % 2 == 0 else self.tile.getShift()
                self.map[y].append(Tile(self.tile.tileType["Block"], ((x * (self.tile.scale - self.tile.getShift() / 2) - self.offset.x), ((y * (self.tile.getSizeWithoutPadding()) + offsetY) - self.offset.y)), (x, y), self.tile.scale))

    def toWorldPosition(self, pos) :
        return self.map[int(pos.y)][int(pos.x)].center
       
    # 마우스 좌표를 인덱스 형태로 변환
    def point_in_hex(self, px, py, center, radius):
        # 마우스 좌표를 타일 중심 좌표로 변환
        dx = abs(px - center.x) / radius
        dy = abs(py - center.y) / radius

        return (dy <= self.SQRT3 / 2) and (self.SQRT3 * dx + dy <= self.SQRT3)

    # 마우스 좌료를 인덱스 형태로 변환한 후의 보정
    def getHex(self, x, y):
        tileWidth = self.tile.scale
        tileHeight = self.tile.getSizeWithoutPadding()
        shiftY = self.tile.getShift()

        px = x + self.offset.x
        py = y + self.offset.y

        xStep = tileWidth - shiftY / 2
        xIndex = int(px // xStep)

        if xIndex % 2 == 0:
            py_adj = py
        else:
            py_adj = py - shiftY

        yIndex = int(py_adj // tileHeight)

        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                cx = xIndex + dx
                cy = yIndex + dy
                if 0 <= cx < self.size.x and 0 <= cy < self.size.y:
                    tile = self.map[cy][cx]
                    if self.point_in_hex(x, y, tile.center, tileWidth / 2):
                        return Vector2(cx, cy)

        return Vector2(xIndex, yIndex)
    
    # 마우스 클릭한 위치가 같은 위치인지 판다ㅏㄴ
    def isSameTarget(self, target) :
        return self.mosueGridPos == self.getHex(target.x, target.y)
    
    # 경로 탐색 함수
    def findPath(self, playerPos, targetPos, path) :
        # 마우스 위치나 특정 오브젝트 위치를 맵 인덱스 형태로 변경
        # 사각형이 아닌 육각형으로 맵을 구성하였기에 판정 또한 육각형을 기준으로 해야함함
        self.mosueGridPos = self.getHex(targetPos.x, targetPos.y)

        # if self.getMapIndex(self.mosueGridPos) == 0 :
        #     self.setMapIndexWithSplash(self.mosueGridPos, "Normal")

        # 변환한 인덱스를 가지고 A* 알고리즘 사용용
        path = self.pathProvider.a_star(self.map, playerPos, self.mosueGridPos)
        print(path)
        # 경로를 다른 블록으로 변경하여 경로를 시각적으로 표시
        if path:
            for i in range(1, len(path)):
                self.setMapIndex(Vector2(path[i][0], path[i][1]), "Path")
        
        # 경로 반환
        return path

    # 맵 전체가 아닌 바뀔 필요가 있는 타일만 업데이트
    def Update(self, input, camera, dt) :
        for key in list(self.mapSwitched.keys()):
            self.mapSwitched[key].Update(dt)

    # 맵을 그리기 위한 함수
    def Draw(self, camera, screen):
        for y in range(int(self.size.y)):
            for x in range(int(self.size.x)):
                # 맵의 인덱스마다 타일을 그림
                self.map[y][x].Draw(self.tile, camera, screen)

    # 업데이트가 필요 없어지면 딕셔너리에서 삭제
    def removeUpdateList(self, pos) :
        del self.mapSwitched[(pos.x, pos.y)]

    # 하나의 칸만 바꾸기 위한 함수
    # 바꾸기 이전 데이터가 유의미하다면 저장
    def setMapIndex(self, pos, t) :
        self.mapSwitched[(pos.x, pos.y)] = self.map[int(pos.y)][int(pos.x)]
        # print(self.mapSwitched)
        if self.getMapIndex(pos) < 2 :
            self.mapChanged[(pos.x, pos.y)] = self.map[int(pos.y)][int(pos.x)].getTileType()
        if self.getMapIndex(pos) == 3 and t == 0 :
            t = 1
        self.map[int(pos.y)][int(pos.x)].setTileType(self.tile.tileType[t] if type(t) == str else t, lambda: self.removeUpdateList(pos))

    # 맵이 바뀌기 전의 상태를 저장하고 있다가 바뀔 때 이전 상태로 되돌리기 위한 함수수
    def getMapChangeIndex(self, pos) :
        if pos in self.mapChanged :
            idx = self.mapChanged[pos]
            del self.mapChanged[pos]
            return idx
        return "Normal"

    # 주변 칸까지 바꾸기 위한 함수
    def setMapIndexWithSplash(self, pos, tileType) :
        self.setMapIndex(pos, tileType)
        self.showNeighborMap(int(pos.x), int(pos.y))

    # 선택한 칸 주변 칸을 뒤집기 위한 함수
    def showNeighborMap(self, x, y) :
        # 3X3으로 탐색하지만 3X3 모두 바꾸면 칸의 모양이 이상하기에
        # 원하는 모양으로 만들기 위해서는 232 구조가 되어야 한다
        '''
                X   
            X       X
                X
            X       X
                X
        '''
        skipYIndex = 1 if x % 2 == 0 else -1
        for i in range(-1, 2, 1) :
            for j in range(-1, 2, 1) :
                if (i == 0 and j == 0) or (i == skipYIndex and j != 0): continue
                dX = x + j
                dY = y + i
                # 배열의 범위를 넘어가지 않게
                if(dX >= 0 and dX < self.size.x and dY >= 0 and dY < self.size.y) : 
                    if self.map[dY][dX].getTileType() == 0:
                        self.setMapIndex(Vector2(dX, dY), "Normal")
                        # self.map[dY][dX] = self.tile.tileType["Normal"]

    def getMapIndex(self, pos) :
        return self.map[int(pos.y)][int(pos.x)].getTileType()