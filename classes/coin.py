import pygame
import sys


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load(
            '/Users/ctechmbp20b/Sites/Snake/Images/coin0.png'))
        self.sprites.append(pygame.image.load(
            '/Users/ctechmbp20b/Sites/Snake/Images/coin1.png'))
        self.sprites.append(pygame.image.load(
            '/Users/ctechmbp20b/Sites/Snake/Images/coin2.png'))
        self.sprites.append(pygame.image.load(
            '/Users/ctechmbp20b/Sites/Snake/Images/coin3.png'))
        self.sprites.append(pygame.image.load(
            '/Users/ctechmbp20b/Sites/Snake/Images/coin4.png'))
        self.sprites.append(pygame.image.load(
            '/Users/ctechmbp20b/Sites/Snake/Images/coin5.png'))
        self.sprites.append(pygame.image.load(
            '/Users/ctechmbp20b/Sites/Snake/Images/coin6.png'))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)


def coin(self):
    self.coin_animation = True


def update(self, speed):
    if self.coin_animation == True:
        self.current_sprite += speed
        if int(self.current_sprite) >= len(self.sprites):
            self.current_sprite = 0
            self.coin_animation = False

        self.image = self.sprites[int(self.current_sprite)]


# General setup
pygame.init()
clock = pygame.time.Clock()

# Game Screen
screen_width = 400
screen_height = 400
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Sprite Animation")

# Creating the sprites and groups
moving_sprites = pygame.sprite.Group()
coin = Coin(150, 150)
moving_sprites.add(coin)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # Drawing
    screen.fill((0, 0, 0))
    moving_sprites.draw(screen)
    # moving_sprites.update(0.25)
    pygame.display.flip()
    clock.tick(60)
