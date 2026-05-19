import pygame


def draw_window(level, enemies, bullets, window):
    window.blit(level.img, (0, 0))
    level.player.draw(window)

    for enemy in enemies:
        enemy.draw(window)

    for bullet in bullets:
        window.blit(bullet.surf, (bullet.rect.left, bullet.rect.top))
    pygame.display.flip()
