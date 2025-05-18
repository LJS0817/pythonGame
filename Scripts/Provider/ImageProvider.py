import pygame
import os

class ImageProvider :
    def __init__(self) :
        self.imageList = {}
        self.base_dir = "Sprites"

    def loadImage(self):
        for subdir, _, files in os.walk(self.base_dir):
            if(len(subdir) < 8) : continue
            group = subdir.split('\\')[1]
            if(group not in self.imageList) :
                self.imageList[group] = {}

            for file in files:
                id = file.split('.')[0]
                path = os.path.join(subdir, file)
                try :
                    self.imageList[group][id] = pygame.image.load(path)
                except pygame.error as e :
                    print(path + " 이미지 없음")
        print(self.imageList)

    def getImage(self, gid, id) :
        return self.imageList[gid][id]
