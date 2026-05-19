import pygame


class HealthBar:
    def __init__(self, max_health, current_health, coords, width, height=3):
        self.max_health = max_health
        self.current_health = current_health
        self.width = width
        self.height = height
        self.position = coords
        self.rect = pygame.Rect(coords[0], coords[1] + 5, width, height)

    def take_damage(self, amount):
        self.current_health = max(0, self.current_health - amount)

    def draw(self, surface):
        pygame.draw.rect(surface, (200, 0, 0), self.rect)
        ratio = max(0, min(self.current_health / self.max_health, 1))
        fill_rect = pygame.Rect(
            self.rect.left,
            self.rect.top,
            int(self.width * ratio),
            self.height,
        )
        pygame.draw.rect(surface, (0, 200, 0), fill_rect)
