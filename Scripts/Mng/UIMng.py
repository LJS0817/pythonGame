import pygame
from Unit.UI.HeroUI import HeroUI

class UIMng :
    def __init__(self, imPro) :
        self.font = pygame.font.SysFont('malgungothic', 16)
        self.heroUI = HeroUI(imPro)

    def Draw(self, camera, screen) :
        self.heroUI.Draw(camera, screen)