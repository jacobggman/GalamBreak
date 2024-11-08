import pygame
from pygame import Color

from brick import Brick


class Paddle(Brick):
    DEFAULT_WIDTH = 150
    DEFAULT_HEIGHT = 25
    DEFAULT_MOVE_SPEED = 2

    def __init__(self, screen: pygame.Surface):
        x = (screen.width - self.DEFAULT_WIDTH) // 2
        y = screen.height - 50
        width = self.DEFAULT_WIDTH
        height = self.DEFAULT_HEIGHT
        super().__init__(x, y, width, height, screen, Color(255, 255, 255))
        self._move_speed = self.DEFAULT_MOVE_SPEED
        self.x_vel = 0

    def update(self, delta_time: float) -> None:
        self.x += self.x_vel * delta_time * self._move_speed
        self.x = min(self.x, self._screen.width - self.width)
        self.x = max(self.x, 0)
