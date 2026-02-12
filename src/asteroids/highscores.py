"""High score management."""

import json

from asteroids.constants import HIGHSCORES_FILE


def load_high_scores() -> list[dict[str, int | str]]:
    """Load high scores from JSON file."""
    if not HIGHSCORES_FILE.exists():
        return []
    try:
        with open(HIGHSCORES_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return []


def save_high_score(name: str, score: int) -> None:
    """Save a new high score to JSON file."""
    scores = load_high_scores()
    scores.append({"name": name, "score": score})
    # Sort by score descending, keep top 10
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:10]
    try:
        with open(HIGHSCORES_FILE, "w") as f:
            json.dump(scores, f, indent=2)
    except OSError:
        pass  # Silently fail if we can't save


def get_top_scores(count: int = 5) -> list[dict[str, int | str]]:
    """Get the top N high scores."""
    scores = load_high_scores()
    return scores[:count]
