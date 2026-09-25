import pygame

from logging_config import get_logger
from utils.utils import load_png
from assets.healthbar import HealthBar
from assets.spritesheet_registry import SPRITESHEET_REGISTRY as sr
from utils.utils import extract_frames

logger = get_logger("player")


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        name,
        sr_entry,
        width,
        height,
        angle,
        max_health,
        current_health,
        coords,
    ):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.surf, self.rect = load_png(
            sr_entry,
            sr["tinyShip3.png"]["width"],
            sr["tinyShip3.png"]["height"],
            angle,
        )

        sheet_key = sr_entry.split("/")[-1]
        sheet = sr[sheet_key]
        self.frames = extract_frames(
            self.surf, sheet["cols"], sheet["rows"], width, height
        )
        self.current_frame = 0
        self.surf = self.frames[self.current_frame]
        self.rect = self.surf.get_rect(topleft=coords)
        self.bottomleft = self.rect.bottomleft

        # position data
        self.width = width  # render width
        self.height = height  # render height
        self.coords = coords
        self.x_coord = coords[0]
        self.y_coord = coords[1]

        # health data
        self.numlives = 1
        self.max_health = max_health
        self.current_health = current_health
        self.healthbar = HealthBar(
            max_health=self.max_health,
            current_health=self.current_health,
            coords=[self.bottomleft[0], self.bottomleft[1]],
            width=self.width,
        )
        self.last_hit_time = 0
        logger.info("Player '%s' created at (%.0f, %.0f)", name, coords[0], coords[1])

    def draw(self, surface):
        surface.blit(self.frames[self.current_frame], (self.x_coord, self.y_coord))
        self.current_frame += 1
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.surf = self.frames[self.current_frame]
        self.healthbar.draw(surface)

    def calculate_movement(self, keys_pressed, step, width):
        # move left
        if keys_pressed[pygame.K_a] and self.x_coord - step > 0:
            self.x_coord = self.x_coord - step

        # move right
        if keys_pressed[pygame.K_d] and self.x_coord + step + self.width < width:
            self.x_coord = self.x_coord + step

    def update(self):
        if self.rect is not None:
            self.rect.topleft = (self.x_coord, self.y_coord)
            self.healthbar.rect.topleft = (
                self.rect.bottomleft[0],
                self.rect.bottomleft[1] + 10,
            )

    # def update(self):
    #     self.update_pos()

    def register_death(self):
        run = True
        self.numlives = self.numlives - 1
        if self.numlives == 0:
            logger.warning("Player '%s' has died — game over", self.name)
            self.kill()
            run = False
            return run
        else:
            logger.info(
                "Player '%s' died — %d lives remaining", self.name, self.numlives
            )
            self.max_health = 100
        return run

    def increase_life_count(self):
        self.numlives += 1
