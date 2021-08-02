import pygame
import sys
from pathlib import Path

base_path = Path(__file__).parent
clock = pygame.time.Clock()

coin_images = [
    '../Images/coin0.png',
    '../Images/coin1.png',
    '../Images/coin2.png',
    '../Images/coin3.png',
    '../Images/coin4.png',
    '../Images/coin5.png',
    '../Images/coin6.png',
]


class Coin(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        for image in coin_images:
            self.sprites.append(pygame.image.load(
                (base_path / image).resolve()))

        self.image = self.sprites[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos_x, pos_y)

    def update(self):
        current_time = round(pygame.time.get_ticks() / 60)
        spriteIndex = current_time % len(self.sprites)
        self.image = self.sprites[spriteIndex]


# General setup
pygame.init()

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
    moving_sprites.update()
    pygame.display.flip()
    clock.tick(15)
