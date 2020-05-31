import pygame
vec = pygame.math.Vector2


# Settings for the in-game screen
SCREEN_WIDTH, SCREEN_HEIGHT = 610, 670
FPS = 60
SCREEN_BUFFER = 50  # buffer added on game-on screen to have space for lives and score
BACKGROUND_WIDTH, BACKGROUND_HEIGHT = SCREEN_WIDTH-SCREEN_BUFFER, SCREEN_HEIGHT-SCREEN_BUFFER
COLS, ROWS = 28, 30 # used on grid creation, the whole game logic is based on it

# Settings for debugging
SHOULD_DISPLAY_GRID = False
SHOULD_DISPLAY_COLORED_WALLS = False
SHOULD_DISPLAY_COLORED_COINS_PATH = False


# Setting for color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (208, 22, 22)
GREY = (107, 107, 107)
PLAYER_COLOUR = (190, 194, 15)
COINS_COLOUR = (124, 123, 7)

PRESS_TO_START_COLOR = (170, 132, 58)
START_INFO_COLOR = (44, 167, 198)

# Setting for font
TEXT_SIZE_START = 16
DEFAULT_FONT = 'arial black'

# Setting for the Player
START_POSITION = vec(1, 1)