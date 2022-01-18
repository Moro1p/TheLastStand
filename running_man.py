from sprite import Sprite
from loaders import load_image


class RunningMan(Sprite):
    def __init__(self, x, y, enemies_group):
        super().__init__(enemies_group)
        self.x = x
        self.y = y
        self.S = 0
        self.image = load_image(f'running_man_frames/{self.S}.gif', -1)
        self.rect = self.image.get_rect().move(self.x, self.y)

    def lose_check(self):
        if self.x >= 670:
            return True
        else:
            return False

    def update(self, v):
        self.x += v
        self.S += 1
        self.rect = self.image.get_rect().move(self.x, self.y)
        self.image = load_image(f'running_man_frames/{self.S % 24}.gif', -1)

    def shot(self, pos):
        if self.rect[0] < pos[0] < (self.rect[0] + self.rect[2]):
            if self.rect[1] < pos[1] < (self.rect[1] + self.rect[3]):
                return True
        else:
            return False
