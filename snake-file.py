import shelve
import pygame
from pygame import mixer
import time
import random

high_score = 0
high_score2 = 0
d = shelve.open('High_Score.txt')
d['High_Score'] = high_score
d.close()

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = '#222222'
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 1080
dis_height = 900

dis = pygame.display.set_mode((dis_width, dis_height), pygame.RESIZABLE)
pygame.display.set_caption('Snake Game by Edureka')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15
# snake_speed_1 = 15
# snake_speed_2 = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

game_screen = 'Menu'  # 'Game' 'GameOver' 'Menu'

# Background Music
mixer.music.load(
    'Gothic Storm Music- Red Harvest (2020 Epic Menacing Sinister Gothic Orchestral).wav')
mixer.music.play(-1)


def Your_score(score):
    value = score_font.render("Player 1: " + str(score), True, yellow)
    dis.blit(value, [0, 0])


def Your_highscore(score):
    value = score_font.render("Player 1: " + str(score), True, red)
    dis.blit(value, [0, 50])


def Your_score_2(score):
    value = score_font.render("Player 2: " + str(score), True, yellow)
    dis.blit(value, [885, 0])


def Your_highscore_2(score):
    value = score_font.render("Player 2: " + str(score), True, red)
    dis.blit(value, [885, 50])


def draw_snake(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, green, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def set_score(high_score, score):
    Your_score(score)
    Your_highscore(high_score)


def set_score2(high_score, score):
    Your_score_2(score)
    Your_highscore_2(high_score)


def check_if_over_food(x, y, foodx, foody, Length_of_snake, snake_speed):
    if x == foodx and y == foody:
        foodx = round(random.randrange(
            0, dis_width - snake_block) / 10.0) * 10.0
        foody = round(random.randrange(
            0, dis_height - snake_block) / 10.0) * 10.0
        Length_of_snake += 1
        snake_speed += 20
    return x, y, foodx, foody, Length_of_snake, snake_speed


def gameLoop():
    global high_score
    global high_score2
    global snake_speed
    global snake_speed_1
    global snake_speed_2
    global game_screen
    img = pygame.image.load('Images/Menu.png')

    game_over = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    x2 = dis_width / 2
    y2 = dis_width / 2

    x2_change = 0
    y2_change = 0

    snake_List1 = []
    snake_List2 = []

    Length_of_snake1 = 1
    Length_of_snake2 = 1

    snake_speed = 15

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    foodx2 = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody2 = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    foodx3 = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody3 = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:
        if Length_of_snake1 - 1 > high_score:
            high_score = Length_of_snake1 - 1
            pygame.display.update()
        if Length_of_snake2 - 1 > high_score2:
            high_score2 = Length_of_snake2 - 1
            pygame.display.update()
        while game_screen == 'Menu':
            dis.fill(black)
            img_size = 600
            dis.blit(img, ((dis_width/2) - img_size/2,
                     (dis_height/2) - img_size/2, img_size, img_size))
            # message(
            # "Welcome to the Creative Tech Snake Game! Press C to play or Q to quit", white)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_screen = 'Game'
                    if event.key == pygame.K_c:
                        game_screen = 'Game'
                        gameLoop()

        while game_screen == 'GameOver':
            dis.fill(black)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            set_score(high_score, Length_of_snake1 - 1)
            set_score2(high_score2, Length_of_snake2 - 1)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_screen = 'Game'
                    if event.key == pygame.K_c:
                        game_screen = 'Game'
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x2_change = -snake_block
                    y2_change = 0
                elif event.key == pygame.K_d:
                    x2_change = snake_block
                    y2_change = 0
                elif event.key == pygame.K_w:
                    y2_change = -snake_block
                    x2_change = 0
                elif event.key == pygame.K_s:
                    y2_change = snake_block
                    x2_change = 0

        snake_offscreen1 = x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0
        snake_offscreen2 = x2 >= dis_width or x2 < 0 or y2 >= dis_height or y2 < 0

        if snake_offscreen1 or snake_offscreen2:
            game_screen = 'GameOver'

        x1 += x1_change
        y1 += y1_change
        x2 += x2_change
        y2 += y2_change
        dis.fill(black)
        pygame.draw.rect(dis, blue, [foodx, foody,  snake_block, snake_block])
        pygame.draw.rect(
            dis, red, [foodx2, foody2,  snake_block, snake_block])
        pygame.draw.rect(
            dis, yellow, [foodx3, foody3,  snake_block, snake_block])

        # build_snake(snake_Head1, snake_List1, x1, y1)
        snake_Head1 = []
        snake_Head1.append(x1)
        snake_Head1.append(y1)
        snake_List1.append(snake_Head1)

        # build_snake(snake_Head2, snake_List2, x2, y2)
        snake_Head2 = []
        snake_Head2.append(x2)
        snake_Head2.append(y2)
        snake_List2.append(snake_Head2)

        if len(snake_List1) > Length_of_snake1:
            del snake_List1[0]
        if len(snake_List2) > Length_of_snake2:
            del snake_List2[0]

        for x in snake_List1[:-1]:
            if x == snake_Head1:
                game_screen = 'GameOver'
        for x in snake_List2[:-1]:
            if x == snake_Head2:
                game_screen = 'GameOver'

        draw_snake(snake_block, snake_List1)
        draw_snake(snake_block, snake_List2)
        set_score(high_score, Length_of_snake1 - 1)
        set_score2(high_score2, Length_of_snake2 - 1)

        pygame.display.update()

        x1, y1, foodx, foody, Length_of_snake1, snake_speed = check_if_over_food(
            x1, y1, foodx, foody, Length_of_snake1, snake_speed)
        x1, y1, foodx2, foody2, Length_of_snake1, snake_speed = check_if_over_food(
            x1, y1, foodx2, foody2, Length_of_snake1, snake_speed)
        x1, y1, foodx3, foody3, Length_of_snake1, snake_speed = check_if_over_food(
            x1, y1, foodx3, foody3, Length_of_snake1, snake_speed)

        x2, y2, foodx, foody, Length_of_snake2, snake_speed = check_if_over_food(
            x2, y2, foodx, foody, Length_of_snake2, snake_speed)
        x2, y2, foodx2, foody2, Length_of_snake2, snake_speed = check_if_over_food(
            x2, y2, foodx2, foody2, Length_of_snake2, snake_speed)
        x2, y2, foodx3, foody3, Length_of_snake2, snake_speed = check_if_over_food(
            x2, y2, foodx3, foody3, Length_of_snake2, snake_speed)

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
