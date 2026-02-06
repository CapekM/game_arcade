"""Main entry point for the game."""

import math
import random
from enum import IntEnum
from typing import Self

import arcade

SCREEN_TITLE = "Asteroids"

SCALE = 0.5
STARTING_ASTEROID_COUNT = 3

# Screen dimensions and limits
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

OFFSCREEN_SPACE = 10
LEFT_LIMIT = -OFFSCREEN_SPACE
RIGHT_LIMIT = SCREEN_WIDTH + OFFSCREEN_SPACE
BOTTOM_LIMIT = -OFFSCREEN_SPACE
TOP_LIMIT = SCREEN_HEIGHT + OFFSCREEN_SPACE


class AsteroidType(IntEnum):
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

    def __init__(self, texture_path, scale: float) -> None:
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

        # Mark that we are respawning.
        self.respawn()

    def respawn(self):
        """
        Called when we die and need to make a new ship.
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

        """ Call the parent class. """
        super().update()

    def on_key_press(self, key: int):
        # TODO particles for ohen za zadkem
        if key == arcade.key.UP or key == arcade.key.W:
            self.thrust = self.thrust_amount
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.thrust = -self.thrust_amount
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.change_angle = -self.turn_speed
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.change_angle = self.turn_speed

    def on_key_release(self, key: int):
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
        # small laser image from resources
        super().__init__(":resources:images/space_shooter/laserBlue01.png", scale=scale)
        self.center_x = x
        self.center_y = y
        # The image faces right by default, but our angle=0 means up, so subtract 90 degrees to match visuals to motion.
        self.angle = angle - 90

        self.change_x = math.sin(math.radians(angle)) * self.speed
        self.change_y = math.cos(math.radians(angle)) * self.speed

    def update(self, delta_time: float = 1 / 60, *args, **kwargs) -> None:
        super().update(delta_time)
        # Remove bullets that go off the expanded limits (consistent with asteroid wrap logic)
        if (
            self.center_x < LEFT_LIMIT
            or self.center_x > RIGHT_LIMIT
            or self.center_y < BOTTOM_LIMIT
            or self.center_y > TOP_LIMIT
        ):
            self.remove_from_sprite_lists()


class GameWindow(arcade.Window):
    """Main game window."""

    def __init__(self) -> None:
        """Initialize the game window."""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.is_over = False
        self.background_color = arcade.color.DARK_LAVENDER  # Color(42, 42, 42, 255)

        self.player_sprite = ShipSprite(
            ":resources:images/space_shooter/playerShip1_blue.png",
            scale=SCALE,
        )
        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player_sprite)

        self.score = 0
        self.asteroid_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()

        # Text fields
        self.text_score = arcade.Text(
            f"Score: {self.score}",
            x=10,
            y=SCREEN_HEIGHT - 80,
            font_size=20,
        )
        self.text_lives = arcade.Text(
            f"Lives: {self.player_sprite.lives}",
            x=10,
            y=SCREEN_HEIGHT - 50,
            font_size=20,
        )

    def setup(self) -> None:
        """Set up the game, initialize variables."""
        self.is_over = False
        self.asteroid_list.clear()
        self.score = 0
        self.player_sprite.lives = 1  # TODO change to 3 after testing

        for _ in range(STARTING_ASTEROID_COUNT):
            # Pick one of four random rock images
            asteroid_sprite = AsteroidSprite(
                asteroid_type=AsteroidType.BIG,
            )

            self.asteroid_list.append(asteroid_sprite)

        self.text_score.text = f"Score: {self.score}"
        self.text_lives.text = f"Lives: {self.player_sprite.lives}"

    def on_draw(self) -> None:
        """Draw the game."""

        # Clear the screen to the background color
        self.clear()

        if self.is_over:
            arcade.Text(
                f"Your score: {self.score}",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT // 2 + 30,
                font_size=42,
                anchor_x="center",
            ).draw()
            arcade.Text(
                "Press R to restart the game",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT // 2 - 30,
                font_size=42,
                anchor_x="center",
            ).draw()

        # Draw our sprites
        self.player_sprite_list.draw()
        self.asteroid_list.draw()
        self.bullet_list.draw()

        # Draw the text
        self.text_score.draw()
        self.text_lives.draw()

    def on_update(self, delta_time: float) -> None:
        """Update game logic."""
        if self.is_over:
            return

        self.player_sprite_list.update()
        self.asteroid_list.update()
        self.bullet_list.update()

        # Bullet–asteroid collisions
        for bullet in self.bullet_list:  # iterate over a snapshot to be safe
            colliding_asteroids = bullet.collides_with_list(self.asteroid_list)
            if colliding_asteroids:
                # remove bullet
                bullet.remove_from_sprite_lists()
                # remove all hit asteroids, update score, and respawn replacements
                for asteroid in colliding_asteroids:
                    self.score += 10
                    asteroid.remove_from_sprite_lists()
                    new_asteroids = asteroid.split()
                    self.asteroid_list.extend(new_asteroids)

        # Collision
        if not self.player_sprite.respawning:
            colliding_asteroids = self.player_sprite.collides_with_list(self.asteroid_list)
            if colliding_asteroids:
                self.player_sprite.respawn()
                self.player_sprite.lives -= 1

        # Update the text objects
        self.text_score.text = f"Score: {self.score}"
        self.text_lives.text = f"Lives: {self.player_sprite.lives}"

        if self.player_sprite.lives <= 0:
            self.is_over = True

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Called whenever a key is pressed."""
        if symbol == arcade.key.ESCAPE:
            self.close()

        if self.is_over and symbol == arcade.key.R:
            self.setup()

        if not self.is_over:
            self.player_sprite.on_key_press(symbol)

            # Fire bullet on SPACE
            if symbol == arcade.key.SPACE:
                bullet = BulletSprite(
                    self.player_sprite.center_x,
                    self.player_sprite.center_y,
                    self.player_sprite.angle,  # pass game angle (ShipSprite uses 0 as up)
                    SCALE,
                )
                self.bullet_list.append(bullet)

                # Go ahead and move it a frame
                bullet.update()

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        """Called whenever a key is released."""
        self.player_sprite.on_key_release(symbol)


def main() -> None:
    """Main function to start the game."""
    window = GameWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
