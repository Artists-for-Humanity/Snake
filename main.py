import pygame
import random
from pathlib import Path
import sqlite3
import platform

from pygame import draw
from classes.snake import Snake
from classes.apple import Apple
from classes.coin import Coin

base_path = Path(__file__).parent
my_system = platform.uname()

pygame.init()
clock = pygame.time.Clock()

#
# Database
db = sqlite3.connect('highscore.db')
cursor = db.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS highscore(
        id INTEGER PRIMARY KEY,
        name TEXT,
        score INTEGER
    )
''')
db.commit()

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
fullscreen = my_system.node == 'raspberrypi'
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
high_score = ('AAA', 0)
snake_block = 20
snake_speed = 15
game_screen = 'Menu'  # 'Menu' 'Game' 'GameOver'
prev_game_screen = ''

#
# Game pad
gamepad = False
print(f"Joystics Count: {pygame.joystick.get_count()}")
if (pygame.joystick.get_count() != 0):
    gamepad = pygame.joystick.Joystick(0)
    print(gamepad.get_name())
    gamepad.init()
else:
    print("No gamepad detected")

#
# Global Functions
def draw_score(score):
    value = font_style.render(f"Your score: {str(score)}".upper(), True, green)
    dis.blit(value, [bounds[3], 8])

def draw_highscore(score):
    value = font_style.render(f"Highscore: {score[0]} - {str(score[1])}".upper(), True, green)
    dis.blit(value, [dis_width / 2, 8])

def get_random_position_x():
    return round(random.randrange(bounds[3], bounds[1] - snake_block) / snake_block) * snake_block

def get_random_position_y():
    return round(random.randrange(bounds[0], bounds[2] - snake_block) / snake_block) * snake_block

def draw_scores(high_score, score):
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

def update_prev_screen():
    global prev_game_screen
    global game_screen
    if (prev_game_screen is not game_screen):
        prev_game_screen = game_screen
        return True
    return False


# Global Variables
snake = Snake(pygame, dis, snake_block, green)
apple1 = Apple(pygame, dis, snake_block, background_color, get_random_position_x(), get_random_position_y())
apple2 = Apple(pygame, dis, snake_block, background_color, get_random_position_x(), get_random_position_y())
apple3 = Apple(pygame, dis, snake_block, background_color, get_random_position_x(), get_random_position_y())

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

initials = []
active_letter = 0
letters = [
    'A',
    'B',
    'C',
    'D',
    'E',
    'F',
    'G',
    'H',
    'I',
    'J',
    'K',
    'L',
    'M',
    'N',
    'O',
    'P',
    'Q',
    'R',
    'S',
    'T',
    'U',
    'V',
    'W',
    'X',
    'Y',
    'Z',
]

#
# Game Loop
def gameLoop():
    global active_letter
    global initials
    global cursor
    global game_screen
    global prev_game_screen
    global snake
    global apple1
    global apple2
    global apple3
    global coin_sprite1
    global coin_sprite2
    global coin_sprite3
    global coin1
    global coin2
    global coin3

    high_scores = cursor.execute('''
        SELECT name, score
        FROM highscore
        ORDER BY score DESC
        LIMIT 3
    ''').fetchall()

    if (len(high_scores) > 0):
        high_score = high_scores[0]
    else:
        high_score = ('AAA', 0)

    exit = False

    while not exit:
        #
        # Menu
        while game_screen == 'Menu':
            draw_background()
            title = menu_font_style_big.render("Snake", True, white)
            dis.blit(title, title.get_rect(center=(dis_width/2, dis_height/2)))
            dis.blit(play_text_image, play_text_image.get_rect(center=(dis_width/2, dis_height/2 + 160)))

            high_score_text = menu_font_style_text.render(f"High Score: {high_score[0]} - {str(high_score[1])}", True, white)
            dis.blit(high_score_text, high_score_text.get_rect(center=(dis_width/2, 80)))

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
                if (
                    ((event.type == pygame.JOYBUTTONDOWN) and (event.button == 0)) or
                    ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_c))
                ):
                    game_screen = 'Game'
                    gameLoop()

            update_prev_screen()
            pygame.display.update()

        #
        # Gameover
        while game_screen == 'GameOver':
            draw_global()
            mesg = menu_font_style_big.render("Game over!", True, white)
            dis.blit(mesg, mesg.get_rect(center=(dis_width/2, dis_height/2)))

            name_header = menu_font_style_text.render("Enter Your Initials", True, white)
            dis.blit(name_header, name_header.get_rect(center=(dis_width/2, dis_height/2 + 100)))

            background_text = "".join((initials + ['A', 'A', 'A'])[:3])
            initial_text_position = menu_font_style_text.render(background_text, True, black)
            dis.blit(initial_text_position, initial_text_position.get_rect(center=(dis_width/2, dis_height/2 + 100 + 75)))
            
            initials_rendered = "".join(initials + [letters[active_letter]])
            initial_text = menu_font_style_text.render(initials_rendered, True, white)
            dis.blit(initial_text, initial_text_position.get_rect(center=(dis_width/2, dis_height/2 + 100 + 75)))

            for event in pygame.event.get():
                if ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_UP)):
                    if (active_letter < len(letters) - 1):
                        active_letter += 1
                    else:
                        active_letter = 0
                if ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_DOWN)):
                    if (active_letter > 0):
                        active_letter -= 1
                    else:
                        active_letter = len(letters) - 1
                    
                if (
                    ((event.type == pygame.JOYBUTTONDOWN) and (event.button == 0)) or
                    ((event.type == pygame.KEYDOWN) and (event.key == pygame.K_c))
                ):
                    initials.append(letters[active_letter])
                    
                    if len(initials) == 3:
                        cursor = db.cursor()
                        cursor.execute('''INSERT INTO highscore(name, score)
                                        VALUES(?,?)''', ("".join(initials), snake.Length - 1))
                        db.commit()

                        game_screen = 'Menu'
                        gameLoop()
                        

            update_prev_screen()
            pygame.display.update()

        #
        # Game
        if game_screen == 'Game':
            if game_screen is not prev_game_screen:
                initials = []
                active_letter = 0
                snake.resetPosition(
                    get_random_position_x(),
                    get_random_position_y()
                )
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                if event.type == pygame.JOYAXISMOTION:
                    axis = event.axis
                    value = round(event.value)
                    # print(f"Axis: {str(axis)}, Value: {str(value)}")

                    if (axis == 0) and (value == 1):
                        snake.moveDown()
                        print("A")
                    if (axis == 0) and (value == -1):
                        snake.moveLeft()
                        print("B")
                    if (axis == 1) and (value == 1):
                        snake.moveUp()
                        print("C")
                    if (axis == 1) and (value == -1):
                        snake.moveRight()
                        print("D")
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        snake.moveLeft()
                    elif event.key == pygame.K_RIGHT:
                        snake.moveRight()
                    elif event.key == pygame.K_UP:
                        snake.moveUp()
                    elif event.key == pygame.K_DOWN:
                        snake.moveDown()

            draw_global()
            draw_scores(high_score, snake.Length - 1)

            snake.update()
            snake.draw()
            apple1.draw()
            apple2.draw()
            apple3.draw()

            coin_sprite1.draw(dis)
            coin_sprite1.update(apple1.x, apple1.y)
            coin_sprite2.draw(dis)
            coin_sprite2.update(apple2.x, apple2.y)
            coin_sprite3.draw(dis)
            coin_sprite3.update(apple3.x, apple3.y)

            if snake.isOutOfBounds(bounds) or snake.isOverlappingItself():
                game_screen = 'GameOver'
                gameLoop()

            if (snake.isOver(apple1.x, apple1.y)):
                apple1.changePosition(
                    get_random_position_x(),
                    get_random_position_y()
                )
                snake.increaseLength()

            if (snake.isOver(apple2.x, apple2.y)):
                apple2.changePosition(
                    get_random_position_x(),
                    get_random_position_y()
                )
                snake.increaseLength()

            if (snake.isOver(apple3.x, apple3.y)):
                apple3.changePosition(
                    get_random_position_x(),
                    get_random_position_y()
                )
                snake.increaseLength()

            update_prev_screen()

        clock.tick(snake_speed)
        pygame.display.update()

    pygame.quit()
    quit()


gameLoop()
