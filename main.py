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
    logger.info("======================= main() called =============================")
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
            figure_eight(100, 100),
            # TODO: I need to play with Route and figure_eight() to get the curve correct.
            math.pi,
        ),
    )
    all_sprites_group.add(player1, enemy)
    logger.info(
        f"player1 and enemy added to all_sprites_group. num of sprites in all_sprites_group {len(all_sprites_group)}"
    )
    enemies_group.add(enemy)
    logger.info(
        f"enemy added to enemies_group. num of emeines in enemies_group {len(enemies_group)}"
    )

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
        enemies_group.update(dt, WINDOW_HEIGHT)
        player1.update()
    pygame.quit()


if __name__ == "__main__":
    main()
