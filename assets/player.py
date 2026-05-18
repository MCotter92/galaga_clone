import pygame

from assets.entity import Entity


class Player(Entity):
    def __init__(self, name, img, width, height, angle, hp, coords):
        super().__init__(name, img, width, height, angle)
        self.surf = pygame.surface.Surface([width, height])
        self.rect: pygame.Rect = self.surf.get_rect(topleft=coords)
        self.width = width
        self.height = height
        self.hp = hp
        self.coords = coords
        self.x_coord = coords[0]
        self.y_coord = coords[1]
        self.numlives = 1

    def move(self, keys_pressed, velo, width, height):
        # move left
        if keys_pressed[pygame.K_a] and self.x_coord - velo > 0:
            self.x_coord = self.x_coord - velo

        # move right
        if keys_pressed[pygame.K_d] and self.x_coord + velo + self.width < width:
            self.x_coord = self.x_coord + velo

        # move up
        if keys_pressed[pygame.K_w] and self.y_coord - velo > 0:
            if self.y_coord <= 500:
                self.y_coord = 500
            else:
                self.y_coord = self.y_coord - velo

        # move down
        if keys_pressed[pygame.K_s] and self.y_coord + velo + self.height < height:
            self.y_coord += velo

    def update_pos(self):
        self.rect.topleft = (self.x_coord, self.y_coord)

    def register_death(self):
        self.numlives = self.numlives - 1
        if self.numlives == 0:
            self.kill()
            pygame.quit()
        else:
            self.hp = 100

    def increase_life_count(self):
        self.numlives += 1
