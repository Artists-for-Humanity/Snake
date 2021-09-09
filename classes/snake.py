import pygame

class Snake():
    def __init__(self, pygame, dis, blockSize, color):
        self.pygame = pygame
        self.dis = dis
        self.blockSize = blockSize
        self.resetPosition(0, 0)
        self.color = color

    def draw(self):
        for x in self.List:
            self.pygame.draw.rect(
                self.dis,
                self.color,
                [x[0], x[1], self.blockSize, self.blockSize]
            )

    def resetPosition(self, x, y):
        self.Length = 1
        self.Head = []
        self.List = []
        self.LastPos = [x, y]
        self.Change = [0, 0]

    def moveUp(self):
        self.Change = [0, self.blockSize * -1]

    def moveDown(self):
        self.Change = [0, self.blockSize]

    def moveLeft(self):
        self.Change = [self.blockSize * -1, 0]

    def moveRight(self):
        self.Change = [self.blockSize, 0]

    def increaseLength(self):
        self.Length = self.Length + 1

    def update(self):
        self.Head = []
        self.Head.append(self.LastPos[0])
        self.Head.append(self.LastPos[1])
        self.List.append(self.Head)

        # Delete the last snake block if the length did not grow.
        if (len(self.List) > self.Length):
            del self.List[0]

        self.LastPos = [self.LastPos[0] + self.Change[0],
                        self.LastPos[1] + self.Change[1]]

    def isOver(self, x, y):
        return x == self.LastPos[0] and y == self.LastPos[1]

    def isOverlappingItself(self):
        for x in self.List[:-1]:
            if x == self.Head:
                return True
        return False

    def isOutOfBounds(self, bounds):
        return self.LastPos[0] >= bounds[1] or self.LastPos[0] < bounds[3] or self.LastPos[1] >= bounds[2] or self.LastPos[1] < bounds[0]
