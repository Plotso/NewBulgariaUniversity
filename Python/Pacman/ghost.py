import pygame
import random
from settings import *

vec = pygame.math.Vector2

class Ghost:
    def __init__(self, game, position, index):
        self.game = game
        self.grid_position = position
        self.pixel_position = self.get_pixel_position()
        self.radius = int(self.game.grid_cell_width//2.3)
        self.index = index
        self.colour = self.set_colour()
        self.direction = vec(0, 0)
        self.personality = self.set_personality()
        self.target = None
        self.speed = self.set_speed()
        self.initial_position = [position.x, position.y]

    def get_pixel_position(self):
        x_cord = (self.grid_position.x * self.game.grid_cell_width) + SCREEN_BUFFER // 2 + self.game.grid_cell_width // 2
        y_cord = (self.grid_position.y * self.game.grid_cell_height) + SCREEN_BUFFER // 2 + self.game.grid_cell_height // 2
        return vec(x_cord, y_cord)

    def update(self):
        self.target = self.set_target()
        if self.target != self.grid_position:
            self.pixel_position += self.direction * self.speed
            if self.should_update_grid_position():
                self.move()

        self.set_grid_position_based_on_pixel_position()

    def draw(self):
        center = (int(self.pixel_position.x), int(self.pixel_position.y))
        pygame.draw.circle(self.game.screen, self.colour, center, self.radius)

    def reset_position(self):
        self.grid_position = vec(self.initial_position)
        self.pixel_position = self.get_pixel_position()
        self.direction *= 0

    def set_target(self):
        player_position = self.game.player.grid_position
        if self.personality == "speedy" or self.personality == "slow":
            return player_position
        else:
            if player_position[0] > COLS//2 and player_position[1] > ROWS//2:
                return vec(1, 1)
            elif player_position[0] > COLS//2 and player_position[1] < ROWS//2:
                return vec(1, ROWS-2)
            elif player_position[0] < COLS//2 and player_position[1] > ROWS//2:
                return vec(COLS-2, 1)
            else:
                return vec(COLS-2, ROWS-2)

    def set_speed(self):
        if self.personality in ["speedy", "scared"]:
            speed = 2
        else:
            speed = 1
        return speed

    def should_update_grid_position(self):
        if int(self.pixel_position.x+SCREEN_BUFFER//2) % self.game.grid_cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pixel_position.y+SCREEN_BUFFER//2) % self.game.grid_cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def move(self):
        if self.personality == "random":
            self.direction = self.get_random_direction()
        elif self.personality == "slow":
            self.direction = self.get_path_direction()
        elif self.personality == "speedy":
            self.direction = self.get_path_direction()
        elif self.personality == "scared":
            self.direction = self.get_path_direction()

    def get_path_direction(self):
        next_grid_cell = self.find_next_cell_in_path(self.target)
        direction_x = next_grid_cell[0] - self.grid_position[0]
        direction_y = next_grid_cell[1] - self.grid_position[1]
        return vec(direction_x, direction_y)

    def get_random_direction(self):
        while True:
            number = random.randint(1, 4)
            if number == 1:
                direction_x, direction_y = 1, 0
            elif number == 2:
                direction_x, direction_y = 0, 1
            elif number == 3:
                direction_x, direction_y = -1, 0
            else:
                direction_x, direction_y = 0, -1
            new_position = vec(self.grid_position.x + direction_x, self.grid_position.y + direction_y)
            if new_position not in self.game.walls:
                break
        return vec(direction_x, direction_y)

    def find_next_cell_in_path(self, target):
        entry_point = [int(self.grid_position.x), int(self.grid_position.y)]
        target_location = [int(target[0]), int(target[1])]
        #target_location = [int(self.game.player.grid_position.x), int(self.game.player.grid_position.y)]
        path = self.BFS(entry_point, target_location)
        next_cell = path[1]
        return next_cell

    # Function based on the Breadth First Search algorithm
    def BFS(self, entry, target):
        # create local grid, fill it with 0s
        grid = [[0 for x in range(COLS)] for x in range(ROWS)]

        for cell in self.game.walls:
            # the algorithm should not include walls, that's why we mark them with 1 in the local grid
            if cell.x < COLS and cell.y < ROWS:
                grid[int(cell.y)][int(cell.x)] = 1 # y is first since it's 2d array
        queue = [entry]
        path = []
        cells_visited = []
        while queue:
            current_cell = queue[0]
            queue.remove(queue[0])
            cells_visited.append(current_cell)
            if current_cell == target:
                break
            else:
                up_neighbour = [0, -1]
                right_neighbour = [1, 0]
                down_neighbour = [0, 1]
                left_neghbour = [-1, 0]
                neighbours_cells = [up_neighbour, right_neighbour, down_neighbour, left_neghbour]

                for neighbour_cell in neighbours_cells:
                    next_cell_x = neighbour_cell[0] + current_cell[0]
                    next_cell_y = neighbour_cell[1] + current_cell[1]
                    if next_cell_x >= 0 and next_cell_x < len(grid[0]):
                        if next_cell_y >= 0 and next_cell_y < len(grid):
                            next_cell = [next_cell_x, next_cell_y]
                            if next_cell not in cells_visited:
                                is_not_a_wall = grid[next_cell_y][next_cell_x] != 1
                                if is_not_a_wall:
                                    queue.append(next_cell)
                                    path.append({"Current": current_cell, "Next": next_cell})
        shortest = [target]
        while target != entry:
            for step in path:
                if step["Next"] == target: # check if the position stored as Next is equal to the desired position
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest

    def set_grid_position_based_on_pixel_position(self):
        self.grid_position[0] = (self.pixel_position[0]-SCREEN_BUFFER+self.game.grid_cell_width//2)//self.game.grid_cell_width+1
        self.grid_position[1] = (self.pixel_position[1]-SCREEN_BUFFER+self.game.grid_cell_height//2)//self.game.grid_cell_height+1

    # Functions used to populate ghost specific fields based on index
    def set_colour(self):
        if self.index == 0:
            return RED_GHOST
        if self.index == 1:
            return GREEN_GHOST
        if self.index == 2:
            return BLUE_GHOST
        if self.index == 3:
            return ORANGE_GHOST

    def set_personality(self):
        if self.index == 0:
            return "speedy"
        elif self.index == 1:
            return "slow"
        elif self.index == 2:
            return "random"
        else:
            return "scared"
