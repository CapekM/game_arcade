"""Game constants and configuration."""

from pathlib import Path

# Game window settings
SCREEN_TITLE = "Asteroids"
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Game settings
SCALE = 0.5
STARTING_ASTEROID_COUNT = 3

# Screen limits for wrapping
OFFSCREEN_SPACE = 10
LEFT_LIMIT = -OFFSCREEN_SPACE
RIGHT_LIMIT = SCREEN_WIDTH + OFFSCREEN_SPACE
BOTTOM_LIMIT = -OFFSCREEN_SPACE
TOP_LIMIT = SCREEN_HEIGHT + OFFSCREEN_SPACE

# High scores file
HIGHSCORES_FILE = Path("highscores.json")

EXPLOSION_PARTICLE_COUNT = 20
