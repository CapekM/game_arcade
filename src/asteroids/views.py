"""Game views - Menu, Game Over, Levels, etc."""

import arcade


class MenuView(arcade.View):
    """Main menu view."""

    def __init__(self) -> None:
        """Initialize the menu view."""
        super().__init__()
        self.manager: arcade.gui.UIManager | None = None

    def on_show_view(self) -> None:
        """Called when this view is shown."""
        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

    def on_draw(self) -> None:
        """Draw the menu."""
        self.clear()
        arcade.draw_text(
            "Moje Super Hra",
            self.window.width / 2,
            self.window.height / 2 + 50,
            arcade.color.WHITE,
            font_size=50,
            anchor_x="center",
        )
        arcade.draw_text(
            "Press SPACE to start",
            self.window.width / 2,
            self.window.height / 2 - 50,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
        )

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Handle key press events."""
        if key == arcade.key.SPACE:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)


class GameView(arcade.View):
    """Main game view."""

    def __init__(self) -> None:
        """Initialize the game view."""
        super().__init__()
        self.player_list: arcade.SpriteList | None = None

    def setup(self) -> None:
        """Set up the game view."""
        self.player_list = arcade.SpriteList()

    def on_draw(self) -> None:
        """Draw the game."""
        self.clear()
        self.player_list.draw()

    def on_update(self, delta_time: float) -> None:
        """Update game logic."""
        self.player_list.update()

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Handle key press events."""
        if key == arcade.key.ESCAPE:
            menu_view = MenuView()
            self.window.show_view(menu_view)


class GameOverView(arcade.View):
    """Game over view."""

    def on_show_view(self) -> None:
        """Called when this view is shown."""
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self) -> None:
        """Draw the game over screen."""
        self.clear()
        arcade.draw_text(
            "Game Over",
            self.window.width / 2,
            self.window.height / 2,
            arcade.color.RED,
            font_size=50,
            anchor_x="center",
        )
        arcade.draw_text(
            "Press ENTER to return to menu",
            self.window.width / 2,
            self.window.height / 2 - 50,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center",
        )

    def on_key_press(self, key: int, modifiers: int) -> None:
        """Handle key press events."""
        if key == arcade.key.ENTER:
            menu_view = MenuView()
            self.window.show_view(menu_view)
