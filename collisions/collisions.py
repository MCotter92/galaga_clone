import pygame

from logging_config import get_logger

logger = get_logger("collisions")


def detect_bullet_enemies_collisions(bullets, enemies):
    for bullet in bullets:
        hit_enemy = pygame.sprite.spritecollideany(bullet, enemies)
        if hit_enemy:
            hit_enemy.current_health -= 25
            hit_enemy.healthbar.current_health = hit_enemy.current_health
            bullet.kill()
            logger.info(
                "Bullet hit '%s' — HP: %d/%d",
                hit_enemy.name,
                hit_enemy.current_health,
                hit_enemy.max_health,
            )
            if hit_enemy.current_health <= 0:
                logger.info("Enemy '%s' destroyed", hit_enemy.name)
                hit_enemy.kill()


def detect_player_enemies_collisions(player, enemies, hit_cooldown):
    player_alive = True
    now = pygame.time.get_ticks()

    for enemy in pygame.sprite.spritecollide(player, enemies, False):
        if now - player.last_hit_time > hit_cooldown:
            enemy.current_health -= 25
            enemy.healthbar.current_health = enemy.current_health
            if enemy.current_health <= 0:
                logger.info("Enemy '%s' destroyed by collision", enemy.name)
                enemy.kill()
            player.current_health -= 25
            player.healthbar.current_health = player.current_health
            player.last_hit_time = now
            logger.warning(
                "Player hit by '%s' — HP: %d/%d",
                enemy.name,
                player.current_health,
                player.max_health,
            )

            if player.current_health <= 0:
                player.register_death()
                player_alive = False
                return player_alive
    return player_alive
