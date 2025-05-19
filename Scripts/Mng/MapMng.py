from pygame.math import Vector2
from Util.MapTile import MapTile
import pygame
import numpy as np
import math

class MapMng :
    def __init__(self, mapSizeX, mapSizeY, imgProvider):
        self.size = Vector2(mapSizeX, mapSizeY)
        self.tile = MapTile(imgProvider)
        self.tile.resize(64)
        self.map = np.zeros((mapSizeY, mapSizeX))
        self.offset = (self.size * 0.5)
        self.offset.x *= (self.tile.scale - self.tile.getShift() / 2)
        self.offset.y = (self.offset.y * self.tile.getSizeWithoutPadding()) + (self.tile.getSizeWithoutPadding() / 2)

        self.mousePos = None
        self.r = 32
        self.w = self.r*2
        self.h = self.tile.getSizeWithoutPadding()

    def getHex(self, x, y) :
        if self.mousePos == None :
             self.mousePos = Vector2()

        r2 = self.r / 2
        h2 = self.h / 2
        xx = math.floor(x / r2)
        yy = math.floor(y / h2)
        xpos = math.floor(xx / 3)
        xx %= 6
        
        if xx % 3 == 0 :
            xa = (x % r2) / r2
            ya = (y % h2) / h2
            if yy % 2 == 0 :
                ya = 1 - ya
            if xx == 3 :
                xa = 1 - xa
            if xa > ya :
                self.mousePos.x = xpos + (-1 if xx == 3 else 0)
                self.mousePos.y = math.floor(yy / 2)
                return self.mousePos
            self.mousePos.x = xpos + (-1 if xx == 0 else 0)
            self.mousePos.y = math.floor((yy + 1) / 2)
            return self.mousePos
        if xx < 3 :
            self.mousePos.x = xpos + (-1 if xx == 3 else 0)
            self.mousePos.y = math.floor(yy / 2)
            return self.mousePos
        self.mousePos.x = xpos + (-1 if xx == 0 else 0)
        self.mousePos.y = math.floor((yy + 1) / 2)
        return self.mousePos
        

    def Update(self, input, camera, dt) :
        print(self.getHex(input.getMousePosition().x, input.getMousePosition().y))
        # pass

    def Draw(self, camera, screen):
        for y in range(int(self.size.y)):
            for x in range(int(self.size.x)):
                offsetY = 0 if x % 2 == 0 else self.tile.halfScale - (self.tile.padding * 0.5)
                screen.blit(self.tile.getTile(self.map[y][x]), ((x * (self.tile.scale - 16) - self.offset.x)  - camera.getPosition().x, ((y * (self.tile.scale - self.tile.padding) + offsetY) - self.offset.y) - camera.getPosition().y))

    def center(self):
        return Vector2(int(self.size.x / 2), int(self.size.y / 2))
    
    def setMapIndex(self, pos, t) :
        print(pos)
        self.map[int(pos.y)][int(pos.x)] = self.tile.tileType[t]

    def getMapIndex(self, pos) :
        return self.map[int(pos.y)][int(pos.x)]