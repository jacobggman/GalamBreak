import pygame
from pygame import Color

from game_object import GameObject


class Brick(GameObject):
    FORCE_LOSE_SPEED = 1
    OUTLINE_WEIGHT = 5
    OUTLINE_COLOR_DIFF = Color(50, 50, 50)

    def __init__(self, x, y, width, height, screen, color):
        super().__init__(screen)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

    def draw(self):
        pygame.draw.rect(
            self._screen, self.color, (self.x, self.y, self.width, self.height))

        pygame.draw.rect(
            self._screen, self.color - self.OUTLINE_COLOR_DIFF, (self.x, self.y, self.width, self.height), self.OUTLINE_WEIGHT)
