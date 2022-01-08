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
    intro_text = ["Последний рубеж", "", "", "", "", "Новая игра"]

    click_sound = pygame.mixer.Sound('data/click_sound3.mp3')
    fon = pygame.transform.scale(load_image('start_fon_1.jpg'), screen_size)
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 0
    for line in intro_text:
        string_rendered = font.render(line, True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 300
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
        clock = pygame.time.Clock()

    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                if 600 > event.pos[0] > 300 and 185 > event.pos[1] > 160:
                    play = False
        pygame.display.flip()
        clock.tick(FPS)


def main():
    song = pygame.mixer.Sound('data/soundtrack.mp3')
    song.play()
    fon2 = pygame.transform.scale(load_image('fon2.jpg'), screen_size)
    screen.blit(fon2, (0, 0))
    clock = pygame.time.Clock()
    play = True
    while play:
        if not pygame.mixer.get_busy():
            song.play()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
        pygame.display.flip()
        clock.tick(FPS)


def end_screen():
    pass


if __name__ == '__main__':
    start_screen()
    main()
    end_screen()
    terminate()

