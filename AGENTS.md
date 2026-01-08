# AGENTS.md

Instructions for AI agents working in this Python Arcade game project.

## Project Overview

This is a Python game built with the Arcade library (v3.3.0). The project uses a modern
src-layout package structure with the package named `asteroids` located in `src/asteroids/`.

## Development Commands

### Environment Setup (using uv)
```bash
# Create virtual environment with Python 3.13
uv venv --python 3.13

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install package in development mode with dev dependencies
uv pip install -e ".[dev]"
```

### Running the Application
```bash
# Run via entry point (after pip install -e .)
asteroids

# Run as module
python -m asteroids.main

# Run main.py directly
python src/asteroids/main.py
```

### Testing Commands
```bash
# Run all tests
pytest

# Run a single test file
pytest tests/test_game.py

# Run a single test function
pytest tests/test_game.py::test_function_name

# Run tests matching a pattern
pytest -k "test_player"

# Run with verbose output
pytest -v

# Run with coverage (configured in pyproject.toml)
pytest --cov=asteroids --cov-report=term-missing

# Run without coverage
pytest --no-cov
```

### Code Quality Commands
```bash
# Lint with ruff
ruff check .

# Lint and auto-fix
ruff check . --fix

# Format code
ruff format .

# Check formatting without changes
ruff format . --check

# Type checking with mypy
mypy src/

# Run all checks
ruff check . && ruff format . --check && mypy src/
```

## Code Style Guidelines

### General Standards
- Follow PEP 8 style guidelines
- Use 4 spaces for indentation (no tabs)
- Maximum line length: 88 characters (ruff default)
- Use f-strings for string formatting
- Target Python version: 3.13+

### Import Organization
Imports must be organized in three groups, separated by blank lines:
```python
# 1. Standard library imports
import os
from pathlib import Path

# 2. Third-party imports
import arcade

# 3. Local/project imports
from .game import GameWindow
from .views import MenuView
```

### Naming Conventions
| Type | Convention | Example |
|------|------------|---------|
| Variables, functions | snake_case | `player_score`, `update_game()` |
| Classes | PascalCase | `GameWindow`, `MenuView` |
| Constants | UPPER_SNAKE_CASE | `SCREEN_WIDTH`, `SCREEN_TITLE` |
| Private members | Leading underscore | `_internal_state`, `_calculate()` |
| Module-level "constants" | UPPER_SNAKE_CASE | `DEFAULT_SPEED = 5.0` |

### Type Hints
Type hints are required for all function signatures (enforced by mypy).
Use modern Python 3.10+ syntax with `| None` instead of `Optional`:
```python
def update_game(self, delta_time: float) -> None:
    pass

def get_player(self, player_id: int) -> Player | None:
    return self._players.get(player_id)

def process_items(self, items: list[str]) -> dict[str, int]:
    return {item: len(item) for item in items}
```

### Documentation
Use docstrings for all classes and public methods (Google style):
```python
class Player:
    """Represents a player sprite in the game.
    
    Attributes:
        speed: Movement speed in pixels per second.
        health: Current health points.
    """
    
    def move(self, dx: float, dy: float) -> None:
        """Move the player by the given delta.
        
        Args:
            dx: Change in x-coordinate.
            dy: Change in y-coordinate.
        """
        pass
```

### Error Handling
- Use specific exception types, not bare `except:`
- Include meaningful error messages
- Re-raise or handle appropriately
```python
try:
    texture = arcade.load_texture(path)
except FileNotFoundError as e:
    print(f"Asset not found: {path}")
    raise
except Exception as e:
    print(f"Failed to load texture: {e}")
    return None
```

## Arcade-Specific Guidelines

### Game Architecture
- Main window class inherits from `arcade.Window`
- Game states/screens use `arcade.View` subclasses
- Use `setup()` method for initialization (called after `__init__`)
- Implement required methods: `on_draw()`, `on_update()`, `on_key_press()`

### Performance Best Practices
- Use `arcade.SpriteList` for efficient batch rendering
- Avoid creating objects in `on_update()` - pre-allocate in `setup()`
- Use spatial hashing for collision detection with many sprites

### Asset Management
- Store assets in `assets/` directory (images/, sounds/)
- Use relative paths from project root
- Load assets in `setup()` method, not `__init__()`

## File Structure
```
game_arcade/
├── assets/              # Game assets (images, sounds, maps)
│   ├── images/
│   └── sounds/
├── src/asteroids/       # Main package
│   ├── __init__.py
│   ├── main.py          # Entry point, main() function
│   ├── game.py          # GameWindow class
│   └── views.py         # Menu, GameOver, and other views
├── tests/               # Test files (test_*.py)
├── pyproject.toml       # Project config, dependencies, tool settings
├── AGENTS.md            # This file
└── README.md
```

## Git Commit Guidelines
Use conventional commits format:
```
type(scope): description

# Types: feat, fix, docs, style, refactor, test, chore
# Examples:
feat(player): add dash ability
fix(collision): resolve wall clipping issue
refactor(views): extract common UI components
```

## Ruff Rules (from pyproject.toml)
Enabled rule sets: E, F, W, I, N, B, A, C4, UP
- E/F/W: pycodestyle errors, pyflakes, warnings
- I: isort (import sorting)
- N: pep8-naming
- B: flake8-bugbear
- A: flake8-builtins
- C4: flake8-comprehensions
- UP: pyupgrade

Ignored: E501 (line length - handled by formatter), B008
