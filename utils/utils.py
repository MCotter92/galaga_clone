import os

import pygame


def load_png(img_path, width, height, angle_x=0):
    """Load image and return image object"""

    try:
        image = pygame.image.load(img_path)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
        scale = pygame.transform.scale(image, (width, height))
        image = pygame.transform.rotate(scale, angle_x)
    except FileNotFoundError:
        print(f"Cannot load image: {img_path}")
        raise SystemExit
    return image
