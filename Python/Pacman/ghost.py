import pygame
from settings import *

vec = pygame.math.Vector2

class Ghost:
    def __init__(self, game, position):
        self.game = game
        self.grid_position = position
        self.pixel_position = self.get_pixel_position()

    def get_pixel_position(self):
        x_cord = (self.grid_position.x * self.game.grid_cell_width) + SCREEN_BUFFER // 2 + self.game.grid_cell_width // 2
        y_cord = (self.grid_position.y * self.game.grid_cell_height) + SCREEN_BUFFER // 2 + self.game.grid_cell_height // 2
        return vec(x_cord, y_cord)

    def update(self):
        pass

    def draw(self):
        center = (int(self.pixel_position.x), int(self.pixel_position.y))
        radius = 15
        pygame.draw.circle(self.game.screen, WHITE, center, radius)
