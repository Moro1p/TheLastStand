import pygame
import sys
from sprite_group import SpriteGroup
from loaders import load_image, load_sound
from running_man import RunningMan
from scope import Scope
from randomizer import get_random_coords
from sprite import Sprite
import sqlite3


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
    pygame.draw.rect(screen, (255, 255, 255), (290, 150, 130, 35))
    pygame.draw.rect(screen, (0, 0, 0), (290, 150, 130, 35), width= 1)
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
                if 420 > event.pos[0] > 290 and 185 > event.pos[1] > 150:
                    play = False
        pygame.display.flip()
        clock.tick(FPS)


def main():
    shot = False
    reload_time = 40
    s = 0
    end_upgrade = False

    reload_process = False
    sp = []
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not reload_process and not (0 < event.pos[0] < 51 and 0 < event.pos[1] < 51) and not end_upgrade:
                    reload_process = True
                    for elem in enemies:
                        shoot_sound.set_volume(0.5)
                        shoot_sound.play()
                        sp = [event.pos[0], event.pos[1]]
                        if elem.shot(event.pos):
                            shot = True
                            enemies.remove(elem)
                            elem.kill()
                            points += 1
                            money += 2
                            break
                if 0 < event.pos[0] < 51 and 0 < event.pos[1] < 51 and not end_upgrade:
                    if reload_time <= 3:
                        end_upgrade = True
                    else:
                        if money >= 5:
                            money -= 5
                        reload_time -= 4
                        pygame.draw.rect(screen, (200, 200, 200), (1, 20, 50, 50))
                        pygame.draw.rect(screen, (0, 0, 0), (1, 20, 50, 50), width=1)
                        pygame.draw.line(screen, (0, 0, 0), (23, 25), (23, 65))
                        pygame.draw.line(screen, (0, 0, 0), (26, 25), (26, 65))
                        pygame.draw.line(screen, (0, 0, 0), (5, 43), (45, 43))
                        pygame.draw.line(screen, (0, 0, 0), (5, 46), (45, 46))
                        pygame.draw.rect(screen, (200, 200, 200), (24, 24, 2, 44))
                        pygame.draw.rect(screen, (200, 200, 200), (4, 44, 44, 2))

        if not enemies:
            for x, y in get_random_coords(num_enemies):
                num_enemies += 2
                r = RunningMan(x, y, enemies_group)
                enemies.append(r)

        line_group.update(screen)
        line_group.draw(screen)
        screen.fill((0, 0, 0))
        screen.blit(fon2, (0, 0))
        if shot:
            pygame.draw.line(screen, (253, 106, 2), (sp[0], sp[1]), (731, 218), width=5)
            shot = False
        enemies_group.draw(screen)
        enemies_group.update(1)

        font = pygame.font.Font(None, 30)
        pygame.draw.rect(screen, (255, 255, 255), (300, 0, 250, 30))
        pygame.draw.rect(screen, (0, 0, 0), (300, 0, 250, 30), width=1)
        string_rendered = font.render(f"Money: {money}  Score: {points}", True, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        intro_rect.x = 310
        intro_rect.y = 5
        screen.blit(string_rendered, intro_rect)

        if not end_upgrade:
            pygame.draw.rect(screen, (255, 255, 255), (1, 20, 50, 50))
            pygame.draw.rect(screen, (0, 0, 0), (1, 20, 50, 50), width=1)
            pygame.draw.line(screen, (0, 0, 0), (23, 25), (23, 65))
            pygame.draw.line(screen, (0, 0, 0), (26, 25), (26, 65))
            pygame.draw.line(screen, (0, 0, 0), (5, 43), (45, 43))
            pygame.draw.line(screen, (0, 0, 0), (5, 46), (45, 46))
            pygame.draw.rect(screen, (255, 255, 255), (24, 24, 2, 44))
            pygame.draw.rect(screen, (255, 255, 255), (4, 44, 44, 2))
            string_rendered = font.render(f"upgrade", True, pygame.Color('black'))
            intro_rect = string_rendered.get_rect()
            intro_rect.x = 1
            intro_rect.y = 1
            screen.blit(string_rendered, intro_rect)

        if reload_process:
            pygame.draw.rect(screen, (6, 139, 6), (600, 5, s + (100 // reload_time), 20))
            s += 100 / reload_time
            if s >= 100:
                s = 0
                reload_process = False

        if pygame.mouse.get_focused():
            players_sprites_group.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

        for enemy in enemies:
            if pygame.sprite.spritecollideany(enemy, line_group):
                lost = True
                play = False
        if points == 10:
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
    con = sqlite3.connect('chart.db')
    cur = con.cursor()
    cur.execute(f"""INSERT INTO scores (value) VALUES ({score})""")
    con.commit()
    con.close()
    terminate()
