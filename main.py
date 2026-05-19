import pygame

from assets.bullet import Bullet
from assets.colors import GREEN
from assets.enemy import Enemy
from assets.groups import all_sprites, bullets, enemies
from assets.helpers import straight_line
from assets.level import Level
from assets.paths import (
    CosinePath,
    ReverseZigZagPath,
    SinePath,
    StraightPath,
    ZigZagPath,
)
from assets.player import Player


WIDTH, HEIGHT = (1080, 700)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = (55, 40)
FPS = 60
VELO = 10
BULLETS_VELOCITY = 10
RED = (255, 0, 0)

HIT_COOLDOWN = 1000  # milliseconds

Player1 = Player(
    name="Player1",
    img="assets/images/spaceship_red.png",
    width=SPACESHIP_WIDTH,
    height=SPACESHIP_HEIGHT,
    angle=180,
    max_health=100,
    current_health=100,
    coords=((WIDTH / 2) - 27.3, 600),
)

all_sprites.add(Player1)

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
            max_health=100,
            current_health=100,
            coords=[x, y],
            start_x=x,
            speed=1,
            path=ReverseZigZagPath(amplitude=80, frequency=0.1),
        )
        enemies.add(enemy)
        all_sprites.add(enemy)
        i += 1
        x += 100
    return enemies


def level_generator(name, image, resolution, num_enemies) -> Level:
    return Level(
        name,
        image,
        resolution[0],
        resolution[1],
        0,
        create_enemies(num_enemies, SPACESHIP_WIDTH - 5, SPACESHIP_HEIGHT - 5),
        Player1,
    )


def draw_window(level: Level, enemies, bullets):
    WINDOW.blit(level.img, (0, 0))
    level.player.draw(WINDOW)

    for enemy in enemies:
        enemy.draw(WINDOW)

    for bullet in bullets:
        WINDOW.blit(bullet.surf, (bullet.rect.left, bullet.rect.top))
    pygame.display.flip()


def detect_bullet_enemies_collisions(bullets, enemies):
    for bullet in bullets:
        hit_enemy = pygame.sprite.spritecollideany(bullet, enemies)
        if hit_enemy:
            hit_enemy.current_health -= 25
            hit_enemy.healthbar.current_health = hit_enemy.current_health
            bullet.kill()
            if hit_enemy.current_health <= 0:
                hit_enemy.kill()


def detect_player_enemies_collisions(player, enemies):
    run = True
    now = pygame.time.get_ticks()

    for enemy in pygame.sprite.spritecollide(player, enemies, False):
        if now - player.last_hit_time > HIT_COOLDOWN:
            enemy.current_health -= 25
            enemy.healthbar.current_health = enemy.current_health
            if enemy.current_health <= 0:
                enemy.kill()
            player.current_health -= 25
            player.healthbar.current_health = player.current_health
            player.last_hit_time = now

            if player.current_health <= 0:
                player.register_death()
                run = False
                return run
    return run


def main():
    clock = pygame.time.Clock()
    run = True
    enemy_count = 3
    level_count = 1
    level = level_generator(
        f"Level {level_count}", "assets/images/space.png", (WIDTH, HEIGHT), enemy_count
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

        Player1.calculate_movement(keys_pressed, VELO, WIDTH, HEIGHT)
        detect_bullet_enemies_collisions(bullets, enemies)
        run = detect_player_enemies_collisions(Player1, enemies)
        bullets.update(WIDTH, HEIGHT)
        enemies.update(WIDTH, HEIGHT)
        Player1.update_pos()
        draw_window(level, enemies, bullets)
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
