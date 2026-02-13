"""Game sprite classes."""

import math
import random
from enum import IntEnum
from typing import Self

import arcade

from asteroids.constants import (
    BOTTOM_LIMIT,
    LEFT_LIMIT,
    RIGHT_LIMIT,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TOP_LIMIT,
)
from asteroids.particles import ThrusterParticle


class AsteroidType(IntEnum):
    """Enum for asteroid sizes."""

    BIG = 4
    MEDIUM = 3
    SMALL = 2
    TINY = 1


class AsteroidSprite(arcade.Sprite):
    """Sprite that represents an asteroid."""

    asteroid_images = {
        AsteroidType.BIG: (
            ":resources:images/space_shooter/meteorGrey_big1.png",
            ":resources:images/space_shooter/meteorGrey_big2.png",
            ":resources:images/space_shooter/meteorGrey_big3.png",
            ":resources:images/space_shooter/meteorGrey_big4.png",
        ),
        AsteroidType.MEDIUM: (
            ":resources:images/space_shooter/meteorGrey_med1.png",
            ":resources:images/space_shooter/meteorGrey_med2.png",
        ),
        AsteroidType.SMALL: (
            ":resources:images/space_shooter/meteorGrey_small1.png",
            ":resources:images/space_shooter/meteorGrey_small2.png",
        ),
        AsteroidType.TINY: (
            ":resources:images/space_shooter/meteorGrey_tiny1.png",
            ":resources:images/space_shooter/meteorGrey_tiny2.png",
        ),
    }

    def __init__(self, asteroid_type: AsteroidType) -> None:
        """Create an asteroid sprite."""
        self.asteroid_type: AsteroidType = asteroid_type
        texture_path = random.choice(self.asteroid_images[asteroid_type])
        super().__init__(texture_path)

        # Set position
        self.center_y = random.randrange(BOTTOM_LIMIT, TOP_LIMIT)
        self.center_x = random.randrange(LEFT_LIMIT, RIGHT_LIMIT)

        # Set speed / rotation
        self.change_x = random.random() * 2 - 1
        self.change_y = random.random() * 2 - 1
        self.change_angle = (random.random() - 0.5) * 2

    def update(self, delta_time: float = 1 / 60, **kwargs) -> None:
        """Move the asteroid around."""
        super().update(delta_time)
        if self.center_x < LEFT_LIMIT:
            self.center_x = RIGHT_LIMIT
        if self.center_x > RIGHT_LIMIT:
            self.center_x = LEFT_LIMIT
        if self.center_y > TOP_LIMIT:
            self.center_y = BOTTOM_LIMIT
        if self.center_y < BOTTOM_LIMIT:
            self.center_y = TOP_LIMIT

    def split(self) -> list[Self]:
        """Split the asteroid into smaller pieces upon destruction."""
        new_asteroids = []
        if self.asteroid_type == AsteroidType.BIG:
            new_type = AsteroidType.MEDIUM
        elif self.asteroid_type == AsteroidType.MEDIUM:
            new_type = AsteroidType.SMALL
        elif self.asteroid_type == AsteroidType.SMALL:
            new_type = AsteroidType.TINY
        else:
            return new_asteroids  # No smaller type to split into

        speed_multiplier = 1.5  # Makes them 50% faster than parent
        split_angle = 30  # Angle in degrees to diverge (20-45 is usually good)

        # Convert angle to radians for math functions
        theta = math.radians(split_angle)
        cos_t = math.cos(theta)
        sin_t = math.sin(theta)

        # Create two smaller asteroids
        asteroid_1 = self.__class__(asteroid_type=new_type)
        asteroid_1.center_x = self.center_x
        asteroid_1.center_y = self.center_y
        asteroid_1.change_angle *= 2

        # Rotate vector formula: x' = x*cos(t) - y*sin(t), y' = x*sin(t) + y*cos(t)
        dir_x1 = self.change_x * cos_t - self.change_y * sin_t
        dir_y1 = self.change_x * sin_t + self.change_y * cos_t
        asteroid_1.change_x = dir_x1 * speed_multiplier
        asteroid_1.change_y = dir_y1 * speed_multiplier

        asteroid_2 = self.__class__(asteroid_type=new_type)
        asteroid_2.center_x = self.center_x
        asteroid_2.center_y = self.center_y
        asteroid_1.change_angle *= 2

        # For negative angle, sin(-t) becomes -sin(t), cos(-t) stays cos(t)
        dir_x2 = self.change_x * cos_t + self.change_y * sin_t
        dir_y2 = -self.change_x * sin_t + self.change_y * cos_t
        asteroid_2.change_x = dir_x2 * speed_multiplier
        asteroid_2.change_y = dir_y2 * speed_multiplier

        return [asteroid_1, asteroid_2]


