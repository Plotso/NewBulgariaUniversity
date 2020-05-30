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

    ################ Main function
    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_events()
                self.start_update()
                self.start_draw()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    ############## Helper functions - function that would be used in several places
    def draw_text(self, text, screen, positions, size, colour, font_name, centered=False):
        font = pygame.font.SysFont(font_name, size)
        display_text = font.render(text, False, colour)
        display_text_size = display_text.get_size()
        if centered:
            positions[0] = positions[0]-display_text_size[0]//2
            positions[1] = positions[1]-display_text_size[1]//2
        screen.blit(display_text, positions)

    ############## Intro functions
    def start_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:  # ToDO: decide and add key to lead to setting screen
                self.state = "playing"

    def start_update(self):
        pass

    def start_draw(self):
        self.screen.fill(BLACK)
        self.draw_text("PRESS SPACE KEY", self.screen, [SCREEN_WIDTH//2, SCREEN_HEIGHT//2-50], TEXT_SIZE_START, PRESS_TO_START_COLOR, FONT_START, True)
        self.draw_text("1 PLAYER ONLY", self.screen, [SCREEN_WIDTH//2, SCREEN_HEIGHT//2+50], TEXT_SIZE_START, START_INFO_COLOR, FONT_START, True)
        self.draw_text("HIGH SCORE", self.screen, [4, 0], TEXT_SIZE_START, WHITE, FONT_START, False)
        pygame.display.update()
