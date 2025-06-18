import pygame

# 좌측 위에 표시되는 UI
class HeroUI : 
    def __init__(self, imgPro) :
        self.profile = pygame.Surface((64, 32), pygame.SRCALPHA)
        self.spBar = pygame.Surface((48, 6), pygame.SRCALPHA)
        self.position = pygame.Vector2(40, 40)

        self.profile.blits([(imgPro.getImage("UI", "Profile"), (0, 0)), (imgPro.getImage("UI", "SpBar"), (40, 19))])
        self.profile = pygame.transform.scale(self.profile, (self.profile.get_size()[0] * 3, self.profile.get_size()[1] * 3))
        
        self.apRect = self.spBar.get_rect(topleft=(self.position.x + 126, self.position.y + 63))
        self.apColor = (205, 174, 152)
        self.maxRect = self.apRect.copy()

    def setAp(self, Ap) :
        self.apRect.width = int(self.maxRect.width * Ap)

    def Draw(self, camera, screen) :
        screen.blit(self.profile, self.position)
        pygame.draw.rect(screen, self.apColor, self.apRect)
        
        # screen.blit(self.back, pygame.Vector2(40, 40))
        # screen.blit(self.hpBar, pygame.Vector2(161, 62))
        # screen.blit(self.spBar, pygame.Vector2(161, 96))