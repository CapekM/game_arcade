"""Main entry point for the game."""

import arcade

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Asteroids"
PLAYER_MOVEMENT_SPEED = 5


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

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite
        )

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
        print(f"{self.player_sprite.position = }")
        print(f"{self.player_sprite.center_x = }")
        print(f"{self.player_sprite.center_y = }")
        self.physics_engine.update()

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Handle key press events."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key: int, modifiers: int) -> None:
        """Handle key release events."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0


def main() -> None:
    """Main function to start the game."""
    window = GameWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
