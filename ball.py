import pygame

from game_object import GameObject
from brick import Brick


class Ball(GameObject):
    RADIUS = 7
    MAX_VEL = 1
    COLOR = "red"

    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self._x = (self._screen.width - self.RADIUS) // 2
        self._y = self._screen.height - 100
        self._radius = self.RADIUS
        self._x_vel = 0
        self._y_vel = self.MAX_VEL

    def draw(self) -> None:
        pygame.draw.circle(self._screen, self.COLOR, (self._x, self._y), self._radius)

    def update(self, delta_time: float) -> None:
        # TODO: add collide wall update
        hit_ceiling = self._y - self._radius <= 0
        if hit_ceiling:
            if self._y_vel < 0:
                self._y_vel *= -1

        hit_right_wall = self._x + self._radius >= self._screen.width
        if hit_right_wall:
            if self._x_vel > 0:
                self._x_vel *= -1

        hit_left_wall = self._x - self._radius <= 0
        if hit_left_wall:
            if self._x_vel < 0:
                self._x_vel *= -1

        self._x += self._x_vel * delta_time
        self._y += self._y_vel * delta_time

    def collide_brick_update(self, rect: Brick) -> bool:
        if self._intersects(rect):
            # Determine which side of the rectangle was hit
            circle_center_y = self._y
            rect_center_y = rect.y + rect.height / 2

            # Only reverse Y velocity if hitting from top or bottom
            if (circle_center_y < rect_center_y and self._y_vel > 0) or \
                    (circle_center_y > rect_center_y and self._y_vel < 0):
                self._y_vel *= -1

            # Calculate x velocity changes
            rect_center_x = rect.x + rect.width / 2
            difference_in_x = rect_center_x - self._x
            reduction_factor = (rect.width / 2) / self.MAX_VEL
            x_vel = difference_in_x / reduction_factor

            # Flip the direction: when difference_in_x is positive (ball is on left),
            # ball should move left, and vice versa
            self._x_vel = min(abs(x_vel), self.MAX_VEL) * (-1 if x_vel > 0 else 1)

            return True
        return False

    def is_down(self):
        return self._y - self._radius > self._screen.height

    def _intersects(self, rect: Brick) -> bool:
        # Get the center points of both objects
        circle_center_x = self._x
        circle_center_y = self._y

        # Find the closest point on the rectangle to the circle
        closest_x = max(rect.x, min(circle_center_x, rect.x + rect.width))
        closest_y = max(rect.y, min(circle_center_y, rect.y + rect.height))

        # Calculate the distance between the circle's center and the closest point
        distance_x = circle_center_x - closest_x
        distance_y = circle_center_y - closest_y

        # If the distance is less than the circle's radius, there is a collision
        distance_squared = (distance_x ** 2) + (distance_y ** 2)
        return distance_squared <= (self._radius ** 2)
