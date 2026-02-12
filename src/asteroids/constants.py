"""Game constants and configuration."""

from pathlib import Path

import arcade

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

# Particle effects for explosions
PARTICLE_FADE_RATE = 8
PARTICLE_MIN_SPEED = 2.5
PARTICLE_SPEED_RANGE = 2.5
PARTICLE_COUNT = 20
PARTICLE_RADIUS = 3
PARTICLE_COLORS = [
    arcade.color.LIGHT_GRAY,
    arcade.color.GRAY,
    arcade.color.WHITE,
    arcade.color.LIGHT_STEEL_BLUE,
]

# Thruster particle effects
THRUSTER_PARTICLE_FADE_RATE = 12
THRUSTER_PARTICLE_LIFETIME = 0.3  # seconds
THRUSTER_PARTICLE_RADIUS = 2
THRUSTER_PARTICLE_COLORS = [
    arcade.color.ORANGE,
    arcade.color.YELLOW,
    arcade.color.RED,
]
