import random

import pygame
from pygame import Color

from ball import Ball
from game_object import GameObject
from paddle import Paddle
from brick import Brick


SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720

FPS = 60

# TODO:

# add types
# make fields private


class ScoreKeeper:
    def __init__(self):
        self.score = 0
        self.score_scale = 1

    def break_brick(self):
        self.score += 100
        self.score_scale += 0.3

    def get_score(self):
        return self.score

    def hit_puddle(self):
        self.score += 10
        self.score_scale = 1


class Game(GameObject):
    def __init__(self, screen):
        super().__init__(screen)
        self.falling_bricks = None
        self.paddle = None
        self.ball = None
        self.bricks = None
        self.score_keeper = None
        self.score_msg = ""
        self.test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
        pygame.mixer.music.load('sounds/song.mp3')
        pygame.mixer.music.play(-1)
        self.hit_brick_sound = pygame.mixer.Sound("sounds/hit1.mp3")
        self.hit_wall_sound = pygame.mixer.Sound("sounds/hit2.mp3")

        self.load_game()


    @staticmethod
    def random_color_generator():
        # TODO:
        #  Fix too dark color
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return Color(r, g, b)

    def load_game(self, restart_score=True):
        self.paddle = Paddle(self.screen)
        self.ball = Ball(self.screen)
        self.bricks = []
        self.falling_bricks = []
        if restart_score:
            self.score_keeper = ScoreKeeper()
        for y in range(11):
            color = self.random_color_generator()
            for x in range(16):
                self.bricks.append(Brick(x * 80 + 5, y * 30 + 40, 150 / 2, 25, self.screen, color))

    def update(self, delta_time):
        self.paddle.x_vel = 0
        keys = pygame.key.get_pressed()

        self.score_msg = f'Score: {self.score_keeper.get_score()}'

        for i, falling_brick in enumerate(self.falling_bricks):
            falling_brick.update(delta_time)
            if falling_brick.y + falling_brick.height > self.screen.height:
                self.falling_bricks.pop(i)

        if self.ball.is_down():
            self.score_msg += "   press R to restart"
            if keys[pygame.K_r]:
                self.load_game()
            return

        if keys[pygame.K_a]:
            self.paddle.x_vel = -1
        if keys[pygame.K_d]:
            self.paddle.x_vel = 1

        if self.ball.is_collide(self.paddle):
            self.score_keeper.hit_puddle()
            pygame.mixer.Sound.play(self.hit_wall_sound)

        self.paddle.update(delta_time)
        self.ball.update(delta_time)

        for i, rect in enumerate(self.bricks):
            if self.ball.is_collide(rect):
                self.score_keeper.break_brick()
                self.bricks.pop(i)
                pygame.mixer.Sound.play(self.hit_brick_sound)

                # Split brick into small bricks
                SPLITS = 2
                FORCE_SCALAR = 0.03
                for x in range(2 ** SPLITS):
                    for y in range(2 ** SPLITS):
                        new_width = rect.width / (2 ** SPLITS)
                        new_height = rect.height / (2 ** SPLITS)
                        b = Brick(rect.x + new_width*x, rect.y + new_height*y, new_width, new_height, self.screen, rect.color)

                        v = (b.x + b.width) - self.ball.x, (b.y + b.height) - self.ball.y
                        magnitude = (v[0]**2 + v[1]**2)**0.5

                        b.add_force((v[0] / magnitude) * FORCE_SCALAR, (v[1] / magnitude) * FORCE_SCALAR)
                        self.falling_bricks.append(b)

        if len(self.bricks) == 0:
            self.load_game(restart_score=False)

    def draw(self):
        score_surf = self.test_font.render(self.score_msg, False, (64, 64, 64))
        score_rect = score_surf.get_rect(center=(self.screen.width / 2, self.screen.height - 200))
        self.screen.blit(score_surf, score_rect)

        for falling_brick in self.falling_bricks:
            falling_brick.draw()

        self.paddle.draw()
        for brick in self.bricks:
            brick.draw()
        self.ball.draw()


def main():
    pygame.init()
    pygame.display.set_caption("GalamBreak")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    running = True

    game = Game(screen)

    while running:
        delta_time = clock.tick(FPS)

        # poll for events
        # pygame.QUIT event means the user clicked X to close your window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print(pos)

        game.update(delta_time)

        screen.fill(Color(25, 25, 25))
        game.draw()

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()


if __name__ == '__main__':
    main()
