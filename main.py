import pygame

from assets import player
from logging_config import setup_logging, get_logger
from assets.level import Level
from assets.bullet import Bullet
from assets.colors import GREEN
from assets.groups import all_sprites_group, bullets_group, enemies_group
from assets.player import Player
from factory.factory import create_enemies, level_generator
from collisions.collisions import (
    detect_bullet_enemies_collisions,
    detect_player_enemies_collisions,
)
from renderers.renderers import draw_window


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
    Player1 = Player(
        name="Player1",
        sr_entry="tinyShip3.png",
        width=27,
        height=27,
        angle=0,
        max_health=100,
        current_health=100,
        coords=((WINDOW_WIDTH / 2) - 27.3, WINDOW_HEIGHT - 50),
    )
    all_sprites_group.add(Player1)
    enemy_count = 3
    level_count = 1
    enemy_list = ["tinyShip1.png", "tinyShip4.png", "tinyShip6.png"]

    logger.info("======================= Game started =============================")
    run = True
    while run:
        dt = min(clock.tick(FPS) / 1000, MAX_DT)
        level_count += 1
        enemy_count += 1
        logger.info("Level complete — advancing to level %d", level_count)
        draw_window(
            "assets/images/background-black.png",
            Player1,
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
                            Player1.x_coord + (Player1.width / 2),
                            Player1.y_coord + (Player1.height / 2),
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

        Player1.calculate_movement(keys_pressed, PLAYER_VELO * dt, WINDOW_WIDTH)
        detect_bullet_enemies_collisions(bullets_group, enemies_group)
        player_alive = detect_player_enemies_collisions(
            Player1, enemies_group, HIT_COOLDOWN
        )
        if not player_alive:
            run = False
            break
        bullets_group.update(WINDOW_WIDTH, WINDOW_HEIGHT)
        enemies_group.update(WINDOW_HEIGHT)
        Player1.update()
    pygame.quit()


if __name__ == "__main__":
    main()
