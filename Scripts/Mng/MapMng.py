from pygame.math import Vector2
from Util.MapTile import MapTile
import pygame
import numpy as np

class MapMng :
    def __init__(self, mapSizeX, mapSizeY, imgProvider):
        self.size = Vector2(mapSizeX, mapSizeY)
        self.tile = MapTile(imgProvider)
        self.tile.resize(64)
        self.map = np.zeros((mapSizeY, mapSizeX))
        self.offset = (self.size * 0.5) * self.tile.getSizeWithoutPadding()

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
        return self.map[y][x]