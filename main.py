import pygame
import sys
from sprite_group import SpriteGroup
from loaders import load_image, load_sound
from running_man import RunningMan
from scope import Scope
from randomizer import get_random_coords
from sprite import Sprite


pygame.mixer.init()
pygame.init()
screen_size = (800, 450)
screen = pygame.display.set_mode(screen_size)
FPS = 50

enemies_group = SpriteGroup()
players_sprites_group = SpriteGroup()
line_group = SpriteGroup()
enemies = []


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
            elif event.type == event.type == pygame.MOUSEBUTTONDOWN:
                click_sound.play()
                if 600 > event.pos[0] > 300 and 185 > event.pos[1] > 160:
                    play = False
        pygame.display.flip()
        clock.tick(FPS)


def main():
    line = Sprite(line_group)
    line.image = load_image('line_image.png')
    line.rect = line.image.get_rect().move(670, 0)
    shoot_sound = load_sound('Gun_shot.mp3')
    pygame.mouse.set_visible(False)
    song = load_sound('soundtrack.mp3')
    song.play()
    song.set_volume(0.1)
    fon2 = pygame.transform.scale(load_image('fon2.jpg'), screen_size)
    screen.blit(fon2, (0, 0))
    clock = pygame.time.Clock()
    play = True
    cursor = Scope(players_sprites_group)
    num_enemies = 0

    pygame.draw.rect(screen, (255, 255, 255), (300, 0, 200, 30))
    for x, y in get_random_coords(num_enemies):
        r = RunningMan(x, y, enemies_group)
        enemies.append(r)
    points = 0
    money = 0

    while play:

        if not pygame.mixer.get_busy():
            song.play()
            song.set_volume(0.1)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
                terminate()
            if event.type == pygame.MOUSEMOTION:
                cursor.update(event.pos)
            if event.type == pygame.MOUSEBUTTONUP:
                for elem in enemies:
                    if elem.shot(event.pos):
                        shoot_sound.play()
                        enemies.remove(elem)
                        elem.kill()
                        points += 1
                        money += 1
                        break

        if not enemies:
            for x, y in get_random_coords(num_enemies):
                if num_enemies < 10:
                    num_enemies += 2
                r = RunningMan(x, y, enemies_group)
                enemies.append(r)

        line_group.update(screen)
        line_group.draw(screen)
        screen.fill((0, 0, 0))
        screen.blit(fon2, (0, 0))
        enemies_group.draw(screen)
        enemies_group.update(1)

        font = pygame.font.Font(None, 30)
        pygame.draw.rect(screen, (255, 255, 255), (300, 0, 200, 30))
        string_rendered = font.render(str(points), True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 400
        screen.blit(string_rendered, intro_rect)

        if pygame.mouse.get_focused():
            players_sprites_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)
        for enemy in enemies:
            if pygame.sprite.spritecollideany(enemy, line_group):
                lost = True
                play = False
        if points == 1:
            song.stop()
            lost = False
            play = False
    if lost:
        song.stop()
        return True, points
    else:
        song.stop()
        return False, points


def end_screen_lose(points):
    song = load_sound('losing_sound.wav')
    song.play()
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(True)
    screen.fill((0, 0, 0))
    image = pygame.transform.scale(load_image('lose.png'), (700, 200))
    play = True
    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.MOUSEBUTTONUP and 446 > event.pos[0] > 395 and 425 > event.pos[0] > 395:
                terminate()
        screen.fill((200, 200, 200))
        screen.blit(image, (50, 0))
        font = pygame.font.Font(None, 30)
        pygame.draw.rect(screen, (0, 128, 0), (395, 395, 51, 30))

        string1_rendered = font.render(f'Score: {points}', True, pygame.Color('black'))
        intro_rect = string1_rendered.get_rect()
        intro_rect.x = 400
        intro_rect.y = 200
        screen.blit(string1_rendered, intro_rect)

        string2_rendered = font.render("Exit", True, pygame.Color('white'))
        intro_rect = string2_rendered.get_rect()
        intro_rect.x = 400
        intro_rect.y = 400
        screen.blit(string2_rendered, intro_rect)

        pygame.display.flip()
        clock.tick(FPS)


def end_screen_win(points):
    win_song = load_sound('win_sound.mp3')
    win_song.play()
    clock = pygame.time.Clock()
    pygame.mouse.set_visible(True)
    screen.fill((0, 0, 0))
    image = pygame.transform.scale(load_image('win.png'), (700, 200))
    play = True

    while play:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play = False
            if event.type == pygame.MOUSEBUTTONUP and 446 > event.pos[0] > 395 and 425 > event.pos[0] > 395:
                terminate()
        screen.fill((200, 200, 200))
        screen.blit(image, (50, 0))
        font = pygame.font.Font(None, 30)
        pygame.draw.rect(screen, (0, 128, 0), (395, 395, 51, 30))

        string1_rendered = font.render(f'Score: {points}', True, pygame.Color('black'))
        intro_rect = string1_rendered.get_rect()
        intro_rect.x = 370
        intro_rect.y = 200
        screen.blit(string1_rendered, intro_rect)

        string_rendered = font.render("Exit", True, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 400
        intro_rect.y = 400
        screen.blit(string_rendered, intro_rect)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    start_screen()
    situation, score = main()
    if situation:
        end_screen_lose(score)
    else:
        end_screen_win(score)
    terminate()
