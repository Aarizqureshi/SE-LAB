"""
GameEngine: owns the helicopter and all obstacles.

Starter version: the helicopter moves and obstacles scroll by, but
there's no collision detection at all yet (the helicopter can fly
straight through obstacles harmlessly), no scoring, and no shield.
That's Tasks 2, 3, and 4. Movement also has known bugs (see
game/helicopter.py) that Task 1 asks you to fix.
"""
import random
import pygame

from game.helicopter import Helicopter
from game.obstacle import Obstacle
from game.renderer import WIDTH, HEIGHT


SPAWN_INTERVAL_FRAMES = 90
GAP_HEIGHT = 150
WALL_WIDTH = 60
SCROLL_SPEED = 3


class GameEngine:
    def __init__(self):
        self.helicopter = Helicopter(x=100, y=HEIGHT / 2)
        self.obstacles = []
        self.frames_until_spawn = 0
        self.game_over = False
        self.distance = 0
        self.shield_active= False
        

    def _spawn_obstacle(self):
        margin = 60
        gap_y = random.randint(
            margin + GAP_HEIGHT // 2,
            HEIGHT - margin - GAP_HEIGHT // 2
        )

        self.obstacles.append(
            Obstacle(
                x=WIDTH,
                gap_y=gap_y,
                gap_height=GAP_HEIGHT,
                wall_width=WALL_WIDTH,
                screen_height=HEIGHT,
                speed=SCROLL_SPEED
            )
        )

    def handle_input(self, keys_pressed):
        self.helicopter.handle_input(keys_pressed)

    def handle_keydown(self, key):
        if key == pygame.K_r and self.game_over:
            self.__init__()
            return

        if key == pygame.K_SPACE and not self.game_over:
            self.shield_active = True
            
    def update(self):
        if self.game_over:
            return

        self.distance += SCROLL_SPEED

        self.helicopter.update(HEIGHT)

        self.frames_until_spawn -= 1

        if self.frames_until_spawn <= 0:
            self._spawn_obstacle()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for obstacle in self.obstacles:
            obstacle.update()

        heli_rect = self.helicopter.get_rect()

        for obstacle in self.obstacles:
            if (
                heli_rect.colliderect(obstacle.get_top_rect())
                or heli_rect.colliderect(obstacle.get_bottom_rect())
            ):
                if self.shield_active:
                    self.shield_active = False
                else:
                    self.game_over = True

                break

        self.obstacles = [
            o for o in self.obstacles
            if not o.is_off_screen()
        ]
        
    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(
            surface,
            self.helicopter,
            self.obstacles,
            self.shield_active
        )

        renderer.draw_text(
            surface,
            font,
            f"Distance: {self.distance}",
            (10, 10)
        )

        if self.shield_active:
            renderer.draw_text(
                surface,
                font,
                "SHIELD ACTIVE",
                (10, 40)
            )

        if self.game_over:
            renderer.draw_banner(
                surface,
                font,
                f"GAME OVER - Distance: {self.distance}"
            )

            renderer.draw_text(
                surface,
                font,
                "Press R to Restart",
                (surface.get_width() // 2 - 100,
                surface.get_height() // 2 + 35)
            )