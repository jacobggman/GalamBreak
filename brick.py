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
        # TODO: use vector math
        # TODO: move physic to game object
        # Velocity
        self.vx = 0
        self.vy = 0

        # Acceleration
        self.ax = 0
        self.ay = 0

        # Mass
        self.mass = 1

        # Forces
        self.forces = []

        self.gravity = -0.001

    def draw(self):
        pygame.draw.rect(
            self._screen, self.color, (self.x, self.y, self.width, self.height))

        pygame.draw.rect(
            self._screen, self.color - self.OUTLINE_COLOR_DIFF, (self.x, self.y, self.width, self.height), self.OUTLINE_WEIGHT)

    def add_force(self, fx: float, fy: float) -> None:
        """Add a force vector (fx, fy) to the object"""
        self.forces.append((fx, fy))

    def update(self, delta_time: float) -> None:
        # Reset acceleration
        self.ax = 0
        self.ay = 0

        # Add gravity
        self.ay -= self.gravity

        # Sum up all forces and convert to acceleration (F = ma)
        for fx, fy in self.forces:
            self.ax += fx / self.mass
            self.ay += fy / self.mass

        # Clear forces for next frame
        self.forces.clear()

        # Update velocity (v = v0 + at)
        self.vx += self.ax * delta_time
        self.vy += self.ay * delta_time

        # Update position (x = x0 + vt)
        self.x += self.vx * delta_time
        self.y += self.vy * delta_time
