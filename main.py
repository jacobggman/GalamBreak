import pygame
from pygame import Color

from game_controller import GameController

SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
BACKGROUND_COLOR = Color(25, 25, 25)
FPS = 60

# TODO:
# Make score text class
# Make sounds class


def main():
    pygame.init()
    pygame.display.set_caption("GalamBreak")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    clock = pygame.time.Clock()
    running = True

    game = GameController(screen)

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

        screen.fill(Color(BACKGROUND_COLOR))
        game.draw()

        # flip() the display to put your work on screen
        pygame.display.flip()

        clock.tick(FPS)  # limits FPS to 60

    pygame.quit()


if __name__ == '__main__':
    main()
