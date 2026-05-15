import math
import os

import pygame

from utils.utils import load_png


class Entity(pygame.sprite.Sprite):
    def __init__(self, name, img, initial_width, initial_height, initial_angle):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.surface = load_png(img, initial_width, initial_height, initial_angle)
        self.rect = self.surface.get_rect()

        screen = pygame.display.get_surface()
        self.screen = screen
        self.area = self.screen.get_rect()
