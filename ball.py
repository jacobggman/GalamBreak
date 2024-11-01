import pygame

from game_object import GameObject
from brick import Brick


class Ball(GameObject):
    RADIUS = 7
    MAX_VEL = 1

    def __init__(self, screen):
        super().__init__(screen)
        self.x = (self.screen.width - self.RADIUS) // 2
        self.y = self.screen.height - 100
        self.radius = self.RADIUS
        self.x_vel = 0
        self.y_vel = self.MAX_VEL

    def draw(self):
        pygame.draw.circle(self.screen, "red", (self.x, self.y), self.radius)

    def update(self, delta_time):
        if self.y - self.radius <= 0:
            if self.y_vel < 0:
                self.y_vel *= -1

        if self.x + self.radius >= self.screen.width:
            if self.x_vel > 0:
                self.x_vel *= -1
        if self.x - self.radius <= 0:
            if self.x_vel < 0:
                self.x_vel *= -1

        self.x += self.x_vel * delta_time
        self.y += self.y_vel * delta_time

    def intersects(self, rect: Brick):
        # Get the center points of both objects
        circle_center_x = self.x
        circle_center_y = self.y

        # Find the closest point on the rectangle to the circle
        closest_x = max(rect.x, min(circle_center_x, rect.x + rect.width))
        closest_y = max(rect.y, min(circle_center_y, rect.y + rect.height))

        # Calculate the distance between the circle's center and the closest point
        distance_x = circle_center_x - closest_x
        distance_y = circle_center_y - closest_y

        # If the distance is less than the circle's radius, there is a collision
        distance_squared = (distance_x ** 2) + (distance_y ** 2)
        return distance_squared <= (self.radius ** 2)

    def is_collide(self, rect: Brick):
        if self.intersects(rect):
            # Determine which side of the rectangle was hit
            circle_center_y = self.y
            rect_center_y = rect.y + rect.height / 2

            # Only reverse Y velocity if hitting from top or bottom
            if (circle_center_y < rect_center_y and self.y_vel > 0) or \
                    (circle_center_y > rect_center_y and self.y_vel < 0):
                self.y_vel *= -1

            # Calculate x velocity changes
            rect_center_x = rect.x + rect.width / 2
            difference_in_x = rect_center_x - self.x
            reduction_factor = (rect.width / 2) / self.MAX_VEL
            x_vel = difference_in_x / reduction_factor

            # Flip the direction: when difference_in_x is positive (ball is on left),
            # ball should move left, and vice versa
            self.x_vel = min(abs(x_vel), self.MAX_VEL) * (-1 if x_vel > 0 else 1)

            return True
        return False

    def is_down(self):
        return self.y - self.radius > self.screen.height
