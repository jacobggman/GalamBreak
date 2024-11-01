import random

import pygame

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
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return r, g, b

    def load_game(self, restart_score=True):
        self.paddle = Paddle(self.screen)
        self.ball = Ball(self.screen)
        self.bricks = []
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

        if len(self.bricks) == 0:
            self.load_game(restart_score=False)

    def draw(self):
        score_surf = self.test_font.render(self.score_msg, False, (64, 64, 64))
        score_rect = score_surf.get_rect(center=(self.screen.width / 2, self.screen.height - 200))
        self.screen.blit(score_surf, score_rect)

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

        screen.fill("black")
        game.draw()

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()


if __name__ == '__main__':
    main()
