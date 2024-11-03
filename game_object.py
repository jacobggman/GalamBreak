import pygame


class GameObject:
    def __init__(self, screen: pygame.Surface):
        self._screen: pygame.Surface = screen

    def draw(self) -> None:
        pass

    def update(self, delta_time: float) -> None:
        pass
