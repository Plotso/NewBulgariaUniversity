from settings import *
vec = pygame.math.Vector2

class Player:
    def __init__(self, game, position):
        self.game = game
        self.grid_position = position
        self.pixel_position = self.get_pixel_position()
        self.direction = vec(1, 0)
        self.stored_direction = None
        self.able_to_move = True
        self.current_score = 0
        self.speed = 2
        self.lives = LIVES
        self.initial_position = [position.x, position.y]

    def get_pixel_position(self):
        x_cord = (self.grid_position.x * self.game.grid_cell_width) + SCREEN_BUFFER // 2 + self.game.grid_cell_width // 2
        y_cord = (self.grid_position.y * self.game.grid_cell_height) + SCREEN_BUFFER // 2 + self.game.grid_cell_height // 2
        return vec(x_cord, y_cord)

    def update(self):
        if self.able_to_move:
            self.pixel_position += self.direction*self.speed
        if self.should_update_grid_position():
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()

        # Setting grid position based on pixel position
        self.grid_position[0] = (self.pixel_position[0]-SCREEN_BUFFER+self.game.grid_cell_width//2)//self.game.grid_cell_width+1
        self.grid_position[1] = (self.pixel_position[1]-SCREEN_BUFFER+self.game.grid_cell_height//2)//self.game.grid_cell_height+1

        if self.is_on_coin():
            self.eat_coin()

        if self.is_on_super_coin():
            self.eat_super_coin()

        if self.is_on_ghost_reset_token():
            self.eat_ghosts_reset_token()

    def draw(self):
        center = (int(self.pixel_position.x),int(self.pixel_position.y))
        radius = self.game.grid_cell_width//2-2
        pygame.draw.circle(self.game.screen, PLAYER_COLOUR, center, radius)

        # Drawing lives
        for x in range(self.lives):
            center = (30 + 20*x, SCREEN_HEIGHT - 15)
            radius = 7
            pygame.draw.circle(self.game.screen, PLAYER_COLOUR, center, radius)

        # Drawing grid position rectangle
        if SHOULD_DISPLAY_GRID:
            rectangle_position_dimensions = (self.grid_position[0]*self.game.grid_cell_width+SCREEN_BUFFER//2,
                              self.grid_position[1]*self.game.grid_cell_height+SCREEN_BUFFER//2,
                              self.game.grid_cell_width,
                              self.game.grid_cell_height)
            width = 1
            pygame.draw.rect(self.game.screen, RED, rectangle_position_dimensions, width)

    def reset_position(self):
        self.grid_position = vec(self.initial_position)
        self.pixel_position = self.get_pixel_position()
        self.direction *= 0

    def on_game_reset(self):
        self.lives = LIVES
        self.current_score = 0

    def move(self, direction):
        self.stored_direction = direction

    def should_update_grid_position(self):
        # logic for updating player position if he has successfully moved to new cell
        if int(self.pixel_position.x+SCREEN_BUFFER//2) % self.game.grid_cell_width == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pixel_position.y+SCREEN_BUFFER//2) % self.game.grid_cell_height == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def can_move(self):
        for wall in self.game.walls:
            if vec(self.grid_position+self.direction) == wall:
                return False
        return True

    def is_on_coin(self):
        if self.grid_position in self.game.coins:
            return self.should_update_grid_position()
        return False

    def is_on_super_coin(self):
        if self.grid_position in self.game.super_coins:
            return self.should_update_grid_position()
        return False

    def is_on_ghost_reset_token(self):
        if self.grid_position in self.game.ghost_reset_tokens:
            return self.should_update_grid_position()
        return False

    def eat_coin(self):
        self.game.coins.remove(self.grid_position)
        self.current_score += 1
        if self.game.is_new_high_score():
            self.game.has_new_high_score = True
            self.game.high_score = self.current_score

    def eat_super_coin(self):
        self.game.super_coins.remove(self.grid_position)
        self.current_score += 10
        if self.game.is_new_high_score():
            self.game.has_new_high_score = True
            self.game.high_score = self.current_score

    def eat_ghosts_reset_token(self):
        self.game.ghost_reset_tokens.remove(self.grid_position)
        self.game.reset_ghosts()

