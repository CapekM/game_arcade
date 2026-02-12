"""Main entry point for the game."""

import arcade

from asteroids.constants import SCREEN_HEIGHT, SCREEN_TITLE, SCREEN_WIDTH
from asteroids.views import MainMenuView


def main() -> None:
    """Main function to start the game."""
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MainMenuView()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
