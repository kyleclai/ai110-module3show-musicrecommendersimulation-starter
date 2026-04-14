import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass


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


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


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
            songs.append(row)
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """Score a single song against user preferences; return (total_score, reasons_string)."""
    score = 0.0
    reasons = []

    if song["genre"] == user_prefs["genre"]:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"] == user_prefs["mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_score = round(1.0 - abs(song["energy"] - user_prefs["energy"]), 2)
    score += energy_score
    reasons.append(f"energy score (+{energy_score:.2f})")

    return round(score, 2), ", ".join(reasons)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score descending, and return the top k as (song, score, reasons) tuples."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]


class Recommender:
    """OOP wrapper around the recommendation logic, operating on Song dataclass objects."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects ranked by score for the given UserProfile."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        scored = []
        for song in self.songs:
            song_dict = {"genre": song.genre, "mood": song.mood, "energy": song.energy}
            score, _ = score_song(user_prefs, song_dict)
            scored.append((score, song))
        return [song for _, song in sorted(scored, key=lambda x: x[0], reverse=True)[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language explanation of why this song was recommended."""
        user_prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        song_dict = {"genre": song.genre, "mood": song.mood, "energy": song.energy}
        _, explanation = score_song(user_prefs, song_dict)
        return explanation
