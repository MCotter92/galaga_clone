import pygame

from assets.bullet import Bullet
from assets.collision import Collision
from assets.colors import BLACK, GREEN
from assets.enemy import Enemy
from assets.groups import all_sprites, bullets, enemies
from assets.helpers import check_collisions
from assets.level import Level
from assets.player import Player

WIDTH, HEIGHT = (1080, 700)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = (55, 40)
FPS = 60
VELO = 10
BULLETS_VELOCITY = 10
RED = (255, 0, 0)

SPACESHIP = Player(
    name="Player1",
    img="assets/images/spaceship_red.png",
    width=SPACESHIP_WIDTH,
    height=SPACESHIP_HEIGHT,
    angle=180,
    hp=100,
)
SPACESHIP.rect.move_ip(WIDTH // 2, 500)
all_sprites.add(SPACESHIP)

# ENEMY_HIT = pygame.USEREVENT


def create_enemies(num, width, height):
    i = 0
    x = 50
    y = 200
    if num > 10:
        num = 10

    while i < num:
        enemy = Enemy(
            f"Enemy{i}",
            "assets/images/spaceship_yellow.png",
            width,
            height,
            angle=0,
            hp=50,
        )
        # line_path = straight_line(enemy.coords[0], HEIGHT)
        # enemy.sprite_path = line_path
        enemies.add(enemy)
        all_sprites.add(enemy)

        i += 1
        x += 100
        # print(enemy.sprite_path)
    return enemies


def level_generator(name, image, resolution, num_enemies) -> Level:
    return Level(
        name,
        image,
        resolution[0],
        resolution[1],
        0,
        create_enemies(num_enemies, SPACESHIP_WIDTH - 5, SPACESHIP_HEIGHT - 5),
        SPACESHIP,
    )


def main():
    clock = pygame.time.Clock()
    run = True
    enemy_count = 3
    level_count = 1
    level = level_generator(
        f"Level {level_count}",
        "assets/images/space.png",
        (WIDTH, HEIGHT),
        enemy_count,
    )

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RSHIFT:
                    bullet = Bullet(
                        GREEN,
                        (
                            SPACESHIP.rect.center[0],
                            SPACESHIP.rect.center[1],
                        ),
                    )
                    bullets.add(bullet)
                    all_sprites.add(bullet)
        keys_pressed = pygame.key.get_pressed()

        spaceship_movement(keys_pressed)

        Collision.check_collisions(
            enemies,
            level.player,
            bullets,
        )

        bullets.update(keys_pressed, WIDTH, HEIGHT)
        level.enemies.update(keys_pressed, WIDTH, HEIGHT)
        SPACESHIP.update(keys_pressed, WIDTH, HEIGHT)
        all_sprites.update(keys_pressed, WIDTH, HEIGHT)

        WINDOW.blit(level.surface, (level.rect.x, level.rect.y))
        WINDOW.blit(SPACESHIP.surface, (SPACESHIP.rect.x, SPACESHIP.rect.y))
        for bullet in bullets.sprites():
            WINDOW.blit(bullet.surf, (bullet.rect.x, bullet.rect.y))
        x = 100
        for enemy in level.enemies.sprites():
            enemy.rect.x = x
            WINDOW.blit(enemy.surface, (enemy.rect.x, enemy.rect.y))
            x += 300

        pygame.display.flip()

        if len(level.enemies) == 0:
            level_count += 1
            enemy_count += 1
            level = level_generator(
                f"Level {level_count}",
                "assets/images/space.png",
                (WIDTH, HEIGHT),
                enemy_count,
            )


if __name__ == "__main__":
    main()
