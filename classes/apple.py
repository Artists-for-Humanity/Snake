class Apple():
    def __init__(self, pygame, dis, blockSize, color, x, y):
        self.pygame = pygame
        self.dis = dis
        self.blockSize = blockSize
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        self.pygame.draw.rect(self.dis, self.color, [
            self.x, self.y,  self.blockSize, self.blockSize])

    def changePosition(self, x, y):
        self.x = x
        self.y = y
