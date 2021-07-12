import shelve
import pygame
import time
import random

high_score = 0

d = shelve.open('High_Score.txt')
d['High_Score'] = high_score
d.close()

pygame.init()

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

dis_width = 1080
dis_height = 900

dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Snake Game by Edureka')

clock = pygame.time.Clock()

snake_block = 10
snake_speed = 15

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)


def Your_score(score):
    value = score_font.render("Your Score: " + str(score), True, yellow)
    dis.blit(value, [0, 0])


def Your_highscore(score):
    value = score_font.render("High Score: " + str(score), True, red)
    dis.blit(value, [0, 50])


def snake_1(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def snake_2(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(dis, black, [x[0], x[1], snake_block, snake_block])


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def set_score(high_score, score):
    # make function called set_scores(high_score, score)
    Your_score(score)
    Your_highscore(high_score)


def gameLoop():
    global high_score
    game_over = False
    game_close = False

    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    x2 = dis_width / 2
    y2 = dis_width / 2

    x2_change = 0
    y2_change = 0

    snake_List = []
    Length_of_snake = 1

    foodx = round(random.randrange(0, dis_width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, dis_height - snake_block) / 10.0) * 10.0

    while not game_over:

        if Length_of_snake - 1 > high_score:
            high_score = Length_of_snake - 1
            pygame.display.update()
        while game_close == True:
            dis.fill(blue)
            message("You Lost! Press C-Play Again or Q-Quit", red)
            set_score(high_score, Length_of_snake - 1)
            # Your_score(Length_of_snake - 1)
            # Your_highscore(high_score)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:

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

        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0 or x1 >= dis_width or x2 < 0 or y1 >= dis_height or y2 < 0:
            game_close = True
        x1 += x1_change
        y1 += y1_change
        x2 += x2_change
        y2 += y2_change
        dis.fill(blue)
        pygame.draw.rect(dis, green, [foodx, foody, snake_block, snake_block])
        snake_Head1 = []
        snake_Head2 = []
        snake_Head1.append(x1)
        snake_Head1.append(y1)
        snake_Head2.append(x2)
        snake_Head2.append(y2)
        snake_List.append(snake_Head1)
        snake_List.append(snake_Head2)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        for x in snake_List[:-1]:
            if x == snake_Head1 or x == snake_Head2:
                game_close = False

        snake_1(snake_block, snake_List)
        set_score(high_score, Length_of_snake - 1)
        # Your_score(Length_of_snake - 1)
        # Your_highscore(high_score)
        snake_2(snake_block, snake_List)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(
                0, dis_width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(
                0, dis_height - snake_block) / 10.0) * 10.0
            Length_of_snake += 1

        clock.tick(snake_speed)

    pygame.quit()
    quit()


gameLoop()
