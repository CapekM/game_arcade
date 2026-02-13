"""Game view classes."""

import arcade

from asteroids.constants import (
    EXPLOSION_PARTICLE_COUNT,
    SCALE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    STARTING_ASTEROID_COUNT,
)
from asteroids.highscores import get_top_scores, save_high_score
from asteroids.particles import ExplosionParticle
from asteroids.sprites import AsteroidSprite, AsteroidType, BulletSprite, ShipSprite


class MainMenuView(arcade.View):
    """Main menu view with keyboard navigation."""

    def __init__(self) -> None:
        """Initialize the main menu."""
        super().__init__()
        self.menu_options = ["Play", "Highest scores", "Options", "Exit"]
        self.selected_index = 0

    def on_show_view(self) -> None:
        """Called when this view is shown."""
        self.window.background_color = arcade.color.DARK_LAVENDER

    def on_draw(self) -> None:
        """Draw the main menu."""
        self.clear()

        # Title
        arcade.Text(
            "ASTEROIDS",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 + 150,
            font_size=64,
            anchor_x="center",
            color=arcade.color.WHITE,
        ).draw()

        # Menu options
        for i, option in enumerate(self.menu_options):
            y_position = SCREEN_HEIGHT // 2 - i * 60
            color = arcade.color.YELLOW if i == self.selected_index else arcade.color.WHITE
            font_size = 42 if i == self.selected_index else 36

            arcade.Text(
                option,
                x=SCREEN_WIDTH // 2,
                y=y_position,
                font_size=font_size,
                anchor_x="center",
                color=color,
            ).draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Handle keyboard input for menu navigation."""
        if symbol == arcade.key.UP or symbol == arcade.key.W:
            self.selected_index = (self.selected_index - 1) % len(self.menu_options)
        elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
            self.selected_index = (self.selected_index + 1) % len(self.menu_options)
        elif symbol == arcade.key.RETURN or symbol == arcade.key.SPACE:
            self._handle_selection()
        elif symbol == arcade.key.ESCAPE:
            self.window.close()

    def _handle_selection(self) -> None:
        """Handle menu option selection."""
        selected_option = self.menu_options[self.selected_index]

        if selected_option == "Play":
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)
        elif selected_option == "Highest scores":
            highscores_view = HighScoresView()
            self.window.show_view(highscores_view)
        elif selected_option == "Options":
            # TODO: Implement options menu
            pass
        elif selected_option == "Exit":
            self.window.close()


class HighScoresView(arcade.View):
    """View to display high scores."""

    def __init__(self) -> None:
        """Initialize the high scores view."""
        super().__init__()

    def on_show_view(self) -> None:
        """Called when this view is shown."""
        self.window.background_color = arcade.color.DARK_LAVENDER

    def on_draw(self) -> None:
        """Draw the high scores screen."""
        self.clear()

        # Title
        arcade.Text(
            "HIGH SCORES",
            x=SCREEN_WIDTH // 2,
            y=SCREEN_HEIGHT // 2 + 200,
            font_size=54,
            anchor_x="center",
            color=arcade.color.YELLOW,
        ).draw()

        # Get top 5 scores
        top_scores = get_top_scores(5)

        if not top_scores:
            arcade.Text(
                "No scores yet!",
                x=SCREEN_WIDTH // 2,
                y=SCREEN_HEIGHT // 2,
                font_size=36,
                anchor_x="center",
                color=arcade.color.WHITE,
            ).draw()
        else:
            # Display scores
            for i, score_entry in enumerate(top_scores):
                y_position = SCREEN_HEIGHT // 2 + 80 - i * 60
                rank = i + 1

                # Rank number
                arcade.Text(
                    f"{rank}.",
                    x=SCREEN_WIDTH // 2 - 250,
                    y=y_position,
                    font_size=32,
                    anchor_x="right",
                    color=arcade.color.GOLD if rank == 1 else arcade.color.WHITE,
                ).draw()

                # Player name
                arcade.Text(
                    str(score_entry["name"]),
                    x=SCREEN_WIDTH // 2 - 200,
                    y=y_position,
                    font_size=32,
                    anchor_x="left",
                    color=arcade.color.GOLD if rank == 1 else arcade.color.WHITE,
                ).draw()

                # Score
                arcade.Text(
                    str(score_entry["score"]),
                    x=SCREEN_WIDTH // 2 + 250,
                    y=y_position,
                    font_size=32,
                    anchor_x="right",
                    color=arcade.color.GOLD if rank == 1 else arcade.color.WHITE,
                ).draw()

        # Instructions
        arcade.Text(
            "Press ESC or ENTER to return to menu",
            x=SCREEN_WIDTH // 2,
            y=100,
            font_size=24,
            anchor_x="center",
            color=arcade.color.LIGHT_GRAY,
        ).draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        """Handle keyboard input."""
        if symbol == arcade.key.ESCAPE or symbol == arcade.key.RETURN:
            menu_view = MainMenuView()
            self.window.show_view(menu_view)


class GameView(arcade.View):
    """Main game view."""

    def __init__(self) -> None:
        """Initialize the game view."""
        super().__init__()
        self.is_over = False
        self.player_name = ""
        self.name_saved = False

        self.player_sprite = ShipSprite(
            ":resources:images/space_shooter/playerShip1_blue.png",
            scale=SCALE,
        )
        self.player_sprite_list = arcade.SpriteList()
        self.player_sprite_list.append(self.player_sprite)

        self.score = 0
        self.asteroid_list = arcade.SpriteList()
        self.bullet_list = arcade.SpriteList()
        self.particles_list = arcade.SpriteList()
        self.thruster_particles_list = arcade.SpriteList()

        # Connect thruster particles list to ship
        self.player_sprite.thruster_particles_list = self.thruster_particles_list

        # Load explosion sound
        self.explosion_sound = arcade.load_sound(":resources:sounds/explosion2.wav")

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
        self.player_name = ""
        self.name_saved = False
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

        # Draw our sprites
        self.thruster_particles_list.draw()  # Draw thruster particles behind ship
        self.player_sprite_list.draw()
        self.asteroid_list.draw()
        self.bullet_list.draw()
        self.particles_list.draw()

        # Draw the text
        self.text_score.draw()
        self.text_lives.draw()

        if self.is_over:
            if not self.name_saved:
                # Name entry screen
                arcade.Text(
                    f"Your score: {self.score}",
                    x=SCREEN_WIDTH // 2,
                    y=SCREEN_HEIGHT // 2 + 100,
                    font_size=42,
                    anchor_x="center",
                ).draw()
                arcade.Text(
                    "Enter your name:",
                    x=SCREEN_WIDTH // 2,
                    y=SCREEN_HEIGHT // 2 + 30,
                    font_size=36,
                    anchor_x="center",
                ).draw()
                # Display name with cursor
                name_display = self.player_name + "_"
                arcade.Text(
                    name_display,
                    x=SCREEN_WIDTH // 2,
                    y=SCREEN_HEIGHT // 2 - 30,
                    font_size=42,
                    anchor_x="center",
                    color=arcade.color.YELLOW,
                ).draw()
                arcade.Text(
                    "Press ENTER to save",
                    x=SCREEN_WIDTH // 2,
                    y=SCREEN_HEIGHT // 2 - 90,
                    font_size=24,
                    anchor_x="center",
                ).draw()
            else:
                # After saving, show the menu options
                arcade.Text(
                    f"Your score: {self.score}",
                    x=SCREEN_WIDTH // 2,
                    y=SCREEN_HEIGHT // 2 + 100,
                    font_size=42,
                    anchor_x="center",
                ).draw()
                arcade.Text(
                    "Score saved!",
                    x=SCREEN_WIDTH // 2,
                    y=SCREEN_HEIGHT // 2 + 30,
                    font_size=36,
                    anchor_x="center",
                    color=arcade.color.GREEN,
                ).draw()
                arcade.Text(
                    "Press R to restart the game",
                    x=SCREEN_WIDTH // 2,
                    y=SCREEN_HEIGHT // 2 - 30,
                    font_size=36,
                    anchor_x="center",
                ).draw()
                arcade.Text(
                    "Press Q to go to main menu",
                    x=SCREEN_WIDTH // 2,
                    y=SCREEN_HEIGHT // 2 - 90,
                    font_size=36,
                    anchor_x="center",
                ).draw()

    def on_update(self, delta_time: float) -> None:
        """Update game logic."""
        if self.is_over:
            return

        self.player_sprite_list.update()
        self.asteroid_list.update()
        self.bullet_list.update()
        self.particles_list.update(delta_time)
        self.thruster_particles_list.update(delta_time)

        # Bullet–asteroid collisions
        for bullet in self.bullet_list:  # iterate over a snapshot to be safe
            colliding_asteroids = bullet.collides_with_list(self.asteroid_list)
            if colliding_asteroids:
                # remove bullet
                bullet.remove_from_sprite_lists()
                # remove all hit asteroids, update score, and respawn replacements
                for asteroid in colliding_asteroids:
                    # Create explosion particles
                    for _ in range(EXPLOSION_PARTICLE_COUNT):
                        particle = ExplosionParticle()
                        particle.center_x = asteroid.center_x
                        particle.center_y = asteroid.center_y
                        self.particles_list.append(particle)

                    # Play explosion sound
                    arcade.play_sound(self.explosion_sound)
                    if asteroid.asteroid_type == AsteroidType.BIG:
                        self.score += 10
                    elif asteroid.asteroid_type == AsteroidType.MEDIUM:
                        self.score += 20
                    elif asteroid.asteroid_type == AsteroidType.SMALL:
                        self.score += 50
                    else:  # TINY
                        self.score += 100

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
            # Return to main menu
            menu_view = MainMenuView()
            self.window.show_view(menu_view)
            return

        if self.is_over:
            if not self.name_saved:
                # Handle name input
                if symbol == arcade.key.RETURN:
                    if self.player_name.strip():  # Only save if name is not empty
                        save_high_score(self.player_name.strip(), self.score)
                        self.name_saved = True
                elif symbol == arcade.key.BACKSPACE:
                    self.player_name = self.player_name[:-1]
            else:
                # After name is saved, allow restart/quit
                if symbol == arcade.key.R:
                    self.setup()
                elif symbol == arcade.key.Q:
                    menu_view = MainMenuView()
                    self.window.show_view(menu_view)
            return

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

    def on_text(self, text: str) -> None:
        """Handle text input for name entry."""
        if self.is_over and not self.name_saved:
            # Allow alphanumeric characters and spaces, limit to 15 characters
            if len(self.player_name) < 15 and (text.isalnum() or text == " "):
                self.player_name += text

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        """Called whenever a key is released."""
        if not self.is_over:
            self.player_sprite.on_key_release(symbol)
