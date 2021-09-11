import pygame
import random
from pathlib import Path

from pygame import draw
from classes.snake import Snake
from classes.apple import Apple
from classes.coin import Coin

base_path = Path(__file__).parent

pygame.init()
clock = pygame.time.Clock()

#
# Colors
black = (34, 34, 34)
gray = (90, 90, 90)
white = (255, 255, 255)
red = (213, 50, 80)
green = (151, 196, 5)
background_color = black

#
# Display variables
score_bar_height = 40
inset = 20
display = pygame.display.Info()
fullscreen = False
if fullscreen:
    dis_width = display.current_w #1080
    dis_height = display.current_h #900
    dis = pygame.display.set_mode((dis_width, dis_height), pygame.FULLSCREEN)
else:
    dis_width = 1200
    dis_height = 1200
    dis = pygame.display.set_mode((dis_width, dis_height), pygame.RESIZABLE)
bounds = [40, dis_width - inset, dis_height - inset, inset] # top, right, bottom, left
print(f"Width: {dis_width}, Height: {dis_height}")
pygame.mouse.set_visible(False)

#
# Font
font_style = pygame.font.Font(str((base_path / 'fonts/OCRAStd.ttf').resolve()), 25)
menu_font_style_big = pygame.font.Font(str((base_path / 'fonts/MonsterFriendFore.ttf').resolve()), 100)
menu_font_style_text = pygame.font.Font(str((base_path / 'fonts/MonsterFriendFore.ttf').resolve()), 25)

#
# Menu
snake_img = pygame.image.load('Images/Snake.png')
play_text_image = pygame.image.load('Images/Play-Text.png')

#
# Game variables
high_score = 0
snake_block = 20
snake_speed = 15
game_screen = 'Menu'  # 'Game' 'GameOver' 'Menu'

#
# Game pad
gamepad = False
print(f"Joystics Count: {pygame.joystick.get_count()}")
if (pygame.joystick.get_count() != 0):
    gamepad = pygame.joystick.Joystick(0)
    print(gamepad.get_name())
    gamepad.init()
    GAME_PAD_Y_AXIS = 2
    GAME_PAD_X_AXIS = 0
else:
    print("No gamepad detected")

#
# Global Functions
def draw_score(score):
    value = font_style.render(f"Your score: {str(score)}".upper(), True, green)
    dis.blit(value, [bounds[3], 8])

def draw_highscore(score):
    value = font_style.render(f"Highscore: {str(score)}".upper(), True, green)
    dis.blit(value, [dis_width / 2, 8])

def get_random_position_x():
    return round(random.randrange(bounds[3], bounds[1] - snake_block) / snake_block) * snake_block

def get_random_position_y():
    return round(random.randrange(bounds[0], bounds[2] - snake_block) / snake_block) * snake_block

def message(msg):
    mesg = font_style.render(msg.upper(), True, green)
    mesg_rect = mesg.get_rect(center=(dis_width/2, dis_height/2))
    dis.blit(mesg, mesg_rect)

def set_score(high_score, score):
    draw_score(score)
    draw_highscore(high_score)


def draw_background():
    dis.fill(background_color)

def draw_global():
    draw_background()

    border = 4
    offset = 2
    top = bounds[0] - border - offset
    right = bounds[1] + border + offset
    bottom = bounds[2] + border + offset
    left = bounds[3] - border - offset

    pygame.draw.rect(
        dis,
        green,
        [
            left,
            top,
            right - left,
            bottom - top
        ],
        border
    )


# Global Variables
snake1 = Snake(pygame, dis, snake_block, green)
apple1 = Apple(pygame, dis, snake_block, background_color, get_random_position_x(), get_random_position_y())
apple2 = Apple(pygame, dis, snake_block, background_color, get_random_position_x(), get_random_position_y())
apple3 = Apple(pygame, dis, snake_block, background_color, get_random_position_x(), get_random_position_y())

