from logging_config import get_logger
from assets.enemy import Enemy
from assets.level import Level
from assets.paths import ReverseZigZagPath, StraightPath
from assets.groups import enemies_group, all_sprites_group
from assets.spritesheet_registry import SPRITESHEET_REGISTRY as sr

logger = get_logger("factory")


def create_enemies(num, enemy_list, enemies_group, step):
    logger.info("Creating %d enemies", num)
    i = 0
    x = 50
    y = 200
    if num > 10:
        logger.warning("Enemy count capped from %d to 10", num)
        num = 10

    while i < num:
        enemy = Enemy(
            name=f"Enemy{i}",
            sr_entry=enemy_list[i],
            width=36,
            height=35,
            angle=180,
            max_health=100,
            current_health=100,
            coords=[x, y],
            start_x=x,
            path=StraightPath(),
            step=step,
        )
        enemies_group.add(enemy)
        all_sprites_group.add(enemy)
        i += 1
        x += 100
    return enemies_group


def level_generator(
    name,
    sr_entry,
    window_width,
    window_height,
    num_enemies,
    enemy_list,
    enemy_velo,
    dt,
    player,
) -> Level:
    logger.info("Generating level '%s' with %d enemies", name, num_enemies)
    return Level(
        name=name,
        img=sr_entry,
        width=window_width,
        height=window_height,
        angle=0,
        enemies=create_enemies(
            num_enemies, enemy_list, enemies_group, step=enemy_velo * dt
        ),
        player=player,
    )
