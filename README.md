# Asteroids

Asteroids game built with Python Arcade library.

## Project Structure

```
game_arcade/
├── assets/              # Graphics, sounds, maps (Tiled)
│   ├── images/
│   └── sounds/
├── src/asteroids/       # Python package
│   ├── __init__.py
│   ├── main.py          # Entry point
│   ├── game.py          # Main game window (Arcade Window)
│   └── views.py         # Menu, Game Over, Levels
├── tests/               # Tests
├── .gitignore
├── AGENTS.md            # AI agent instructions
├── pyproject.toml       # Project config and dependencies
└── README.md
```

## Installation and Running

### Using uv (recommended)

[uv](https://docs.astral.sh/uv/) is a fast Python package manager.

```bash
# Install uv (if not installed)
curl -LsSf https://astral.sh/uv/install.sh | sh  # Linux/Mac
# or
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"  # Windows

# Create virtual environment with Python 3.13
uv venv --python 3.13

# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
uv pip install -e .

# Run the game
asteroids
# or
python -m asteroids.main
```

### Alternative: pip

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -e .
```

## Development

### Install dev dependencies

```bash
uv pip install -e ".[dev]"
```

### Testing

```bash
pytest
```

### Code quality

```bash
ruff check .
ruff format .
mypy src/
```

## License

MIT License
