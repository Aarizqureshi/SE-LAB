"""
Helicopter: the player-controlled vehicle. Moves vertically based on
held Up/Down keys.
"""

import pygame

THRUST = 0.4
MAX_VY = 5.0


class Helicopter:
    def __init__(self, x, y, width=40, height=24):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vy = 0.0

    def handle_input(self, keys_pressed):
        if keys_pressed[pygame.K_UP]:
            self.vy -= THRUST
        if keys_pressed[pygame.K_DOWN]:
            self.vy += THRUST

        self.vy = max(-MAX_VY, min(MAX_VY, self.vy))

    def update(self, height_bound):
        self.y += self.vy

        if self.y < 0:
            self.y = 0
            self.vy = 0

        if self.y > height_bound:
            self.y = height_bound
            self.vy = 0
        

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )
