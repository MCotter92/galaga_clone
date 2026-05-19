import pygame


def detect_bullet_enemies_collisions(bullets, enemies):
    for bullet in bullets:
        hit_enemy = pygame.sprite.spritecollideany(bullet, enemies)
        if hit_enemy:
            hit_enemy.current_health -= 25
            hit_enemy.healthbar.current_health = hit_enemy.current_health
            bullet.kill()
            if hit_enemy.current_health <= 0:
                hit_enemy.kill()


def detect_player_enemies_collisions(player, enemies, hit_cooldown):
    run = True
    now = pygame.time.get_ticks()

    for enemy in pygame.sprite.spritecollide(player, enemies, False):
        if now - player.last_hit_time > hit_cooldown:
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
