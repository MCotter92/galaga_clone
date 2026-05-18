import pygame

from assets.bullet import Bullet
from assets.colors import GREEN
from assets.enemy import Enemy
from assets.groups import all_sprites, bullets, enemies
from assets.helpers import straight_line
from assets.level import Level
from assets.player import Player


WIDTH, HEIGHT = (1080, 700)
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = (55, 40)
FPS = 60
VELO = 10
BULLETS_VELOCITY = 10
RED = (255, 0, 0)

Player1 = Player(
    name="Player1",
    img="assets/images/spaceship_red.png",
    width=SPACESHIP_WIDTH,
    height=SPACESHIP_HEIGHT,
    angle=180,
    hp=100,
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
            hp=50,
            coords=(x, y),
        )
        line_path = straight_line(enemy.coords[0], HEIGHT)
        enemy.sprite_path = line_path
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
    WINDOW.blit(level.player.img, (level.player.x_coord, level.player.y_coord))

    for enemy in enemies:
        WINDOW.blit(enemy.img, (enemy.x_coord, enemy.y_coord))

    for bullet in bullets:
        WINDOW.blit(bullet.surf, (bullet.rect.left, bullet.rect.top))
    pygame.display.flip()


def handle_bullets(bullets, enemies):
    for bullet in bullets:
        hit_enemy = pygame.sprite.spritecollideany(bullet, enemies)
        if hit_enemy:
            hit_enemy.hp -= 25
            bullet.kill()
            if hit_enemy.hp <= 0:
                hit_enemy.kill()


def handle_crashes(player, enemies):
    for enemy in pygame.sprite.spritecollide(player, enemies, False):
        enemy.hp -= 25
        player.hp -= 25
        print("player hp: ", player.hp)
        print("enemy hp: ", enemy.hp)
        if enemy.hp <= 0:
            enemy.kill()
        if player.hp <= 0:
            player.register_death()


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

        Player1.move(keys_pressed, VELO, WIDTH, HEIGHT)
        handle_bullets(bullets, enemies)
        handle_crashes(Player1, enemies)
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
