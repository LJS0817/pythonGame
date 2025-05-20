import pygame

class HeroUI : 
    def __init__(self, imgPro) :
        self.profile = pygame.Surface((64, 32), pygame.SRCALPHA)
        # self.back = pygame.transform.scale(self.back, (self.back.get_size()[0] * 3, self.back.get_size()[1] * 3))
        # self.hpBar = pygame.transform.scale(self.hpBar, (self.hpBar.get_size()[0] * 3, self.hpBar.get_size()[1] * 3))
        self.hpBar = pygame.Surface((48, 6), pygame.SRCALPHA)
        self.spBar = pygame.Surface((48, 6), pygame.SRCALPHA)
        self.position = pygame.Vector2(40, 40)
        # self.spBar = imgPro.getImage("UI", "SpBar")
        # self.spBar = pygame.transform.scale(self.spBar, (self.spBar.get_size()[0] * 3, self.spBar.get_size()[1] * 3))

        self.profile.blits([(imgPro.getImage("UI", "Profile"), (0, 0)), (imgPro.getImage("UI", "HpBar"), (40, 8)), (imgPro.getImage("UI", "SpBar"), (40, 19))])
        self.profile = pygame.transform.scale(self.profile, (self.profile.get_size()[0] * 3, self.profile.get_size()[1] * 3))

    def Draw(self, camera, screen) :
        screen.blit(self.profile, self.position)
        pygame.draw.rect(screen, (223, 124, 124), self.hpBar.get_rect(topleft=(self.position.x + 126, self.position.y + 30))) # 빨간색 HP 바
        pygame.draw.rect(screen, (126, 173, 153), self.spBar.get_rect(topleft=(self.position.x + 126, self.position.y + 63))) # 빨간색 HP 바
        
        # screen.blit(self.back, pygame.Vector2(40, 40))
        # screen.blit(self.hpBar, pygame.Vector2(161, 62))
        # screen.blit(self.spBar, pygame.Vector2(161, 96))