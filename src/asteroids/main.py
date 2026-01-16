"""Main entry point for the game."""

import arcade


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Asteroids"


class GameWindow(arcade.Window):
    """Main game window."""

    def __init__(self) -> None:
        """Initialize the game window."""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        self.background_color = arcade.color.DARK_LAVENDER  # Color(42, 42, 42, 255)

        # Variable to hold our texture for our player
        self.player_texture = arcade.load_texture(
            ":resources:images/space_shooter/playerShip1_blue.png"
        )

        # Separate variable that holds the player sprite
        self.player_sprite = arcade.Sprite(self.player_texture)
        self.player_sprite.center_x = SCREEN_WIDTH // 2
        self.player_sprite.center_y = SCREEN_HEIGHT // 2

    def setup(self) -> None:
        """Set up the game, initialize variables."""
        pass

    def on_draw(self) -> None:
        """Draw the game."""
        self.clear()
        # Draw our sprites
        arcade.draw_sprite(self.player_sprite)

    def on_update(self, delta_time: float) -> None:
        """Update game logic."""
        pass

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Handle key press events."""
        pass

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Handle key release events."""
        pass



def main() -> None:
    """Main function to start the game."""
    window = GameWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
