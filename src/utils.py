"""
Utility Functions

Helper functions for the keystroke authentication system.
"""

import re
from pathlib import Path


# Sample paragraphs for typing tests
SAMPLE_PARAGRAPHS = [
    {
        "id": "solar",
        "title": "The Solar System",
        "text": "The Moon is a barren, rocky world without air and water. The Moon keeps changing its shape as it moves round the Earth. The Sun is the star at the center of the Solar System."
    },
    {
        "id": "nature", 
        "title": "Nature",
        "text": "The forest is home to countless species of plants and animals. Trees provide shelter and food for many creatures. Rivers flow through the landscape, bringing life to all they touch."
    },
    {
        "id": "technology",
        "title": "Technology",
        "text": "Computers have transformed the way we live and work. The internet connects people across the globe instantly. Modern technology continues to evolve at an unprecedented rate."
    },
    {
        "id": "history",
        "title": "Ancient History",
        "text": "The great pyramids of Egypt stand as monuments to human ingenuity. Ancient civilizations built remarkable structures that still inspire awe. Their achievements continue to influence modern architecture."
    },
    {
        "id": "science",
        "title": "Scientific Discovery",
        "text": "Scientists explore the mysteries of the universe every day. From atoms to galaxies, there is always more to discover. Research and experimentation drive our understanding forward."
    }
]


def get_random_paragraph() -> dict:
    """Get a random paragraph for typing test."""
    import random
    return random.choice(SAMPLE_PARAGRAPHS)


def get_paragraph_by_id(paragraph_id: str) -> dict:
    """Get a specific paragraph by ID."""
    for para in SAMPLE_PARAGRAPHS:
        if para['id'] == paragraph_id:
            return para
    return SAMPLE_PARAGRAPHS[0]


def validate_username(username: str) -> tuple[bool, str]:
    """
    Validate username format.
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not username:
        return False, "Username cannot be empty"
    
    if len(username) < 2:
        return False, "Username must be at least 2 characters"
    
    if len(username) > 20:
        return False, "Username must be 20 characters or less"
    
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$', username):
        return False, "Username must start with a letter and contain only letters, numbers, and underscores"
    
    return True, ""


def calculate_text_similarity(typed: str, original: str) -> float:
    """
    Calculate similarity between typed text and original.
    
    Returns:
        Similarity score between 0 and 1
    """
    if not original:
        return 0.0
    
    typed = typed.lower().strip()
    original = original.lower().strip()
    
    # Simple character-level comparison
    matches = sum(1 for a, b in zip(typed, original) if a == b)
    max_len = max(len(typed), len(original))
    
    if max_len == 0:
        return 0.0
    
    return matches / max_len


def get_project_root() -> Path:
    """Get the project root directory."""
    return Path(__file__).parent.parent


def get_data_path() -> Path:
    """Get the data directory path."""
    return get_project_root() / 'data'


def get_models_path() -> Path:
    """Get the models directory path."""
    return get_project_root() / 'models'


def ensure_directories() -> None:
    """Ensure required directories exist."""
    get_data_path().mkdir(parents=True, exist_ok=True)
    get_models_path().mkdir(parents=True, exist_ok=True)

