import pygame
import sys

from settings import *

pygame.init()
vec = pygame.math.Vector2


class Pacman:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()  # used to simulate FPS
        self.running = True
        self.state = 'start'
        # state represents a screen. There should be at least Start, Playing & GameOver screens. Each screen should have events, update and draw functions
        self.load()
        self.grid_cell_width = BACKGROUND_WIDTH//28
        self.grid_cell_height = BACKGROUND_HEIGHT//30

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
            else:
                self.running = False
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    #------------------------------------------------- Helper functions - function that would be used in several places

    def draw_text(self, text, screen, positions, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        display_text = font.render(text, False, colour)
        display_text_size = display_text.get_size()
        if centered:
            positions[0] = positions[0]-display_text_size[0]//2
            positions[1] = positions[1]-display_text_size[1]//2
        screen.blit(display_text, positions)

    def load(self):
        self.background = pygame.image.load('background.png')
        self.background = pygame.transform.scale(self.background, (BACKGROUND_WIDTH, BACKGROUND_HEIGHT))

    def draw_grid(self):
        #draw vertical lines
        for x in range(SCREEN_WIDTH//self.grid_cell_width):
            pygame.draw.line(self.background, GREY, (x*self.grid_cell_width, 0), (x*self.grid_cell_width, SCREEN_HEIGHT))
        #draw horizontal line
        for x in range(SCREEN_HEIGHT//self.grid_cell_height):
            pygame.draw.line(self.background, GREY, (0, x*self.grid_cell_height), (SCREEN_WIDTH, x*self.grid_cell_height))
    #------------------------------------------------- Start screen functions -------------------------------------------------#

    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # ToDO: decide and add key to lead to setting screen
                self.state = "game on"

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text("PRESS SPACE KEY", self.screen, [SCREEN_WIDTH//2, SCREEN_HEIGHT//2-50], TEXT_SIZE_START, PRESS_TO_START_COLOR, DEFAULT_FONT, True)
        self.draw_text("1 PLAYER ONLY", self.screen, [SCREEN_WIDTH//2, SCREEN_HEIGHT//2+50], TEXT_SIZE_START, START_INFO_COLOR, DEFAULT_FONT, True)
        self.draw_text("HIGH SCORE", self.screen, [4, 0], TEXT_SIZE_START, WHITE, DEFAULT_FONT, False)
        pygame.display.update()

    #------------------------------------------------- Active game screen functions -------------------------------------------------#

    def game_on_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def game_on_update(self):
        pass

    def game_on_draw(self):
        self.screen.fill(BLACK)
        background_position = SCREEN_BUFFER//2
        self.screen.blit(self.background, (background_position,background_position))
        self.draw_grid()

        texture_pixels_aside = 60
        current_score_position = [texture_pixels_aside, 0]
        hight_score_position = [SCREEN_WIDTH//2+texture_pixels_aside, 0]
        self.draw_text('CURRENT SCORE: 0', self.screen, current_score_position, 18, WHITE, DEFAULT_FONT)
        self.draw_text('HIGH SCORE: 0', self.screen, hight_score_position, 18, WHITE, DEFAULT_FONT) #ToDO: 'HIGH SCORE: {}'.format(self.player.score)
        pygame.display.update()
