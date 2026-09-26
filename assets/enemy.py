import pygame

from logging_config import get_logger

from assets.healthbar import HealthBar
from assets.route import Route
from assets.spritesheet_registry import SPRITESHEET_REGISTRY as sr

from utils.utils import load_png
from utils.utils import extract_frames

from game_math.curves import figure_eight


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
        self.start_x = start_x
        self.start_y = start_y
        self.route = route

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
        logger.debug(
            "Enemy '%s' created at (%.0f, %.0f)",
            name,
            self.rect.topleft[0],
            self.rect.topleft[1],
        )

    def update(self, dt, window_height):
        # TODO: The parameter order here is `(dt, window_height)`, but the call site in
        # `main` invokes `enemies_group.update(WINDOW_HEIGHT, dt)`, and
        # `pygame.sprite.Group.update` forwards those two values positionally. The result
        # is that `dt` is bound to 700 and `window_height` is bound to roughly 0.0167.
        # Fix the mismatch and then consider whether the signature should be reordered or
        # renamed so the order cannot be guessed wrong, since nothing in the type
        # annotations will catch a swapped pair of floats.
        if self.rect is None:
            logger.error("Enemy '%s' has None rect", self.name)
            raise ValueError("self.rect is None")
        else:
            # TODO: This assigns the route's return value directly to `rect.topleft`,
            # which means the route is required to emit absolute screen coordinates. The
            # curve in `game_math.curves` emits offsets around the origin instead, so
            # `start_x` and `start_y` are applied once in `__init__` and then silently
            # discarded on the first update. This is why the enemy jumps into the
            # top-left corner. Whichever contract is chosen, it should be visible here
            # at the point of use, either by adding `start_x` / `start_y` to the route's
            # output, or by storing the spawn point on the enemy and adding it here.
            self.rect.topleft = self.route.update(dt)
            # TODO: The health bar tracks `rect.topleft` by rebuilding its position from
            # scratch every frame. That works, but it means the bar has no notion of its
            # own anchor and cannot be offset for enemies that are taller than 54 pixels,
            # where a fixed 10-pixel gap above the sprite will overlap it.
            self.healthbar.rect.bottomleft = (
                self.rect.topleft[0],
                self.rect.topleft[1] - 10,
            )

            # TODO: The 25-pixel margin is a magic number that happens to be large enough
            # to hide the sprite's full height. It is also the value that turns the
            # swapped-argument bug above into a self-destruct: with `window_height`
            # holding a fraction of a second instead of 700, the effective threshold
            # becomes about 25 pixels and a curve oscillating around the origin crosses it
            # on roughly half of all frames. Once the argument order is fixed this
            # threshold is harmless, but it is worth deriving it from the sprite height or
            # naming it as a constant, so that a future change to the argument order
            # fails loudly instead of looking like an enemy that vanishes at random.
            if self.rect.topleft[1] > window_height + 25:
                logger.debug("Enemy '%s' removed — off-screen", self.name)
                self.kill()

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
