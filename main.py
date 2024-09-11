from data.draw import check_collisions, draw_borders, draw_misc
from data.ghosts import Ghost
from data.player import check_position, draw_player, get_targets, move_player
import pygame
import math
import copy
from data.map import *

if __name__ == '__main__':
    pygame.init()
    WIDTH = 900
    HEIGHT = 950
    SCREEN = pygame.display.set_mode([WIDTH, HEIGHT])
    TIMER = pygame.time.Clock()
    FPS = 60
    FONT = pygame.font.Font('freesansbold.ttf', 20)
    LEVEL = copy.deepcopy(map)
    COLOR = '#0000cc'
    PI = math.pi
    player_images = []
    for i in range(1, 5):
        player_images.append(pygame.transform.scale(pygame.image.load(
            f'pacman/img/{i}.png'), (45, 45)))
    red_img = pygame.transform.scale(pygame.image.load(
        f'pacman/img/red.png'), (45, 45))
    green_img = pygame.transform.scale(pygame.image.load(
        f'pacman/img/green.png'), (45, 45))
    blue_img = pygame.transform.scale(pygame.image.load(
        f'pacman/img/blue.png'), (45, 45))
    yellow_img = pygame.transform.scale(pygame.image.load(
        f'pacman/img/yellow.png'), (45, 45))
    spooked_img = pygame.transform.scale(pygame.image.load(
        f'pacman/img/powerup.png'), (45, 45))
    dead_img = pygame.transform.scale(pygame.image.load(
        f'pacman/img/dead.png'), (45, 45))

    player_x = 450
    player_y = 663
    direction = 0
    red_x = 56
    red_y = 58
    red_direction = 0
    blue_x = 440
    blue_y = 388
    blue_direction = 2
    green_x = 440
    green_y = 400
    green_direction = 2
    yellow_x = 440
    yellow_y = 438
    yellow_direction = 2
    counter = 0
    flicker = False

    turns_allowed = [False, False, False, False]
    direction_command = 0
    player_speed = 2
    score = 0
    powerup = False
    power_counter = 0
    eaten_ghost = [False, False, False, False]
    targets = [(player_x, player_y),
               (player_x, player_y),
               (player_x, player_y),
               (player_x, player_y)]
    red_dead = False
    blue_dead = False
    yellow_dead = False
    green_dead = False
    red_box = False
    blue_box = False
    yellow_box = False
    green_box = False
    moving = False
    ghost_speeds = [2, 2, 2, 2]
    startup_counter = 0
    lives = 3
    game_over = False
    game_won = False

    run = True
    while run:
        timer.tick(fps)
        if counter < 19:
            counter += 1
            if counter > 3:
                flicker = False
        else:
            counter = 0
            flicker = True
        if powerup and power_counter < 600:
            power_counter += 1
        elif powerup and power_counter >= 600:
            power_counter = 0
            powerup = False
            eaten_ghost = [False, False, False, False]
        if startup_counter < 180 and not game_over and not game_won:
            moving = False
            startup_counter += 1
        else:
            moving = True

        screen.fill('#151515')
        draw_borders()
        center_x = player_x + 23
        center_y = player_y + 24
        if powerup:
            ghost_speeds = [1, 1, 1, 1]
        else:
            ghost_speeds = [2, 2, 2, 2]
        if eaten_ghost[0]:
            ghost_speeds[0] = 2
        if eaten_ghost[1]:
            ghost_speeds[1] = 2
        if eaten_ghost[2]:
            ghost_speeds[2] = 2
        if eaten_ghost[3]:
            ghost_speeds[3] = 2
        if red_dead:
            ghost_speeds[0] = 4
        if blue_dead:
            ghost_speeds[1] = 4
        if green_dead:
            ghost_speeds[2] = 4
        if yellow_dead:
            ghost_speeds[3] = 4

        game_won = True
        for i in range(len(level)):
            if 1 in level[i] or 2 in level[i]:
                game_won = False

        player_circle = pygame.draw.circle(screen, '#0d1117',
                                           (center_x, center_y), 20, 2)
        draw_player()
        red = Ghost(red_x, red_y, targets[0],
                    ghost_speeds[0], red_img,
                    red_direction, red_dead,
                    red_box, 0)
        blue = Ghost(blue_x, blue_y, targets[1],
                     ghost_speeds[1], blue_img,
                     blue_direction, blue_dead,
                     blue_box, 1)
        green = Ghost(green_x, green_y, targets[2],
                      ghost_speeds[2], green_img,
                      green_direction, green_dead,
                      green_box, 2)
        yellow = Ghost(yellow_x, yellow_y, targets[3],
                       ghost_speeds[3], yellow_img,
                       yellow_direction, yellow_dead,
                       yellow_box, 3)
        draw_misc()
        targets = get_targets(red_x, red_y, blue_x, blue_y,
                              green_x, green_y, yellow_x, yellow_y)

        turns_allowed = check_position(center_x, center_y)
        if moving:
            player_x, player_y = move_player(player_x, player_y)
            if not red_dead and not red.in_box:
                red_x, red_y, red_direction = red.move_red()
            else:
                red_x, red_y, red_direction = red.move_yellow()
            if not green_dead and not green.in_box:
                green_x, green_y, green_direction = green.move_green()
            else:
                green_x, green_y, green_direction = green.move_yellow()
            if not blue_dead and not blue.in_box:
                blue_x, blue_y, blue_direction = blue.move_blue()
            else:
                blue_x, blue_y, blue_direction = blue.move_yellow()
            yellow_x, yellow_y, yellow_direction = yellow.move_yellow()
        score, powerup, power_counter, eaten_ghost = check_collisions(
            score, powerup,
            power_counter, eaten_ghost)

        if not powerup:
            if (player_circle.colliderect(
                red.rect) and not red.dead) or \
                    (player_circle.colliderect(
                        blue.rect) and not blue.dead) or \
                    (player_circle.colliderect(green.rect) and not green.dead) or \
                    (player_circle.colliderect(yellow.rect) and not yellow.dead):
                if lives > 0:
                    lives -= 1
                    startup_counter = 0
                    powerup = False
                    power_counter = 0
                    player_x = 450
                    player_y = 663
                    direction = 0
                    direction_command = 0
                    red_x = 56
                    red_y = 58
                    red_direction = 0
                    blue_x = 440
                    blue_y = 388
                    blue_direction = 2
                    green_x = 440
                    green_y = 438
                    green_direction = 2
                    yellow_x = 440
                    yellow_y = 438
                    yellow_direction = 2
                    eaten_ghost = [False, False,
                                   False, False]
                    red_dead = False
                    blue_dead = False
                    yellow_dead = False
                    green_dead = False
                else:
                    game_over = True
                    moving = False
                    startup_counter = 0
        if powerup and player_circle.colliderect(red.rect) and\
                eaten_ghost[0] and not red.dead:
            if lives > 0:
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                red_x = 56
                red_y = 58
                red_direction = 0
                blue_x = 440
                blue_y = 388
                blue_direction = 2
                green_x = 440
                green_y = 438
                green_direction = 2
                yellow_x = 440
                yellow_y = 438
                yellow_direction = 2
                eaten_ghost = [False, False,
                               False, False]
                red_dead = False
                blue_dead = False
                yellow_dead = False
                green_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
        if powerup and player_circle.colliderect(blue.rect) and\
                eaten_ghost[1] and not blue.dead:
            if lives > 0:
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                red_x = 56
                red_y = 58
                red_direction = 0
                blue_x = 440
                blue_y = 388
                blue_direction = 2
                green_x = 440
                green_y = 438
                green_direction = 2
                yellow_x = 440
                yellow_y = 438
                yellow_direction = 2
                eaten_ghost = [False, False,
                               False, False]
                red_dead = False
                blue_dead = False
                yellow_dead = False
                green_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
        if powerup and player_circle.colliderect(green.rect) and\
                eaten_ghost[2] and not green.dead:
            if lives > 0:
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                red_x = 56
                red_y = 58
                red_direction = 0
                blue_x = 440
                blue_y = 388
                blue_direction = 2
                green_x = 440
                green_y = 438
                green_direction = 2
                yellow_x = 440
                yellow_y = 438
                yellow_direction = 2
                eaten_ghost = [False, False,
                               False, False]
                red_dead = False
                blue_dead = False
                yellow_dead = False
                green_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
        if powerup and player_circle.colliderect(yellow.rect) and\
                eaten_ghost[3] and not yellow.dead:
            if lives > 0:
                powerup = False
                power_counter = 0
                lives -= 1
                startup_counter = 0
                player_x = 450
                player_y = 663
                direction = 0
                direction_command = 0
                red_x = 56
                red_y = 58
                red_direction = 0
                blue_x = 440
                blue_y = 388
                blue_direction = 2
                green_x = 440
                green_y = 438
                green_direction = 2
                yellow_x = 440
                yellow_y = 438
                yellow_direction = 2
                eaten_ghost = [False, False,
                               False, False]
                red_dead = False
                blue_dead = False
                yellow_dead = False
                green_dead = False
            else:
                game_over = True
                moving = False
                startup_counter = 0
        if powerup and player_circle.colliderect(red.rect) and not\
                red.dead and not eaten_ghost[0]:
            red_dead = True
            eaten_ghost[0] = True
            score += (2 ** eaten_ghost.count(True)) * 100
        if powerup and player_circle.colliderect(blue.rect) and not\
                blue.dead and not eaten_ghost[1]:
            blue_dead = True
            eaten_ghost[1] = True
            score += (2 ** eaten_ghost.count(True)) * 100
        if powerup and player_circle.colliderect(green.rect) and not\
                green.dead and not eaten_ghost[2]:
            green_dead = True
            eaten_ghost[2] = True
            score += (2 ** eaten_ghost.count(True)) * 100
        if powerup and player_circle.colliderect(yellow.rect) and not\
                yellow.dead and not eaten_ghost[3]:
            yellow_dead = True
            eaten_ghost[3] = True
            score += (2 ** eaten_ghost.count(True)) * 100

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    direction_command = 0
                if event.key == pygame.K_LEFT:
                    direction_command = 1
                if event.key == pygame.K_UP:
                    direction_command = 2
                if event.key == pygame.K_DOWN:
                    direction_command = 3
                if event.key == pygame.K_SPACE and\
                        (game_over or game_won):
                    powerup = False
                    power_counter = 0
                    lives -= 1
                    startup_counter = 0
                    player_x = 450
                    player_y = 663
                    direction = 0
                    direction_command = 0
                    red_x = 56
                    red_y = 58
                    red_direction = 0
                    blue_x = 440
                    blue_y = 388
                    blue_direction = 2
                    green_x = 440
                    green_y = 438
                    green_direction = 2
                    yellow_x = 440
                    yellow_y = 438
                    yellow_direction = 2
                    eaten_ghost = [False, False,
                                   False, False]
                    red_dead = False
                    blue_dead = False
                    yellow_dead = False
                    green_dead = False
                    score = 0
                    lives = 3
                    level = copy.deepcopy(map)
                    game_over = False
                    game_won = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT and\
                        direction_command == 0:
                    direction_command = direction
                if event.key == pygame.K_LEFT and\
                        direction_command == 1:
                    direction_command = direction
                if event.key == pygame.K_UP and\
                        direction_command == 2:
                    direction_command = direction
                if event.key == pygame.K_DOWN and\
                        direction_command == 3:
                    direction_command = direction

        if direction_command == 0 and turns_allowed[0]:
            direction = 0
        if direction_command == 1 and turns_allowed[1]:
            direction = 1
        if direction_command == 2 and turns_allowed[2]:
            direction = 2
        if direction_command == 3 and turns_allowed[3]:
            direction = 3

        if player_x > 900:
            player_x = -47
        elif player_x < -50:
            player_x = 897

        if red.in_box and red_dead:
            red_dead = False
        if blue.in_box and blue_dead:
            blue_dead = False
        if green.in_box and green_dead:
            green_dead = False
        if yellow.in_box and yellow_dead:
            yellow_dead = False

        pygame.display.flip()
    pygame.quit()
