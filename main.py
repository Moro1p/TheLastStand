import pygame
import os
import sys


pygame.mixer.init()
pygame.init()
screen_size = (800, 450)
screen = pygame.display.set_mode(screen_size)
FPS = 50


class SpriteGroup(pygame.sprite.Group):

    def __init__(self):
        super().__init__()

    def get_event(self, event):
        for sprite in self:
            sprite.get_event(event)


class Sprite(pygame.sprite.Sprite):

    def __init__(self, group):
        super().__init__(group)
        self.rect = None

    def get_event(self, event):
        pass


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    image = image.convert_alpha()
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    return image


def load_sound(name):
    fullname = os.path.join('data', name)
    try:
        sound = pygame.mixer.Sound(fullname)
    except pygame.error as message:
        print('Не удаётся загрузить:', name)
        raise SystemExit(message)
    return sound


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    pass


def main():
    pass


def end_screen():
    pass


if __name__ == '__main__':
    start_screen()
    main()
    end_screen()
    terminate()

