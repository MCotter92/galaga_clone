from assets.enemy import Enemy
from assets.level import Level
from assets.paths import ReverseZigZagPath
from assets.groups import enemies, all_sprites


def create_enemies(num, width, height):
    i = 0
    x = 50
    y = 200
    if num > 10:
        num = 10

    while i < num:
        enemy = Enemy(
            name=f"Enemy{i}",
            img="assets/images/spaceship_yellow.png",
            width=width,
            height=height,
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


def level_generator(
    name,
    image,
    window_width,
    window_height,
    num_enemies,
    player,
    player_height,
    player_width,
) -> Level:
    return Level(
        name=name,
        img=image,
        width=window_width,
        height=window_height,
        angle=0,
        enemies=create_enemies(num_enemies, player_width - 5, player_height - 5),
        player=player,
    )
