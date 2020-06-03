import pygame
import sys

from settings import *
from player import *
from ghost import *

pygame.init()
pygame.display.set_caption(TITLE)
vec = pygame.math.Vector2


class Pacman:

    def __init__(self):
        programIcon = pygame.image.load('icon.png')

        pygame.display.set_icon(programIcon)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()  # used to simulate FPS
        self.running = True
        self.state = 'start'
        # state represents a screen. There should be at least Start, Playing & GameOver screens. Each screen should have events, update and draw functions
        self.grid_cell_width = BACKGROUND_WIDTH // COLS
        self.grid_cell_height = BACKGROUND_HEIGHT // ROWS
        self.walls = []
        self.coins = []
        self.ghosts = []
        self.high_score = 20  # ToDo: Extract the high score to file
        self.player_position = None
        self.ghosts_position = []
        self.temp_counter = None
        self.ghosts_limit = 4 # add logic based on test counter
        self.has_new_high_score = False

        self.load()
        self.player = Player(self, vec(self.player_position))
        self.create_ghosts()

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            elif self.state == 'game on':
                self.game_on_events()
                self.game_on_update()
                self.game_on_draw()
            elif self.state == "settings":
                self.settings_events()
                self.settings_draw()
            elif self.state == 'game over':
                self.game_over_events()
                self.game_over_update()
                self.game_over_draw()
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    # ------------------------------------------------- Helper functions - function that would be used in several places

    def load(self):  # loads all prerequisites to play the game
        self.background = pygame.image.load('background.png')
        self.background = pygame.transform.scale(self.background, (BACKGROUND_WIDTH, BACKGROUND_HEIGHT))
        self.temp_counter = self.ghosts_limit

        # Opening map file. Create list of walls containing cordinates stored as vector
        with open("map.txt", 'r') as file:
            for index_y, line in enumerate(file):
                for index_x, character in enumerate(line):
                    if character == "W":
                        self.walls.append(vec(index_x, index_y))
                    elif character == 'C':
                        self.coins.append(vec(index_x, index_y))
                    elif character == 'P':
                        self.player_position = [index_x, index_y]
                    elif character in ["1", "2", "3", "4"]:
                        self.ghosts_position.append([index_x, index_y])
                    elif character == 'E':
                        surface = self.background
                        rectangle_position_dimensions = (index_x*self.grid_cell_width, index_y*self.grid_cell_height,
                                                         self.grid_cell_width, self.grid_cell_height)
                        pygame.draw.rect(surface, BLACK, rectangle_position_dimensions)

    def create_ghosts(self):
        for index, position in enumerate(self.ghosts_position):
            if len(self.ghosts) < self.ghosts_limit:
                self.ghosts.append(Ghost(self, vec(position), index))

    def reset_ghosts(self):
        self.ghosts = []
        self.ghosts_position = []
        with open("map.txt", 'r') as file:
            for index_y, line in enumerate(file):
                for index_x, character in enumerate(line):
                    if character in ["1", "2", "3", "4"]:
                        self.ghosts_position.append([index_x, index_y])
        self.create_ghosts()

    def draw_text(self, text, screen, positions, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        display_text = font.render(text, False, colour)
        display_text_size = display_text.get_size()
        if centered:
            positions[0] = positions[0] - display_text_size[0] // 2
            positions[1] = positions[1] - display_text_size[1] // 2
        screen.blit(display_text, positions)

    def draw_grid(self):
        # draw vertical lines
        surface = self.background
        for x in range(SCREEN_WIDTH // self.grid_cell_width):
            start_position = (x * self.grid_cell_width, 0)
            end_position = (x * self.grid_cell_width, SCREEN_HEIGHT)
            pygame.draw.line(surface, GREY, start_position, end_position)
        # draw horizontal line
        for x in range(SCREEN_HEIGHT // self.grid_cell_height):
            start_position = (0, x * self.grid_cell_height)
            end_position = (SCREEN_WIDTH, x * self.grid_cell_height)
            pygame.draw.line(surface, GREY, start_position, end_position)
        self.display_coins_and_walls_paths()

    def is_new_high_score(self):
        return self.player.current_score > self.high_score

    def display_coins_and_walls_paths(self):
        # works only if should display grid setting is set to True
        if SHOULD_DISPLAY_COLORED_WALLS:
            for wall in self.walls:
                rectangle_position_dimensions = (
                wall.x * self.grid_cell_width, wall.y * self.grid_cell_height, self.grid_cell_width,
                self.grid_cell_height)
                pygame.draw.rect(self.background, (112, 55, 163), rectangle_position_dimensions)

        if SHOULD_DISPLAY_COLORED_COINS_PATH:
            for coin in self.coins:
                rectangle_position_dimensions = (
                coin.x * self.grid_cell_width, coin.y * self.grid_cell_height, self.grid_cell_width,
                self.grid_cell_height)
                pygame.draw.rect(self.background, (167, 179, 34), rectangle_position_dimensions)

    def reset(self):
        self.has_new_high_score = False
        self.player.on_game_reset()
        self.player.reset_position()
        for ghost in self.ghosts:
            ghost.reset_position()
        self.coins = []
        with open("map.txt", "r") as file:
            for index_y, line in enumerate(file):
                for index_x, character in enumerate(line):
                    if character == 'C':
                        self.coins.append(vec(index_x, index_y))
        self.state = "game on"

    # ------------------------------------------------- Start screen functions -------------------------------------------------#

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.state = "game on"
                if event.key == pygame.K_s:
                    self.state = "settings"

    def start_update(self):  # ToDo: Remove if not used later
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text("PRESS SPACE KEY", self.screen, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50], TEXT_SIZE_START*2,
                       PRESS_TO_START_COLOR, DEFAULT_FONT, True)
        self.draw_text("1 PLAYER ONLY", self.screen, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50], TEXT_SIZE_START,
                       START_INFO_COLOR, DEFAULT_FONT, True)

        self.draw_text("PRESS S TO GO TO SETTING", self.screen, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 150], TEXT_SIZE_START,
                       GREY, DEFAULT_FONT, True)
        self.draw_text("HIGH SCORE", self.screen, [4, 0], TEXT_SIZE_START, WHITE, DEFAULT_FONT, False)
        pygame.display.update()

    # ------------------------------------------------- Active game screen functions -------------------------------------------------#

    def game_on_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pygame.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pygame.K_DOWN:
                    self.player.move(vec(0, 1))

    def game_on_update(self):
        self.player.update()
        for ghost in self.ghosts:
            ghost.update()

        for ghost in self.ghosts:
            if ghost.grid_position == self.player.grid_position:
                self.decrease_lives()

    def game_on_draw(self):
        self.screen.fill(BLACK)
        background_position = SCREEN_BUFFER // 2
        self.screen.blit(self.background, (background_position, background_position))
        self.draw_coins()
        if SHOULD_DISPLAY_GRID:
            self.draw_grid()

        # print scores
        texture_pixels_aside = 60
        current_score_position = [texture_pixels_aside, 0]
        hight_score_position = [SCREEN_WIDTH // 2 + texture_pixels_aside, 0]
        self.draw_text('CURRENT SCORE: {}'.format(self.player.current_score), self.screen, current_score_position, 18,
                       WHITE, DEFAULT_FONT)
        self.draw_text('HIGH SCORE: {}'.format(self.high_score), self.screen, hight_score_position, 18, WHITE,
                       DEFAULT_FONT)

        self.player.draw()
        for ghost in self.ghosts:
            ghost.draw()

        pygame.display.update()

    def draw_coins(self):
        # drawing to screen in order to be able to delete after player passes through coin place. If drawn on background, it's loaded only 1 time
        for coin in self.coins:
            center = (int(coin.x * self.grid_cell_width) + self.grid_cell_width // 2 + SCREEN_BUFFER // 2,
                      int(coin.y * self.grid_cell_height) + self.grid_cell_height // 2 + SCREEN_BUFFER // 2)
            radius = 5
            pygame.draw.circle(self.screen, COINS_COLOUR, center, radius)

    def decrease_lives(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "game over"
            #ToDO: add logic for updating HighScore in file after the game is finished, only if there is new high score
            if self.has_new_high_score:
                pass # write in file... also read it from file on load function
        else:
            self.player.reset_position()
            for ghost in self.ghosts:
                ghost.reset_position()

    # ------------------------------------------------- Settings screen functions -------------------------------------------------#

    def settings_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.ghosts_limit = self.temp_counter
                    self.state = "start"
                    self.reset_ghosts()
                if event.key == pygame.K_ESCAPE:
                    self.temp_counter = self.ghosts_limit
                    self.state = "start"
                if event.key == pygame.K_UP:
                    if self.temp_counter < 4:
                        self.temp_counter += 1
                if event.key == pygame.K_DOWN:
                    if self.temp_counter > 1:
                        self.temp_counter -= 1

    def settings_draw(self):
        #self.screen.blit(self.screen, (SCREEN_WIDTH-5, SCREEN_HEIGHT))
        self.screen.fill(BLACK)
        press_arrows_text = "Press the  UP arrow to INCREASE or DOWN arrow to DECREASE"
        number_of_ghosts_text = 'NUMBER OF GHOSTS: {}'.format(self.temp_counter)
        save_settings_text = "Press the SPACE button to SAVE"
        discard_settings_text = "Press the ESCAPE button to DISCARD"

        self.draw_text(number_of_ghosts_text, self.screen, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50], TEXT_SIZE_START,
                       START_INFO_COLOR, DEFAULT_FONT, True)

        self.draw_text(press_arrows_text, self.screen, [8, 5], TEXT_SIZE_START, WHITE, DEFAULT_FONT, False)
        self.draw_text(save_settings_text, self.screen, [
                       SCREEN_WIDTH//2, SCREEN_HEIGHT//2+50],  TEXT_SIZE_START, GAME_OVER_COLOR, DEFAULT_FONT, True)
        self.draw_text(discard_settings_text, self.screen, [
                       SCREEN_WIDTH//2, SCREEN_HEIGHT//2+75],  TEXT_SIZE_START, GAME_OVER_COLOR, DEFAULT_FONT, True)

        pygame.display.update()

    # ------------------------------------------------- Game Over functions -------------------------------------------------#
    def game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.reset()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def game_over_update(self):
        pass

    def game_over_draw(self):
        self.screen.fill(BLACK)
        exit_text = "Press the ESCAPE button to QUIT"
        play_again_text = "Press the SPACE button to PLAY AGAIN"
        game_over_size = 52
        options_size = 20
        self.draw_text("GAME OVER", self.screen, [SCREEN_WIDTH//2, 100],  game_over_size, RED, DEFAULT_FONT, True)
        self.draw_text(play_again_text, self.screen, [
                       SCREEN_WIDTH//2, SCREEN_HEIGHT//2],  options_size, GAME_OVER_COLOR, DEFAULT_FONT, True)
        self.draw_text(exit_text, self.screen, [
                       SCREEN_WIDTH//2, SCREEN_HEIGHT//1.5],  options_size, GAME_OVER_COLOR, DEFAULT_FONT, True)
        if self.has_new_high_score:
            new_high_score_text = 'NEW HIGH SCORE RECORD: {}'.format(self.high_score)
            self.draw_text(new_high_score_text, self.screen, [
                SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50], options_size, START_INFO_COLOR, DEFAULT_FONT, True)

        texture_pixels_aside = 60
        current_score_position = [SCREEN_WIDTH//2, 150]
        self.draw_text('SCORE: {}'.format(self.player.current_score), self.screen, current_score_position, 18,
                       WHITE, DEFAULT_FONT, True)
        pygame.display.update()