import pygame
import math

from logging_config import setup_logging, get_logger

from assets.bullet import Bullet
from assets.colors import GREEN
from assets.groups import all_sprites_group, bullets_group, enemies_group
from assets.player import Player
from assets.enemy import Enemy
from assets.route import Route

from game_math.curves import figure_eight

from collisions.collisions import (
    detect_bullet_enemies_collisions,
    detect_player_enemies_collisions,
)

from renderers.renderers import draw_window

from utils.utils import load_png


logger = get_logger("main")

WINDOW_WIDTH, WINDOW_HEIGHT = (1080, 700)
PLAYER_WIDTH, PLAYER_HEIGHT = (54, 54)
FPS = 60
PLAYER_VELO = 600
ENEMY_VELO = 400
BULLETS_VELO = 600
RED = (255, 0, 0)
HIT_COOLDOWN = 1000  # milliseconds
MAX_DT = 1.0 / 30.0


def main():
    pygame.init()
    setup_logging()
    clock = pygame.time.Clock()
    WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Galaga Clone")
    BACKGROUND_SURF, _ = load_png("background-black.png", WINDOW_WIDTH, WINDOW_WIDTH)
    player1 = Player(
        name="Player1",
        sr_entry="tinyShip3.png",
        width=PLAYER_WIDTH,
        height=PLAYER_HEIGHT,
        angle=0,
        max_health=100,
        current_health=100,
        coords=((WINDOW_WIDTH / 2) - 27.3, WINDOW_HEIGHT - 50),
    )
    enemy = Enemy(
        name="Enemy1",
        sr_entry="tinyShip3.png",
        width=PLAYER_WIDTH,
        height=PLAYER_HEIGHT,
        angle=180,
        max_health=100,
        current_health=100,
        start_x=360,
        start_y=233,
        route=Route(
            # TODO: The call below is actually correct and this note was wrong.
            # `figure_eight(amplitude_x, amplitude_y)` returns the inner `curve(t)`
            # closure, and `Route.__init__` stores that closure as `self.curve`,
            # which is exactly the callable `Route.update` expects. The real problem
            # is that `Route.update` returns whatever the curve returns (absolute
            # coordinates around the origin) and `Enemy.update` assigns that value
            # straight to `self.rect.topleft`, so `start_x=360` / `start_y=233` are
            # used once in `__init__` and then discarded. The enemy therefore lives in
            # curve-space anchored at (0, 0), which is the top-left corner of the
            # screen. Decide deliberately whether a route describes offsets from the
            # spawn point or absolute screen positions, and make that contract
            # explicit in the signature or a docstring rather than leaving it implied
            # by a bare tuple return.
            figure_eight(50, 50),
            # TODO: Tune this once the dt plumbing is correct. At 2*math.pi radians per
            # second the Gerono curve takes 2 seconds to complete a full loop, because
            # `y = amplitude_y * sin(2 * t)` completes two cycles for every one cycle
            # of `x = amplitude_x * sin(t)`. The 50/50 amplitudes also keep the whole
            # path inside a 100x100 pixel box, which is why the motion currently reads
            # as "the enemy is not moving" rather than as a visible figure-eight.
            2 * math.pi,
        ),
    )
    all_sprites_group.add(player1, enemy)
    enemies_group.add(enemy)

    logger.info("======================= Game started =============================")
    run = True
    while run:
        dt = min(clock.tick(FPS) / 1000, MAX_DT)
        draw_window(
            BACKGROUND_SURF,
            player1,
            enemies_group,
            bullets_group,
            WINDOW,
        )
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("Quit event received")
                run = False
                break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    logger.info("Q pressed — quitting")
                    run = False
                    break
                if event.key == pygame.K_RSHIFT:
                    bullet = Bullet(
                        GREEN,
                        (
                            player1.x_coord + (player1.width / 2),
                            player1.y_coord + (player1.height / 2),
                        ),
                        BULLETS_VELO * dt,
                    )
                    bullets_group.add(bullet)
                    all_sprites_group.add(bullet)
                    logger.debug(
                        "Bullet fired at (%.0f, %.0f)",
                        bullet.rect.centerx,
                        bullet.rect.centery,
                    )
        keys_pressed = pygame.key.get_pressed()

        player1.calculate_movement(keys_pressed, PLAYER_VELO * dt, WINDOW_WIDTH)
        detect_bullet_enemies_collisions(bullets_group, enemies_group)
        player_alive = detect_player_enemies_collisions(
            player1, enemies_group, HIT_COOLDOWN
        )
        if not player_alive:
            run = False
            break
        bullets_group.update(WINDOW_WIDTH, WINDOW_HEIGHT)
        # TODO: This call passes the two arguments in the wrong order for
        # `Enemy.update(self, dt, window_height)`. `pygame.sprite.Group.update` splats
        # these positionally, so `dt` receives the constant WINDOW_HEIGHT (700) and
        # `window_height` receives the frame's real dt (about 0.0167 at 60 FPS). The two
        # downstream effects are severe: `self.route.update(dt)` advances the route's
        # `t` by roughly 4400 radians every frame, which samples the figure-eight at an
        # effectively random phase and makes the enemy jitter inside its path instead of
        # tracing it; and the off-screen check in `Enemy.update` becomes
        # `y > 0.0167 + 25`, so the enemy deletes itself roughly half the time because
        # the curve is oscillating around the origin. Either reverse the order here to
        # match the current signature, or make the signature order unambiguous so the
        # next reader cannot repeat the mistake. Passing `dt` to each sprite explicitly
        # is worth considering, since splatting positional args through a group is what
        # allowed this to go unnoticed.
        enemies_group.update(WINDOW_HEIGHT, dt)
        player1.update()
    pygame.quit()


if __name__ == "__main__":
    main()
