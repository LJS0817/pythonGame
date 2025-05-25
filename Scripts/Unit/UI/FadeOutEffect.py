import pygame

class FadeEffect:
    def __init__(self, text_surface, position):
        self.text_surface = text_surface.copy()
        self.start_pos = position
        self.current_pos = position
        self.alpha = 255
        self.timer = 0
        self.duration = 1.0  # seconds
        self.padding = 8

    def update(self, dt):
        self.timer += dt
        progress = self.timer / self.duration

        # 위치 이동 (위로)
        self.current_pos.y = self.start_pos.y - (progress * 1.5)

        # 투명도 감소
        self.alpha = max(0, 255 - int(progress * 255))

        return self.timer < self.duration  # 살아있는 동안 True

    def draw(self, screen, camera):
        text_rect = self.text_surface.get_rect(center=(self.current_pos.x, self.current_pos.y - 20) - camera.getPosition())

        bg_rect = pygame.Rect(
            text_rect.x - self.padding,
            text_rect.y - self.padding,
            text_rect.width + 2 * self.padding,
            text_rect.height + 2 *self. padding
        )

        # 배경 그리기 (반투명 검정 또는 다른 색)
        bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        bg_surface.fill((0, 0, 0, int(self.alpha * 0.7)))  # alpha 적용

        # 배경 먼저 그리기
        screen.blit(bg_surface, (bg_rect.x, bg_rect.y))
        self.text_surface.set_alpha(self.alpha)
        # screen.blit(self.text_surface, camera.getCenter())  # 살짝 위로 띄움
        screen.blit(self.text_surface, text_rect)  # 살짝 위로 띄움
