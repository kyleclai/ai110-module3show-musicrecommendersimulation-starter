import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# Challenge 2: Scoring Modes
# Each mode is a dict of weights for the three primary signals.
# Popularity and decade bonuses are fixed at +0.5 each when provided by the
# user profile — they are additive features, not part of the mode strategy.
# ---------------------------------------------------------------------------
SCORING_MODES: Dict[str, Dict[str, float]] = {
    "balanced":       {"genre": 2.0, "mood": 1.0, "energy": 1.0},
    "genre-first":    {"genre": 4.0, "mood": 0.5, "energy": 0.5},
    "mood-first":     {"genre": 0.5, "mood": 4.0, "energy": 0.5},
    "energy-focused": {"genre": 1.0, "mood": 1.0, "energy": 2.0},
}


def max_possible_score(mode: str, user_prefs: Dict) -> float:
    """Return the maximum score achievable for a given mode and user profile."""
    w = SCORING_MODES[mode]
    total = w["genre"] + w["mood"] + w["energy"]
    if "target_popularity" in user_prefs:
        total += 0.5
    if "target_decade" in user_prefs:
        total += 0.5
    return total


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float
    # Challenge 1: new features — defaults keep existing tests passing
    popularity: int = 50
    release_decade: int = 2020


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    # Challenge 1: optional advanced preferences
    target_popularity: Optional[int] = None
    target_decade: Optional[int] = None


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of song dictionaries with typed values."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            # Challenge 1: cast new columns when present
            if "popularity" in row:
                row["popularity"] = int(row["popularity"])
            if "release_decade" in row:
                row["release_decade"] = int(row["release_decade"])
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict, weights: Optional[Dict] = None) -> Tuple[float, str]:
    """Score a single song against user preferences using the given weights.

    Args:
        user_prefs: dict with keys genre, mood, energy, and optionally
                    target_popularity and target_decade.
        song:       dict loaded from songs.csv.
        weights:    weight dict from SCORING_MODES; defaults to "balanced".

    Returns:
        (total_score, reasons_string)
    """
    if weights is None:
        weights = SCORING_MODES["balanced"]

    score = 0.0
    reasons = []

    # Primary signals (controlled by scoring mode weights)
    if song["genre"] == user_prefs["genre"]:
        pts = weights["genre"]
        score += pts
        reasons.append(f"genre match (+{pts})")

    if song["mood"] == user_prefs["mood"]:
        pts = weights["mood"]
        score += pts
        reasons.append(f"mood match (+{pts})")

    energy_score = round((1.0 - abs(song["energy"] - user_prefs["energy"])) * weights["energy"], 2)
    score += energy_score
    reasons.append(f"energy score (+{energy_score:.2f})")

    # Challenge 1: Popularity proximity — worth up to +0.5
    if "target_popularity" in user_prefs and user_prefs["target_popularity"] is not None and "popularity" in song:
        pop_score = round((1.0 - abs(song["popularity"] - user_prefs["target_popularity"]) / 100) * 0.5, 2)
        score += pop_score
        reasons.append(f"popularity score (+{pop_score:.2f})")

    # Challenge 1: Decade match — exact match worth +0.5
    if "target_decade" in user_prefs and user_prefs["target_decade"] is not None and "release_decade" in song:
        if song["release_decade"] == user_prefs["target_decade"]:
            score += 0.5
            reasons.append("decade match (+0.5)")

    return round(score, 2), ", ".join(reasons)


def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "balanced",
) -> List[Tuple[Dict, float, str]]:
    """Score every song using the chosen mode, sort descending, return top k.

    Args:
        user_prefs: user preference dict.
        songs:      list of song dicts from load_songs.
        k:          number of results to return.
        mode:       one of the keys in SCORING_MODES.

    Returns:
        List of (song_dict, score, reasons_string) tuples.
    """
    weights = SCORING_MODES.get(mode, SCORING_MODES["balanced"])
    scored = [(song, *score_song(user_prefs, song, weights)) for song in songs]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]


# ---------------------------------------------------------------------------
# OOP wrapper (used by tests)
# ---------------------------------------------------------------------------

class Recommender:
    """OOP wrapper around the recommendation logic, operating on Song dataclass objects."""

    def __init__(self, songs: List[Song], mode: str = "balanced"):
        self.songs = songs
        self.mode = mode

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects ranked by score for the given UserProfile."""
        weights = SCORING_MODES.get(self.mode, SCORING_MODES["balanced"])
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        if user.target_popularity is not None:
            user_prefs["target_popularity"] = user.target_popularity
        if user.target_decade is not None:
            user_prefs["target_decade"] = user.target_decade

        scored = []
        for song in self.songs:
            song_dict = {
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "popularity": song.popularity,
                "release_decade": song.release_decade,
            }
            score, _ = score_song(user_prefs, song_dict, weights)
            scored.append((score, song))
        return [song for _, song in sorted(scored, key=lambda x: x[0], reverse=True)[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language explanation of why this song was recommended."""
        weights = SCORING_MODES.get(self.mode, SCORING_MODES["balanced"])
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        if user.target_popularity is not None:
            user_prefs["target_popularity"] = user.target_popularity
        if user.target_decade is not None:
            user_prefs["target_decade"] = user.target_decade

        song_dict = {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "popularity": song.popularity,
            "release_decade": song.release_decade,
        }
        _, explanation = score_song(user_prefs, song_dict, weights)
        return explanation
