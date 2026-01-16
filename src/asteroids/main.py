"""Main entry point for the game."""
import math

import arcade

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Asteroids"

SCALE = 0.5

class ShipSprite(arcade.Sprite):
    """ Sprite that represents our spaceship. """
    thrust_amount = 0.2
    turn_speed = 3

    def __init__(self, texture_path, scale):
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

        # Mark that we are respawning.
        self._respawn()

    def _respawn(self):
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

    def setup(self) -> None:
        """Set up the game, initialize variables."""
        pass

    def on_draw(self) -> None:
        """Draw the game."""

        # Clear the screen to the background color
        self.clear()

        # Draw our sprites
        self.player_sprite_list.draw()

    def on_update(self, delta_time: float) -> None:
        """Update game logic."""
        self.player_sprite_list.update()

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
