from main import HEIGHT, WIDTH
import pygame
import math
import copy
from data.map import *

def draw_player():
    if direction == 0:
        screen.blit(player_images[counter // 5],
                    (player_x, player_y))
    elif direction == 1:
        screen.blit(pygame.transform.flip(
            player_images[counter // 5], True, False),
            (player_x, player_y))
    elif direction == 2:
        screen.blit(pygame.transform.rotate(
            player_images[counter // 5], 90),
            (player_x, player_y))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(
            player_images[counter // 5], 270),
            (player_x, player_y))


def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = (HEIGHT - 50) // 32
    num2 = (WIDTH // 30)
    num3 = 15
    if centerx // 30 < 29:
        if direction == 0:
            if level[centery // num1][(centerx - num3) // num2] < 3:
                turns[1] = True
        if direction == 1:
            if level[centery // num1][(centerx + num3) // num2] < 3:
                turns[0] = True
        if direction == 2:
            if level[(centery + num3) // num1][centerx // num2] < 3:
                turns[3] = True
        if direction == 3:
            if level[(centery - num3) // num1][centerx // num2] < 3:
                turns[2] = True

        if direction == 2 or direction == 3:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num3) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num3) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num2) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num2) // num2] < 3:
                    turns[0] = True
        if direction == 0 or direction == 1:
            if 12 <= centerx % num2 <= 18:
                if level[(centery + num1) // num1][centerx // num2] < 3:
                    turns[3] = True
                if level[(centery - num1) // num1][centerx // num2] < 3:
                    turns[2] = True
            if 12 <= centery % num1 <= 18:
                if level[centery // num1][(centerx - num3) // num2] < 3:
                    turns[1] = True
                if level[centery // num1][(centerx + num3) // num2] < 3:
                    turns[0] = True
    else:
        turns[0] = True
        turns[1] = True

    return turns


def move_player(play_x, play_y):
    if direction == 0 and turns_allowed[0]:
        play_x += player_speed
    elif direction == 1 and turns_allowed[1]:
        play_x -= player_speed
    if direction == 2 and turns_allowed[2]:
        play_y -= player_speed
    elif direction == 3 and turns_allowed[3]:
        play_y += player_speed
    return play_x, play_y


def get_targets(red_x, red_y, blue_x, blue_y, green_x, green_y, yellow_x, yellow_y):
    if player_x < 450:
        runaway_x = 900
    else:
        runaway_x = 0
    if player_y < 450:
        runaway_y = 900
    else:
        runaway_y = 0
    return_target = (380, 400)
    if powerup:
        if not red.dead and not eaten_ghost[0]:
            red_target = (runaway_x, runaway_y)
        elif not red.dead and eaten_ghost[0]:
            if 340 < red_x < 560 and 340 < red_y < 500:
                red_target = (400, 100)
            else:
                red_target = (player_x, player_y)
        else:
            red_target = return_target
        if not blue.dead and not eaten_ghost[1]:
            blue_target = (runaway_x, player_y)
        elif not blue.dead and eaten_ghost[1]:
            if 340 < blue_x < 560 and 340 < blue_y < 500:
                blue_target = (400, 100)
            else:
                blue_target = (player_x, player_y)
        else:
            blue_target = return_target
        if not green.dead:
            green_target = (player_x, runaway_y)
        elif not green.dead and eaten_ghost[2]:
            if 340 < green_x < 560 and 340 < green_y < 500:
                green_target = (400, 100)
            else:
                green_target = (player_x, player_y)
        else:
            green_target = return_target
        if not yellow.dead and not eaten_ghost[3]:
            yellow_target = (450, 450)
        elif not yellow.dead and eaten_ghost[3]:
            if 340 < yellow_x < 560 and 340 < yellow_y < 500:
                yellow_target = (400, 100)
            else:
                yellow_target = (player_x, player_y)
        else:
            yellow_target = return_target
    else:
        if not red.dead:
            if 340 < red_x < 560 and 340 < red_y < 500:
                red_target = (400, 100)
            else:
                red_target = (player_x, player_y)
        else:
            red_target = return_target
        if not blue.dead:
            if 340 < blue_x < 560 and 340 < blue_y < 500:
                blue_target = (400, 100)
            else:
                blue_target = (player_x, player_y)
        else:
            blue_target = return_target
        if not green.dead:
            if 340 < green_x < 560 and 340 < green_y < 500:
                green_target = (400, 100)
            else:
                green_target = (player_x, player_y)
        else:
            green_target = return_target
        if not yellow.dead:
            if 340 < yellow_x < 560 and 340 < yellow_y < 500:
                yellow_target = (400, 100)
            else:
                yellow_target = (player_x, player_y)
        else:
            yellow_target = return_target
    return [red_target, blue_target,
            green_target, yellow_target]