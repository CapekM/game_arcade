"""Particle effects for the game."""

import math
import random

import arcade

from asteroids.constants import (
    PARTICLE_COLORS,
    PARTICLE_FADE_RATE,
    PARTICLE_MIN_SPEED,
    PARTICLE_RADIUS,
    PARTICLE_SPEED_RANGE,
    THRUSTER_PARTICLE_COLORS,
    THRUSTER_PARTICLE_LIFETIME,
    THRUSTER_PARTICLE_RADIUS,
)


class Particle(arcade.SpriteCircle):
    """Explosion particle for asteroid destruction."""

    def __init__(self) -> None:
        """Create a particle sprite."""
        super().__init__(PARTICLE_RADIUS, random.choice(PARTICLE_COLORS))

        # Set random direction and speed
        speed = random.random() * PARTICLE_SPEED_RANGE + PARTICLE_MIN_SPEED
        direction = random.randrange(360)
        self.change_x = math.sin(math.radians(direction)) * speed
        self.change_y = math.cos(math.radians(direction)) * speed

    def update(self, delta_time: float = 1 / 60) -> None:
        """Update the particle position and fade."""
        time_step = 60 * delta_time

        if self.alpha == 0:
            # Faded out, remove
            self.remove_from_sprite_lists()
        else:
            # Gradually fade out the particle
            self.alpha = max(0, self.alpha - int(PARTICLE_FADE_RATE * time_step))
            # Move the particle
            self.center_x += self.change_x * time_step
            self.center_y += self.change_y * time_step


class ThrusterParticle(arcade.SpriteCircle):
    """Fire particle for ship thrusters."""

    def __init__(self, x: float, y: float, direction: float, reverse: bool = False) -> None:
        """Create a thruster particle sprite.

        Args:
            x: Starting x position
            y: Starting y position
            direction: Ship's angle (0 is up)
            reverse: True if reverse thrusters (going backward)
        """
        super().__init__(THRUSTER_PARTICLE_RADIUS, random.choice(THRUSTER_PARTICLE_COLORS))

        self.center_x = x
        self.center_y = y

        # Particles shoot out opposite to thrust direction
        particle_angle = direction + 180 if not reverse else direction

        # Add some random spread
        spread = random.uniform(-15, 15)
        particle_angle += spread

        # Set velocity - particles shoot backward from ship
        speed = random.uniform(1.5, 3.0)
        self.change_x = math.sin(math.radians(particle_angle)) * speed
        self.change_y = math.cos(math.radians(particle_angle)) * speed

        self.lifetime = 0

    def update(self, delta_time: float = 1 / 60) -> None:
        """Update the particle position and fade."""
        self.lifetime += delta_time

        # Remove after lifetime expires
        if self.lifetime > THRUSTER_PARTICLE_LIFETIME:
            self.remove_from_sprite_lists()
        else:
            # Fade out based on lifetime
            fade_progress = self.lifetime / THRUSTER_PARTICLE_LIFETIME
            self.alpha = int(255 * (1 - fade_progress))

            # Move the particle
            self.center_x += self.change_x
            self.center_y += self.change_y

            # Shrink particle over time
            self.scale = 1.0 - (fade_progress * 0.5)
