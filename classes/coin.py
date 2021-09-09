import pygame
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

    def update(self, pos_x, pos_y):
        current_time = round(pygame.time.get_ticks() / 60)
        spriteIndex = current_time % len(self.sprites)
        self.image = self.sprites[spriteIndex]

        offset = 0
        # can this be done somewhere else?
        self.rect.topleft = (pos_x - offset,
                             pos_y - offset)
