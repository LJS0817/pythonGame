import pygame
import os

class ImageProvider :
    def __init__(self) :
        # Sprites/ 아래 있는 이미지 불러오기 위한 딕셔너리
        self.imageList = {}
        self.base_dir = "Sprites"

    def loadImage(self):
        # Sprites/ 아래 있는 이미지 불러오기
        for subdir, _, files in os.walk(self.base_dir):
            if(len(subdir) < 8) : continue
            group = subdir.split('\\')[1]
            # Aseprite 원본 이미지 파일은 제외
            if group == 'Aseprite' : continue
            # 디렉토리 명으로 그룹 생성
            if(group not in self.imageList) :
                self.imageList[group] = {}

            # 파일 확장자 제외
            for file in files:
                id = file.split('.')[0]
                path = os.path.join(subdir, file)
                try :
                    self.imageList[group][id] = pygame.image.load(path)
                except pygame.error as e :
                    print(path + " 이미지 없음")
        print(self.imageList)

    # 이미지 반환
    def getImage(self, gid, id) :
        return self.imageList[gid][id]
    
    # 애니메이션을 포함한 이미지를 리스트 형태로 반환
    def getAnimatedImage(self, gid, id, size) :
        return [self.imageList[gid][f"{id}{i}"] for i in range(1, size + 1)]
