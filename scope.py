import pygame
from sprite import Sprite
from loaders import load_image


class Scope(Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.x = 0
        self.y = 0
        self.image = load_image("scope.png")
        self.rect = self.image.get_rect()

    def update(self, pos):
        self.x = pos[0]
        self.y = pos[1]
        self.rect.center = pos[0], pos[1]

