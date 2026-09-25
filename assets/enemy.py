import pygame

from logging_config import get_logger
from assets.healthbar import HealthBar
from assets.paths import StraightPath
from utils.utils import load_png
from assets.spritesheet_registry import SPRITESHEET_REGISTRY as sr
from utils.utils import extract_frames

logger = get_logger("enemy")


class Enemy(pygame.sprite.Sprite):
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
        step,
        start_x,
        start_y=0,
        path=None,
    ):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.surf, self.rect = load_png(
            sr_entry,
            sr[sr_entry]["width"],
            sr[sr_entry]["height"],
            angle,
        )

        # spritesheet data
        sheet_key = sr_entry.split("/")[-1]
        sheet = sr[sheet_key]
        self.frames = extract_frames(
            self.surf, sheet["cols"], sheet["rows"], width, height
        )
        self.current_frame = 0
        self.surf = self.frames[self.current_frame]
        self.rect = self.surf.get_rect(topleft=coords)

        # position data
        self.angel = angle
        self.width = width
        self.height = height
        self.coords = coords
        self.x_coord = coords[0]
        self.y_coord = coords[1]
        self.x_intercept = start_x
        self.start_x = start_x
        self.start_y = start_y
        self.coords[0] = self.start_x
        self.coords[1] = self.start_y
        self.speed = step
        self.sprite_path = path or StraightPath()

        # health data
        self.max_health = max_health
        self.current_health = current_health
        self.healthbar = HealthBar(
            max_health=self.max_health,
            current_health=self.current_health,
            coords=[self.rect.topleft[0], self.rect.topleft[1]],
            width=self.width,
        )
        self.last_hit_time = 0
        logger.debug("Enemy '%s' created at (%.0f, %.0f)", name, coords[0], coords[1])

    def update(self, window_height):
        if self.rect is None:
            logger.error("Enemy '%s' has None rect", self.name)
            raise ValueError("self.rect is None")
        else:
            self.coords[0] = self.sprite_path.path(self.x_intercept, self.coords[1])
            self.coords[1] += self.speed
            self.rect.topleft = (self.coords[0], self.coords[1])  # type: ignore
            self.healthbar.rect.bottomleft = (
                self.coords[0],
                self.coords[1] - 10,
            )

            if self.coords[1] > window_height + 25:
                logger.debug("Enemy '%s' removed — off-screen", self.name)
                self.kill()

    def draw(self, surface):
        self.current_frame += 1
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.surf = self.frames[self.current_frame]
        surface.blit(self.surf, (self.coords[0], self.coords[1]))

        self.healthbar.draw(surface)
