import pygame

from assets.entity import Entity
from assets.healthbar import HealthBar


class Enemy(Entity):
    def __init__(
        self, name, img, width, height, angle, max_health, current_health, coords
    ):
        super().__init__(name, img, width, height, angle)
        self.surf = pygame.surface.Surface((width, height))
        self.rect: pygame.Rect = self.surf.get_rect(topleft=coords)
        self.topleft = self.rect.topleft
        self.width = width
        self.height = height
        self.coords = coords
        self.x_coord = coords[0]
        self.y_coord = coords[1]

        self.sprite_path = []

        self.max_health = max_health
        self.current_health = current_health
        self.healthbar = HealthBar(
            max_health=self.max_health,
            current_health=self.current_health,
            coords=[self.topleft[0], self.topleft[1]],
            width=self.width,
        )

        self.last_hit_time = 0

    def update(self, window_width, window_height):
        self.y_coord += 1
        self.rect.topleft = (self.x_coord, self.y_coord)
        self.healthbar.rect.bottomleft = (
            self.rect.topleft[0],
            self.rect.topleft[1] - 10,
        )
        if self.y_coord > window_height + 25:
            self.kill()

    def draw(self, surface):
        surface.blit(self.img, (self.x_coord, self.y_coord))
        self.healthbar.draw(surface)
