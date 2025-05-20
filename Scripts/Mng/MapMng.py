from pygame.math import Vector2
from Util.MapTile import MapTile
from Unit.Tile import Tile
from Provider.PathProvider import PathProvider
import pygame
import numpy as np
import math

class MapMng :
    def __init__(self, mapSizeX, mapSizeY, imgProvider):
        self.size = Vector2(mapSizeX, mapSizeY)
        self.tile = MapTile(imgProvider)
        self.tile.resize(64)
        self.mapChanged = {}
        self.mapSwitched = {}
        self.offset = (self.size * 0.5)
        self.offset.x *= (self.tile.scale - self.tile.getShift() / 2)
        self.offset.y = (self.offset.y * self.tile.getSizeWithoutPadding()) + (self.tile.getSizeWithoutPadding() / 2)
        self.center = Vector2(int(self.size.x / 2), int(self.size.y / 2))

        self.mosueGridPos = Vector2(0, 0)
        self.pathProvider = PathProvider()
        
        self.map = []
        for y in range(mapSizeY) :
            self.map.append([])
            for x in range(mapSizeX) :
                offsetY = 0 if x % 2 == 0 else self.tile.halfScale - (self.tile.padding * 0.5)
                self.map[y].append(Tile(self.tile.tileType["Block"], ((x * (self.tile.scale - 16) - self.offset.x), ((y * (self.tile.scale - self.tile.padding) + offsetY) - self.offset.y)), (x, y), self.tile.scale))

    def toWorldPosition(self, pos) :
        return self.map[int(pos.y)][int(pos.x)].center
        # return pos * self.tile.scale

    def axial_round(self, hex_coords):
        q, r = hex_coords
        s = -q - r
        rq = round(q)
        rr = round(r)
        rs = round(s)
        q_diff = abs(rq - q)
        r_diff = abs(rr - r)
        s_diff = abs(rs - s)
        if q_diff > r_diff and q_diff > s_diff:
            rq = -rr - rs
        elif r_diff > s_diff:
            rr = -rq - rs
        else:
            rs = -rq - rr
        return Vector2(rq, rr) + self.center

    def getHex(self, x, y) :
        q = round((2./3. * x) / self.tile.halfScale)
        r = round((-1./3. * x + math.sqrt(3)/3. * y) / self.tile.halfScale)
        if q < 0 and q % 2 == 1 : r -= 1
        return Vector2(q, r + int(q  / 2))
    
    def isSameTarget(self, target) :
        return self.mosueGridPos == self.getHex(target.x, target.y) + self.center
    
    def findPath(self, playerPos, targetPos, path) :
        self.mosueGridPos = self.getHex(targetPos.x, targetPos.y) + self.center
        # if self.getMapIndex(self.mosueGridPos) == 0 :
        #     self.setMapIndexWithSplash(self.mosueGridPos, "Normal")
        path = self.pathProvider.a_star(self.map, playerPos, self.mosueGridPos)
        print(path)
        if path:
            for i in range(1, len(path)):
                self.setMapIndex(Vector2(path[i][0], path[i][1]), "Path")
        return path

    # 맵 전체가 아닌 바뀔 필요가 있는 타일만 업데이트
    def Update(self, input, camera, dt) :
        for key in list(self.mapSwitched.keys()):
            self.mapSwitched[key].Update(dt)
        # for y in range(int(self.size.y)):
        #     for x in range(int(self.size.x)):
        #         self.map[y][x].Update(dt)

    # 맵을 그리기 위한 함수
    def Draw(self, camera, screen):
        for y in range(int(self.size.y)):
            for x in range(int(self.size.x)):
                # 맵의 인덱스마다 타일을 그림
                self.map[y][x].Draw(self.tile, camera, screen)
                # offsetY = 0 if x % 2 == 0 else self.tile.halfScale - (self.tile.padding * 0.5)
                # screen.blit(self.tile.getTile(self.map[y][x]), ((x * (self.tile.scale - 16) - self.offset.x)  - camera.getPosition().x, ((y * (self.tile.scale - self.tile.padding) + offsetY) - self.offset.y) - camera.getPosition().y))

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
        if self.map[int(pos.y)][int(pos.x)].getTileType() == 3 and t == 0 :
            t = 1
        self.map[int(pos.y)][int(pos.x)].setTileType(self.tile.tileType[t] if type(t) == str else t, lambda: self.removeUpdateList(pos))

    # 
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