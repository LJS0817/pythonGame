import pygame
import os

class UIMng :
    def __init__(self, imPro) :
        self.font_path = os.path.join(os.path.dirname(__file__), "..","..", "Font", "font.ttf")
        # 폰트 크기 저장
        self.font = {}

    def getFont(self, size) :
        if size not in self.font:
            self.font[size] = pygame.font.Font(self.font_path, size)
        return self.font[size]