class ShipSprite(arcade.Sprite):
    """Sprite that represents our spaceship."""

    thrust_amount = 0.2
    turn_speed = 3

    def __init__(self, texture_path: str, scale: float) -> None:
        """Set up the spaceship."""
        # Call the parent Sprite constructor
        super().__init__(texture_path, scale=scale)

        # Info on the space ship.
        # Angle comes in automatically from the parent class.
        self.lives: int = 3
        self.thrust = 0
        self.drag = 0.05
        self.speed = 0
        self.max_speed = 4
        self.respawning = 0  # Counter, 0 meaning not respawning

        self.sound_spawn = arcade.load_sound(":resources:sounds/upgrade1.wav")

        # Reference to thruster particles list (will be set by GameView)
        self.thruster_particles_list: arcade.SpriteList | None = None

        # Mark that we are respawning.
        self.respawn()

    def respawn(self) -> None:
        """Called when we die and need to make a new ship.

        'respawning' is an invulnerability timer.
        """
        # If we are in the middle of respawning, this is non-zero.
        self.respawning = 1
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = SCREEN_HEIGHT // 2
        self.angle = 0
        self.alpha = 0

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        """Update our position and other particulars."""
        # Is the user spawning
        if self.respawning:
            # Increase spawn counter, setting alpha to that amount
            self.respawning += 5
            self.alpha = self.respawning
            # Once we are close enough, set alpha to 255 and clear
            # respawning flag
            if self.respawning > 230:
                self.respawning = 0
                self.alpha = 255
                arcade.play_sound(self.sound_spawn)

        # Apply drag forward
        if self.speed > 0:
            self.speed -= self.drag
            if self.speed < 0:
                self.speed = 0
        # Apply drag reverse
        if self.speed < 0:
            self.speed += self.drag
            if self.speed > 0:
                self.speed = 0

        # Apply thrust
        self.speed += self.thrust

        # Spawn thruster particles when thrusting
        if self.thrust > 0 and self.thruster_particles_list is not None and not self.respawning:
            # Calculate the back of the ship (opposite to direction of travel)
            # Ship's angle 0 is pointing up, so we need to calculate the rear position
            back_distance = self.height / 2
            back_x = self.center_x - math.sin(math.radians(self.angle)) * back_distance
            back_y = self.center_y - math.cos(math.radians(self.angle)) * back_distance

            # Create thruster particle
            particle = ThrusterParticle(back_x, back_y, self.angle, reverse=(self.thrust < 0))
            self.thruster_particles_list.append(particle)

        # Enforce speed limit
        if self.speed > self.max_speed:
            self.speed = self.max_speed
        if self.speed < -self.max_speed:
            self.speed = -self.max_speed

        # Calculate movement vector based on speed/angle
        self.change_x = math.sin(math.radians(self.angle)) * self.speed
        self.change_y = math.cos(math.radians(self.angle)) * self.speed

        # Apply movement vector
        self.center_x += self.change_x
        self.center_y += self.change_y

        # If the ship goes off-screen, move it to the other side of the window
        if self.right < 0:
            self.left = SCREEN_WIDTH
        if self.left > SCREEN_WIDTH:
            self.right = 0
        if self.top < 0:
            self.bottom = SCREEN_HEIGHT
        if self.bottom > SCREEN_HEIGHT:
            self.top = 0

        # Call the parent class.
        super().update()

    def on_key_press(self, key: int) -> None:
        """Handle key press events."""
        if key == arcade.key.UP or key == arcade.key.W:
            self.thrust = self.thrust_amount
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.thrust = -self.thrust_amount
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.change_angle = -self.turn_speed
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.change_angle = self.turn_speed

    def on_key_release(self, key: int) -> None:
        """Handle key release events."""
        if key == arcade.key.UP or key == arcade.key.W:
            self.thrust = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.thrust = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.change_angle = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.change_angle = 0


class BulletSprite(arcade.Sprite):
    """Bullet fired by the ship."""

    speed: int = 10

    def __init__(self, x: float, y: float, angle: float, scale: float) -> None:
        """Create a bullet sprite."""
        # small laser image from resources
        super().__init__(":resources:images/space_shooter/laserBlue01.png", scale=scale)
        self.center_x = x
        self.center_y = y
        # The image faces right by default, but our angle=0 means up, so subtract 90 degrees to match visuals to motion.
        self.angle = angle - 90

        self.change_x = math.sin(math.radians(angle)) * self.speed
        self.change_y = math.cos(math.radians(angle)) * self.speed

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        """Update bullet position."""
        super().update(delta_time)
        # Remove bullets that go off the expanded limits (consistent with asteroid wrap logic)
        if (
            self.center_x < LEFT_LIMIT
            or self.center_x > RIGHT_LIMIT
            or self.center_y < BOTTOM_LIMIT
            or self.center_y > TOP_LIMIT
        ):
            self.remove_from_sprite_lists()
