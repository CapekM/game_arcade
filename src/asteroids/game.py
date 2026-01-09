"""Main game window class."""

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

    def setup(self) -> None:
        """Set up the game, initialize variables."""
        pass

    def on_draw(self) -> None:
        """Draw the game."""
        self.clear()
        # Draw game elements here

    def on_update(self, delta_time: float) -> None:
        """Update game logic."""
        pass

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Handle key press events."""
        pass

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Handle key release events."""
        pass
