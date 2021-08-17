import pygame


class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.Up_KEY, self.Down_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 480, 270
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.display =