#
# Game Loop
def gameLoop():
    global high_score
    global game_screen
    global snake1
    global apple1
    global apple2
    global apple3

    # Loading the sprite
    coin_sprite1 = pygame.sprite.Group()
    coin1 = Coin()
    coin_sprite1.add(coin1)

    coin_sprite2 = pygame.sprite.Group()
    coin2 = Coin()
    coin_sprite2.add(coin2)

    coin_sprite3 = pygame.sprite.Group()
    coin3 = Coin()
    coin_sprite3.add(coin3)

    snake1.resetPosition(
        get_random_position_x(),
        get_random_position_y()
    )

    game_over = False

    while not game_over:
        if snake1.Length - 1 > high_score:
            high_score = snake1.Length - 1
            pygame.display.update()

        #
        # Menu
        while game_screen == 'Menu':
            draw_background()
            title = menu_font_style_big.render("Snake", True, white)
            dis.blit(title, title.get_rect(center=(dis_width/2, dis_height/2)))
            dis.blit(play_text_image, play_text_image.get_rect(center=(dis_width/2, dis_height/2 + 160)))

            credits = [
                menu_font_style_text.render("Created by:", True, gray),
                menu_font_style_text.render("Creative Technology Studio", True, gray),
                menu_font_style_text.render("Jeremiah Harris", True, gray),
                menu_font_style_text.render("JQ", True, gray)
            ]
            credits.reverse()
            for i, credit in enumerate(credits):
                dis.blit(credit, credit.get_rect(center=(dis_width/2, dis_height - 40 - (40 * i))))

            snake_img_scaled = pygame.transform.scale(snake_img, (256, 256))
            dis.blit(snake_img_scaled, snake_img_scaled.get_rect(center=(dis_width/2 + 128, dis_height/2 - 128 - 25)))

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_screen = 'Game'
                    if event.key == pygame.K_c:
                        game_screen = 'Game'
                        gameLoop()

            pygame.display.update()

        #
        # Gameover
        while game_screen == 'GameOver':
            draw_global()
            message("You Lost! Press C-Play Again or Q-Quit")
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
            # print(event)
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.JOYAXISMOTION:
                axis = event.axis
                value = round(event.value)
                # print(f"Axis: {str(axis)}, Value: {str(value)}")

                if (axis == GAME_PAD_X_AXIS):
                    if (value == 1):
                        snake1.moveRight()
                    if (value == -1):
                        snake1.moveUp()
                if (axis == GAME_PAD_Y_AXIS):
                    if (value == 1):
                        snake1.moveLeft()
                    if (value == -1):
                        snake1.moveDown()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    snake1.moveLeft()
                elif event.key == pygame.K_RIGHT:
                    snake1.moveRight()
                elif event.key == pygame.K_UP:
                    snake1.moveUp()
                elif event.key == pygame.K_DOWN:
                    snake1.moveDown()

        draw_global()
        set_score(high_score, snake1.Length - 1)

        snake1.update()
        snake1.draw()
        apple1.draw()
        apple2.draw()
        apple3.draw()

        coin_sprite1.draw(dis)
        coin_sprite1.update(apple1.x, apple1.y)
        coin_sprite2.draw(dis)
        coin_sprite2.update(apple2.x, apple2.y)
        coin_sprite3.draw(dis)
        coin_sprite3.update(apple3.x, apple3.y)

        if snake1.isOutOfBounds(bounds) or snake1.isOverlappingItself():
            game_screen = 'GameOver'
            pygame.display.update()

        if (snake1.isOver(apple1.x, apple1.y)):
            apple1.changePosition(
                get_random_position_x(),
                get_random_position_y()
            )
            snake1.increaseLength()

        if (snake1.isOver(apple2.x, apple2.y)):
            apple2.changePosition(
                get_random_position_x(),
                get_random_position_y()
            )
            snake1.increaseLength()

        if (snake1.isOver(apple3.x, apple3.y)):
            apple3.changePosition(
                get_random_position_x(),
                get_random_position_y()
            )
            snake1.increaseLength()

        clock.tick(snake_speed)
        pygame.display.update()

    pygame.quit()
    quit()


gameLoop()
