"""Main entry point for the game."""
import math
import random
from enum import IntEnum

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

    def __init__(self, scale: float, asteroid_type: AsteroidType) -> None:
        self.asteroid_type: AsteroidType = asteroid_type
        texture_path = random.choice(self.asteroid_images[asteroid_type])
        super().__init__(texture_path, scale=scale)

        # Set position
        self.center_y = random.randrange(BOTTOM_LIMIT, TOP_LIMIT)
        self.center_x = random.randrange(LEFT_LIMIT, RIGHT_LIMIT)

        # Set speed / rotation
        self.change_x = random.random() * 2 - 1
        self.change_y = random.random() * 2 - 1
        self.change_angle = (random.random() - 0.5) * 2

    def update(self, delta_time: float = 1 / 60, **kwargs) -> None:
        """ Move the asteroid around. """
        super().update(delta_time)
        if self.center_x < LEFT_LIMIT:
            self.center_x = RIGHT_LIMIT
        if self.center_x > RIGHT_LIMIT:
            self.center_x = LEFT_LIMIT
        if self.center_y > TOP_LIMIT:
            self.center_y = BOTTOM_LIMIT
        if self.center_y < BOTTOM_LIMIT:
            self.center_y = TOP_LIMIT


class ShipSprite(arcade.Sprite):
    """ Sprite that represents our spaceship. """
    thrust_amount = 0.2
    turn_speed = 3

    def __init__(self, texture_path, scale: float) -> None:
        """ Set up the spaceship. """

        # Call the parent Sprite constructor
        super().__init__(texture_path, scale=scale)

        # Info on the space ship.
        # Angle comes in automatically from the parent class.
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
        """ Update our position and other particulars. """

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


class GameWindow(arcade.Window):
    """Main game window."""

    def __init__(self) -> None:
        """Initialize the game window."""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.background_color = arcade.color.DARK_LAVENDER  # Color(42, 42, 42, 255)

        self.player_sprite = ShipSprite(
            ":resources:images/space_shooter/playerShip1_blue.png",
            scale=SCALE,
        )
        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player_sprite)

        self.score = 0
        self.asteroid_list = arcade.SpriteList()

        # Text fields
        self.text_score = arcade.Text(
            f"Score: {self.score}",
            x=10,
            y=70,
            font_size=13,
        )
        self.text_asteroid_count = arcade.Text(
            f"Asteroid Count: {len(self.asteroid_list)}",
            x=10,
            y=50,
            font_size=13,
        )

    def setup(self) -> None:
        """Set up the game, initialize variables."""

        for _ in range(STARTING_ASTEROID_COUNT):
            # Pick one of four random rock images
            asteroid_sprite = AsteroidSprite(
                scale=SCALE,
                asteroid_type=AsteroidType.BIG,
            )

            self.asteroid_list.append(asteroid_sprite)

        self.text_score.text = f"Score: {self.score}"
        self.text_asteroid_count.text = f"Asteroid Count: {len(self.asteroid_list)}"

    def on_draw(self) -> None:
        """Draw the game."""

        # Clear the screen to the background color
        self.clear()

        # Draw our sprites
        self.player_sprite_list.draw()
        self.asteroid_list.draw()

        # Draw the text
        self.text_score.draw()
        self.text_asteroid_count.draw()

    def on_update(self, delta_time: float) -> None:
        """Update game logic."""
        self.player_sprite_list.update()
        self.asteroid_list.update()

        # Collision
        if not self.player_sprite.respawning:
            colliding_asteroids = self.player_sprite.collides_with_list(self.asteroid_list)
            if colliding_asteroids:
                self.player_sprite.respawn()

        # Update the text objects
        self.text_score.text = f"Score: {self.score}"
        self.text_asteroid_count.text = f"Asteroid Count: {len(self.asteroid_list)}"

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Called whenever a key is pressed."""
        if symbol == arcade.key.ESCAPE:
            self.close()
        self.player_sprite.on_key_press(symbol)

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
