import random

import pygame
from pygame import Color

from ball import Ball
from brick import Brick
from game_object import GameObject
from score_keeper import ScoreKeeper
from paddle import Paddle


class GameController(GameObject):
    def __init__(self, screen: pygame.Surface):
        super().__init__(screen)
        self._falling_bricks: list[Brick] = None
        self._paddle: Paddle = None
        self._ball: Ball = None
        self._bricks: list[Brick] = None
        self._score_keeper: ScoreKeeper = None
        self._score_msg = ""
        self._score_font = pygame.font.Font('font/Pixeltype.ttf', 50)

        pygame.mixer.music.load('sounds/song.mp3')
        pygame.mixer.music.play(-1)
        self._hit_brick_sound = pygame.mixer.Sound("sounds/hit1.mp3")
        self._hit_wall_sound = pygame.mixer.Sound("sounds/hit2.mp3")

        self._load_game()

    @staticmethod
    def _random_color_generator() -> Color:
        # TODO:
        #  Fix too dark color
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return Color(r, g, b)

    def _load_game(self, restart_score: bool = True) -> None:
        self._paddle = Paddle(self._screen)
        self._ball = Ball(self._screen)
        self._bricks = []
        self._falling_bricks = []
        if restart_score:
            self._score_keeper = ScoreKeeper()

        BRICK_WIDTH = 150 / 2
        BRICK_HEIGHT = 25
        BRICK_X_OFFSET = 5
        BRICK_Y_OFFSET = 40
        BRICK_X_DISTANCE = 80
        BRICK_Y_DISTANCE = 30
        for y in range(11):
            row_color = self._random_color_generator()
            for x in range(16):
                self._bricks.append(Brick(x * BRICK_X_DISTANCE + BRICK_X_OFFSET, y * BRICK_Y_DISTANCE + BRICK_Y_OFFSET,
                                          BRICK_WIDTH, BRICK_HEIGHT, self._screen, row_color))

    def update(self, delta_time: float) -> None:
        self._paddle.x_vel = 0
        keys = pygame.key.get_pressed()

        self._score_msg = f'Score: {self._score_keeper.get_score()}'

        for i, falling_brick in enumerate(self._falling_bricks):
            falling_brick.update(delta_time)
            if falling_brick.y + falling_brick.height > self._screen.height:
                self._falling_bricks.pop(i)

        if self._ball.is_down():
            self._score_msg += "   press R to restart"
            if keys[pygame.K_r]:
                self._load_game()
            return

        if keys[pygame.K_a]:
            self._paddle.x_vel = -1
        if keys[pygame.K_d]:
            self._paddle.x_vel = 1

        if self._ball.collide_brick_update(self._paddle):
            self._score_keeper.hit_puddle()
            pygame.mixer.Sound.play(self._hit_wall_sound)

        self._paddle.update(delta_time)
        self._ball.update(delta_time)

        for i, rect in enumerate(self._bricks):
            if self._ball.collide_brick_update(rect):
                self._score_keeper.break_brick()
                self._bricks.pop(i)
                pygame.mixer.Sound.play(self._hit_brick_sound)

                # Split brick into small bricks
                SPLITS = 2
                FORCE_SCALAR = 0.03
                for x in range(2 ** SPLITS):
                    for y in range(2 ** SPLITS):
                        new_width = rect.width / (2 ** SPLITS)
                        new_height = rect.height / (2 ** SPLITS)
                        b = Brick(rect.x + new_width * x, rect.y + new_height * y, new_width, new_height, self._screen,
                                  rect.color)

                        # TODO: use vector
                        v = (b.x + b.width) - self._ball._x, (b.y + b.height) - self._ball._y
                        magnitude = (v[0] ** 2 + v[1] ** 2) ** 0.5

                        b.add_force((v[0] / magnitude) * FORCE_SCALAR, (v[1] / magnitude) * FORCE_SCALAR)
                        self._falling_bricks.append(b)

        if len(self._bricks) == 0:
            self._load_game(restart_score=False)

    def draw(self):
        # TODO: remove this function (make update function)
        score_surf = self._score_font.render(self._score_msg, False, (64, 64, 64))
        score_rect = score_surf.get_rect(center=(self._screen.width / 2, self._screen.height - 200))
        self._screen.blit(score_surf, score_rect)

        for falling_brick in self._falling_bricks:
            falling_brick.draw()

        self._paddle.draw()
        for brick in self._bricks:
            brick.draw()
        self._ball.draw()
