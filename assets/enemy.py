from collections import deque

import pygame

from logging_config import get_logger

from assets.healthbar import HealthBar
from assets.spritesheet_registry import SPRITESHEET_REGISTRY as sr

from utils.utils import load_png
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
        start_x,
        start_y,
        route,
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

        # position data
        self.width = width
        self.height = height
        self.rect.topleft = [start_x, start_y]
        self.position = pygame.Vector2(self.rect.topleft)
        self.anchor = pygame.Vector2(start_x, start_y)
        self.route = route
        self.next_routes = deque()

        # health data
        self.max_health = max_health
        self.current_health = current_health
        self.healthbar = HealthBar(
            max_health=self.max_health,
            current_health=self.current_health,
            coords=[self.rect.topleft[0], self.rect.topleft[1] - 10],
            width=self.width,
        )
        self.last_hit_time = 0
        logger.info(
            "Enemy '%s' created at (%.0f, %.0f)",
            name,
            self.rect.topleft[0],
            self.rect.topleft[1],
        )

    def update(self, dt, window_height):
        if self.rect is None:
            logger.error("Enemy '%s' has None rect", self.name)
            raise ValueError("self.rect is None")
        else:
            self.position = self.anchor + pygame.Vector2(self.route.update(dt))
            if self.route.finished:
                self._advance_route()
            self.rect.topleft = (self.position[0], self.position[1])
            self.healthbar.rect.bottomleft = (
                self.position[0],
                self.position[1] - 10,
            )

            if self.rect.topleft[1] > window_height + 25:
                logger.debug("Enemy '%s' removed — off-screen", self.name)
                self.kill()

    def queue_route(self, route):
        self.next_routes.append(route)

    def _advance_route(self):
        if self.next_routes:
            self._switch_route(self.next_routes.popleft())
        else:
            self.route.reset()

    def _switch_route(self, route):
        # Re-anchor so the new route starts exactly where the enemy is now.
        self.anchor = self.position - pygame.Vector2(route.curve(route.t))
        self.route = route

    def draw(self, surface):
        self.current_frame += 1
        if self.current_frame >= len(self.frames):
            self.current_frame = 0
        self.surf = self.frames[self.current_frame]
        if self.rect is not None:
            surface.blit(self.surf, (self.rect.topleft[0], self.rect.topleft[1]))
        else:
            raise ValueError("self.rect.topleft is None")

        self.healthbar.draw(surface)
