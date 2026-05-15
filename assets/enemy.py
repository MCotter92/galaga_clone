from assets.entity import Entity


class Enemy(Entity):
    def __init__(self, name, img, width, height, angle, hp):
        super().__init__(name, img, width, height, angle)

        self.hp = hp
        self.sprite_path = []
        self.width = width
        self.height = height

    def update(self, keys_pressed, window_height, window_width):

        self.rect.move_ip(0, 1)
        if self.rect.y > window_height + 25:
            self.kill()
