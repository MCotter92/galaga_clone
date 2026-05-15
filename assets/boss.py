from enemy import Enemy


class Boss(Enemy):
    def __init__(self, name, img, width, height, angle, hp, coords):
        super().__init__(name, img, width, height, angle, hp)
