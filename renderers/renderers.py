import pygame


def draw_window(level_img_surf, player, enemies, bullets, window):
    window.blit(level_img_surf, (0, 0))
    player.draw(window)

    for enemy in enemies:
        enemy.draw(window)

    for bullet in bullets:
        window.blit(bullet.surf, (bullet.rect.left, bullet.rect.top))
    pygame.display.flip()
