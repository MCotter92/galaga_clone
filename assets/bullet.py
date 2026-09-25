import pygame

from logging_config import get_logger

logger = get_logger("bullet")


class Bullet(pygame.sprite.Sprite):
    def __init__(self, color, coordinates, step):
        super(Bullet, self).__init__()
        self.surf = pygame.surface.Surface((5, 25))
        self.surf.fill(color)
        self.rect: pygame.Rect = self.surf.get_rect(
            center=(
                coordinates[0],
                coordinates[1],
            )
        )
        assert self.rect is not None
        self.step = (
            step * -1
        )  # move the bullets up the screen. Positive would be down. Freakin' comp sci
        logger.debug("Bullet spawned at (%.0f, %.0f)", coordinates[0], coordinates[1])

    def update(self, window_width, window_height):
        self.rect.move_ip(0, self.step)

        if (
            self.rect.top <= 0
            or self.rect.top >= window_height
            or self.rect.left <= 0
            or self.rect.left >= window_width
        ):
            logger.debug(
                "Bullet removed — off-screen at (%d, %d)",
                self.rect.centerx,
                self.rect.centery,
            )
            self.kill()
