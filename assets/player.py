import pygame
from pygame.locals import K_w, K_a, K_s, K_d

from assets.entity import Entity


class Player(Entity):
    def __init__(self, name, img, width, height, angle, hp):
        super().__init__(name, img, width, height, angle)
        self.width = width
        self.height = height
        self.hp = hp
        self.coords = self.rect.center
        self.numlives = 3

    def register_death(self):
        self.numlives = self.numlives - 1
        if self.numlives == 0:
            self.kill()
            pygame.quit()

    def increase_life_count(self):
        self.numlives += 1

    def update(self, pressed_keys, display_width, display_height):
        if pressed_keys[K_w]:
            self.rect.move_ip(0, -5)
            print("moving up")
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 5)
            print("moving down")
        if pressed_keys[K_a]:
            self.rect.move_ip(-5, 0)
            print("moving left")
        if pressed_keys[K_d]:
            self.rect.move_ip(5, 0)
            print("moving right")

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > display_width:
            self.rect.right = display_width
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= display_height:
            self.rect.bottom = display_height
