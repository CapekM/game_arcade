"""Main entry point for the game."""

import arcade
from .game import GameWindow


def main() -> None:
    """Main function to start the game."""
    window = GameWindow()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()