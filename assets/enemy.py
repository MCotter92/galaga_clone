import pygame
from assets.entity import Entity


class Enemy(Entity):
    def __init__(self, name, img, width, height, angle, hp, coords):
        super().__init__(name, img, width, height, angle)
        self.surf = pygame.surface.Surface((width, height))
        self.rect: pygame.Rect = self.surf.get_rect(topleft=coords)

        self.hp = hp
        self.coords = coords
        self.x_coord = coords[0]
        self.y_coord = coords[1]
        self.sprite_path = []
        self.width = width
        self.height = height

    def update(self, window_width, window_height):
        self.y_coord += 1
        self.rect.topleft = (self.x_coord, self.y_coord)
        if self.y_coord > window_height + 25:
            self.kill()
