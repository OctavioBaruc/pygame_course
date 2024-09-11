from main import HEIGHT, WIDTH
import pygame
import math
import copy
from data.map import *

def draw_misc():
    score_text = font.render(f'Score: {score}', True, '#00e6fc')
    screen.blit(score_text, (10, 920))
    if powerup:
        pygame.draw.circle(screen, '#d52b1e', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(
            player_images[0], (30, 30)), (650 + i * 40, 915))
    if game_over:
        pygame.draw.rect(screen, '#00e6fc',
                         [265, 215, 370, 120], 0, 10)
        pygame.draw.rect(screen, "#0d1117",
                         [270, 220, 360, 110], 0, 10)
        gameover_text = font.render(
            'Game over! Space bar to restart!', True, '#d52b1e')
        screen.blit(gameover_text, (290, 265))
    if game_won:
        pygame.draw.rect(screen, '#00e6fc',
                         [265, 215, 370, 120], 0, 10)
        pygame.draw.rect(screen, '#151515',
                         [270, 220, 360, 110], 0, 10)
        gameover_text = font.render(
            'Victory! Space bar to restart!', True, '#00ff00')
        screen.blit(gameover_text, (307, 265))


def check_collisions(scor, power, power_count, eaten_ghosts):
    num1 = (HEIGHT - 50) // 32
    num2 = WIDTH // 30
    if 0 < player_x < 870:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            scor += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            scor += 50
            power = True
            power_count = 0
            eaten_ghosts = [False, False, False, False]
    return scor, power, power_count, eaten_ghosts


def draw_borders():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, '#faeb7f',
                                   (j * num2 + (0.5 * num2),
                                    i * num1 + (0.5 * num1)),
                                   4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, '#faeb7f',
                                   (j * num2 + (0.5 * num2),
                                    i * num1 + (0.5 * num1)),
                                   10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color,
                                 (j * num2 + (0.5 * num2),
                                  i * num1),
                                 (j * num2 + (0.5 * num2),
                                  i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color,
                                 (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2,
                                  i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2,
                                 (i * num1 + (0.5 * num1)),
                                 num2, num1],
                                0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)),
                                 (i * num1 + (0.5 * num1)),
                                 num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color,
                                [(j * num2 + (num2 * 0.5)),
                                 (i * num1 - (0.4 * num1)),
                                 num2, num1], PI,
                                3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color,
                                [(j * num2 - (num2 * 0.4)) - 2,
                                 (i * num1 - (0.4 * num1)),
                                 num2, num1], 3 * PI / 2,
                                2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, '#faeb7f',
                                 (j * num2, i * num1 + (0.5 * num1)),
                                 (j * num2 + num2,
                                  i * num1 + (0.5 * num1)), 3)
