import pygame

from assets.bullet import Bullet
from assets.colors import GREEN
from assets.groups import all_sprites, bullets, enemies
from assets.player import Player
from factory.factory import level_generator
from collisions.collisions import (
    detect_bullet_enemies_collisions,
    detect_player_enemies_collisions,
)
from renderers.renderers import draw_window


WINDOW_WIDTH, WINDOW_HEIGHT = (1080, 700)
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
PLAYER_WIDTH, PLAYER_HEIGHT = (100, 100)
FPS = 60
VELO = 10
BULLETS_VELOCITY = 10
RED = (255, 0, 0)
HIT_COOLDOWN = 1000  # milliseconds

Player1 = Player(
    name="Player1",
    img="assets/images/tiny-spaceships/tinyShip2.png",
    width=PLAYER_WIDTH,
    height=PLAYER_HEIGHT,
    angle=180,
    max_health=100,
    current_health=100,
    coords=((WINDOW_WIDTH / 2) - 27.3, 600),
)
all_sprites.add(Player1)


def main():
    clock = pygame.time.Clock()
    run = True
    enemy_count = 3
    level_count = 1
    level = level_generator(
        name=f"Level {level_count}",
        image="assets/images/background-black.png",
        window_width=WINDOW_WIDTH,
        window_height=WINDOW_HEIGHT,
        num_enemies=enemy_count,
        player=Player1,
        player_height=PLAYER_HEIGHT,
        player_width=PLAYER_WIDTH,
    )
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                    pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RSHIFT:
                    bullet = Bullet(
                        GREEN,
                        (
                            level.player.x_coord + (level.player.width / 2),
                            level.player.y_coord + (level.player.height / 2),
                        ),
                    )
                    bullets.add(bullet)
                    all_sprites.add(bullet)
        keys_pressed = pygame.key.get_pressed()

        Player1.calculate_movement(keys_pressed, VELO, WINDOW_WIDTH, WINDOW_HEIGHT)
        detect_bullet_enemies_collisions(bullets, enemies)
        run = detect_player_enemies_collisions(Player1, enemies, HIT_COOLDOWN)
        bullets.update(WINDOW_WIDTH, WINDOW_HEIGHT)
        enemies.update(WINDOW_HEIGHT)
        Player1.update_pos()
        draw_window(level, enemies, bullets, WINDOW)
        if len(level.enemies) == 0:
            level_count += 1
            enemy_count += 1
            level = level_generator(
                name=f"Level {level_count}",
                image="assets/images/space.png",
                window_width=WINDOW_WIDTH,
                window_height=WINDOW_HEIGHT,
                num_enemies=enemy_count,
                player=Player1,
                player_height=PLAYER_HEIGHT,
                player_width=PLAYER_WIDTH,
            )


if __name__ == "__main__":
    main()
