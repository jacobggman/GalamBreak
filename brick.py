import pygame

from game_object import GameObject


class Brick(GameObject):
    def __init__(self, x, y, width, height, screen, color):
        super().__init__(screen)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        pygame.draw.rect(
            self.screen, self.color, (self.x, self.y, self.width, self.height))
