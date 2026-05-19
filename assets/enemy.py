import pygame

from assets.entity import Entity
from assets.healthbar import HealthBar
from assets.paths import StraightPath


class Enemy(Entity):
    def __init__(
        self,
        name,
        img,
        width,
        height,
        angle,
        max_health,
        current_health,
        coords,
        speed,
        start_x,
        start_y=0,
        path=None,
    ):
        super().__init__(name, img, width, height, angle)
        self.surf = pygame.surface.Surface((width, height))
        self.rect: pygame.Rect = self.surf.get_rect(topleft=coords)

        self.topleft = self.rect.topleft
        self.width = width
        self.height = height
        self.coords = coords
        self.x_intercept = start_x
        self.start_x = start_x
        self.start_y = start_y
        self.coords[0] = self.start_x
        self.coords[1] = self.start_y

        self.speed = speed

        self.sprite_path = path or StraightPath()

        self.max_health = max_health
        self.current_health = current_health
        self.healthbar = HealthBar(
            max_health=self.max_health,
            current_health=self.current_health,
            coords=[self.topleft[0], self.topleft[1]],
            width=self.width,
        )

        self.last_hit_time = 0

    def update(self, window_height):
        self.coords[0] = self.sprite_path.path(self.x_intercept, self.coords[1])
        self.coords[1] += self.speed
        self.healthbar.rect.bottomleft = (
            self.coords[0],
            self.coords[1] - 10,
        )

        if self.coords[1] > window_height + 25:
            self.kill()

    def draw(self, surface):
        surface.blit(self.img, (self.coords[0], self.coords[1]))
        self.healthbar.draw(surface)
