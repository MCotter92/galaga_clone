import pygame


class Bullet(pygame.sprite.Sprite):
    def __init__(self, color, coordinates, speed=-10):
        super(Bullet, self).__init__()
        self.surf = pygame.surface.Surface((10, 25))
        self.surf.fill(color)
        self.rect: pygame.Rect = self.surf.get_rect(
            center=(
                coordinates[0],
                coordinates[1],
            )
        )
        assert self.rect is not None
        self.speed = speed

    def update(self, window_width, window_height):
        self.rect.move_ip(0, self.speed)

        if self.rect.top <= 0:
            self.kill()
        elif self.rect.top >= window_height:
            self.kill()
        elif self.rect.left <= 0:
            self.kill()
        elif self.rect.left >= window_width:
            self.kill()
