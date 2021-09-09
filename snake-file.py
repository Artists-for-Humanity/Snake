import pygame
import random
from classes.snake import Snake
from classes.apple import Apple
from classes.coin import Coin

high_score = 0
high_score2 = 0

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

font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

game_screen = 'Menu'  # 'Game' 'GameOver' 'Menu'

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


def get_random_position(size):
    return round(random.randrange(0, size - snake_block) / 10.0) * 10.0


def message(msg, color):
    mesg = font_style.render(msg, True, color)
    dis.blit(mesg, [dis_width / 6, dis_height / 3])


def set_score(high_score, score):
    Your_score(score)
    Your_highscore(high_score)


def set_score2(high_score, score):
    Your_score_2(score)
    Your_highscore_2(high_score)


snake1 = Snake(pygame, dis, snake_block)
snake2 = Snake(pygame, dis, snake_block)
apple1 = Apple(pygame, dis, snake_block, black, get_random_position(
    dis_width), get_random_position(dis_height))
apple2 = Apple(pygame, dis, snake_block, black, get_random_position(
    dis_width), get_random_position(dis_height))
apple3 = Apple(pygame, dis, snake_block, black, get_random_position(
    dis_width), get_random_position(dis_height))


def gameLoop():
    global high_score
    global high_score2
    global game_screen
    global snake1
    global snake2
    global apple1
    global apple2
    global apple3
    img = pygame.image.load('Images/Menu.png')

    # Loading the sprite
    coin_sprite1 = pygame.sprite.Group()
    coin1 = Coin(150, 150)
    coin_sprite1.add(coin1)

    coin_sprite2 = pygame.sprite.Group()
    coin2 = Coin(150, 150)
    coin_sprite2.add(coin2)

    coin_sprite3 = pygame.sprite.Group()
    coin3 = Coin(150, 150)
    coin_sprite3.add(coin3)

    snake1.resetPosition(
        get_random_position(dis_width), get_random_position(dis_height)
    )
    snake2.resetPosition(get_random_position(dis_width),
                         get_random_position(dis_height))

    game_over = False

    while not game_over:
        if snake1.Length - 1 > high_score:
            high_score = snake1.Length - 1
            pygame.display.update()

        while game_screen == 'Menu':
            dis.fill(black)
            img_size = 600
            dis.blit(img, ((dis_width/2) - img_size/2,
                     (dis_height/2) - img_size/2, img_size, img_size))
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
            set_score(high_score, snake1.Length - 1)
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
                    snake1.moveLeft()
                elif event.key == pygame.K_RIGHT:
                    snake1.moveRight()
                elif event.key == pygame.K_UP:
                    snake1.moveUp()
                elif event.key == pygame.K_DOWN:
                    snake1.moveDown()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    snake2.moveLeft()
                elif event.key == pygame.K_d:
                    snake2.moveRight()
                elif event.key == pygame.K_w:
                    snake2.moveUp()
                elif event.key == pygame.K_s:
                    snake2.moveDown()

        dis.fill(black)
        set_score(high_score, snake1.Length - 1)

        snake1.update()
        snake1.draw()
        snake2.update()
        snake2.draw()
        apple1.draw()
        apple2.draw()
        apple3.draw()

        if snake1.isOutOfBounds(dis_width, dis_height) or snake2.isOutOfBounds(dis_width, dis_height):
            game_screen = 'GameOver'

        if snake1.isOverlappingItself() or snake2.isOverlappingItself():
            game_screen = 'GameOver'

        food_pos_x = apple1.x
        food_pos_y = apple1.y
        food_pos_x_2 = apple2.x
        food_pos_y_2 = apple2.y
        food_pos_x_3 = apple3.x
        food_pos_y_3 = apple3.y

        coin_sprite1.draw(dis)
        coin_sprite1.update(food_pos_x, food_pos_y)
        coin_sprite2.draw(dis)
        coin_sprite2.update(food_pos_x_2, food_pos_y_2)
        coin_sprite3.draw(dis)
        coin_sprite3.update(food_pos_x_3, food_pos_y_3)

        if (snake1.isOver(apple1.x, apple1.y)):
            apple1.changePosition(get_random_position(
                dis_width), get_random_position(dis_height))
            snake1.increaseLength()

        if (snake1.isOver(apple2.x, apple2.y)):
            apple2.changePosition(get_random_position(
                dis_width), get_random_position(dis_height))
            snake1.increaseLength()

        if (snake1.isOver(apple3.x, apple3.y)):
            apple3.changePosition(get_random_position(
                dis_width), get_random_position(dis_height))
            snake1.increaseLength()

        if (snake2.isOver(apple1.x, apple1.y)):
            apple1.changePosition(get_random_position(
                dis_width), get_random_position(dis_height))
            snake2.increaseLength()

        if (snake2.isOver(apple2.x, apple2.y)):
            apple2.changePosition(get_random_position(
                dis_width), get_random_position(dis_height))
            snake2.increaseLength()

        if (snake2.isOver(apple3.x, apple3.y)):
            apple3.changePosition(get_random_position(
                dis_width), get_random_position(dis_height))
            snake2.increaseLength()

        clock.tick(15)
        pygame.display.update()

    pygame.quit()
    quit()


gameLoop()
