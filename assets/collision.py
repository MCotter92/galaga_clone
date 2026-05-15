import pygame


class Collision:
    def __init__(self, enemies, player, bullets):
        self.enemies = enemies
        self.player = player
        self.bullets = bullets

    def check_collisions(self, enemies, player, bullets):
        # if any enemy has collieded with the player
        enemy_to_player = pygame.sprite.spritecollideany(player, enemies)
        if enemy_to_player:
            player.hp -= 2
            enemy_to_player.kill()
            if player.hp <= 0:
                player.kill()
                # end the game somehow here

        for bullet in bullets.sprites():
            bullet_to_enemy = pygame.sprite.spritecollideany(bullet, enemies)
            if bullet_to_enemy:
                bullet_to_enemy.kill()
                bullet.kill()
