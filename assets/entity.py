import pygame

from utils.utils import load_png


class Entity(pygame.sprite.Sprite):
    def __init__(self, name, img, initial_width, initial_height, initial_angle):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.img, self.rect = load_png(
            img, initial_width, initial_height, initial_angle
        )
        self.screen = pygame.display.get_surface()
        self.area = self.screen.get_rect()
