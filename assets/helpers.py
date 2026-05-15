import pygame

# from assets.entity import Entity
# from assets.enemy import Enemy
# from assets.player import Player


def check_collisions(player, enemies, bullets):

    # if any enemy has collieded with the player
    enemy_to_player = pygame.sprite.spritecollideany(player, enemies)
    if enemy_to_player is not None:
        player.kill()
        enemy_to_player.kill()

    for bullet in bullets.sprites():
        bullet_to_enemy = pygame.sprite.spritecollideany(bullet, enemies)
        if bullet_to_enemy:
            bullet_to_enemy.kill()
