from __future__ import annotations

from enum import Enum
from typing import Dict, List, Tuple

# categories source of truth
class CategoryKey(str, Enum):
    NATURAL_WONDERS   = "natural_wonders"
    GLOBAL_TRIVIA     = "global_trivia"
    CAPITAL_CITIES    = "capital_cities"
    CULTURAL_FOODS    = "cultural_foods"
    ANIMAL_HABITATS   = "animal_habitats"
    LANGUAGES_WORLD   = "languages_world"
    OCEANS_SEAS       = "oceans_seas"
    COUNTRY_FLAGS     = "country_flags"
    FAMOUS_LANDMARKS  = "famous_landmarks"
    
# Human-friendly display labels for the UI.
CATEGORY_LABELS: Dict[str, str] = {
    CategoryKey.NATURAL_WONDERS.value:  "Natural Wonders",
    CategoryKey.GLOBAL_TRIVIA.value:    "Global Trivia",
    CategoryKey.CAPITAL_CITIES.value:   "Capital Cities",
    CategoryKey.CULTURAL_FOODS.value:   "Cultural Foods",
    CategoryKey.ANIMAL_HABITATS.value:  "Animal Habitats",
    CategoryKey.LANGUAGES_WORLD.value:  "Languages of the World",
    CategoryKey.OCEANS_SEAS.value:      "Oceans & Seas",
    CategoryKey.COUNTRY_FLAGS.value:    "Country Flags",
    CategoryKey.FAMOUS_LANDMARKS.value: "Famous Landmarks",
}

# Fast membership checks / SQLAlchemy Enum values
CATEGORY_KEYS: Tuple[str, ...] = tuple(e.value for e in CategoryKey)

def is_valid_category(value: str | None) -> bool:
    """
    Return True if `value` is a valid *key* or *label* (case-insensitive for labels).
    """
    if not value:
        return False
    if value in CATEGORY_KEYS:
        return True
    # Label match (case-insensitive, normalized)
    v = normalize_label(value)
    return any(normalize_label(lbl) == v for lbl in CATEGORY_LABELS.values())

def coerce_category(value: str) -> str:
    """
    Coerce an incoming string (key or label) to the canonical *key*.
    Raises ValueError if it cannot be resolved.

    Accepts:
      - "natural_wonders"  -> "natural_wonders"
      - "Natural Wonders"  -> "natural_wonders"
      - " NATURAL  WONDERS " -> "natural_wonders"
    """
    if value in CATEGORY_KEYS:
        return value

    normalized = normalize_label(value)
    for key, label in CATEGORY_LABELS.items():
        if normalize_label(label) == normalized:
            return key

    raise ValueError(f"Unknown category: {value!r}")


def all_categories() -> List[Dict[str, str]]:
    """Return a list of {"key": <key>, "label": <label>} for APIs/UI."""
    return [{"key": k, "label": v} for k, v in CATEGORY_LABELS.items()]


# --------------------
# Internal helpers
# --------------------
def normalize_label(s: str) -> str:
    """
    Normalize labels for comparison:
      - lowercase
      - replace ampersands with 'and'
      - collapse whitespace
      - strip leading/trailing spaces
    """
    s = (s or "").lower().replace("&", "and").strip()
    parts = s.split()
    return " ".join(parts)