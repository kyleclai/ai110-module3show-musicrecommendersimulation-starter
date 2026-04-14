"""
Command line runner for the Music Recommender Simulation.

Run from the project root:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs, score_song


def print_recommendations(songs, user_prefs, label, k=5, weights=None):
    """Print top-k recommendations for a given user profile."""
    print(f"\n{'=' * 55}")
    print(f"  Profile: {label}")
    print(f"  genre={user_prefs['genre']} | mood={user_prefs['mood']} | energy={user_prefs['energy']}")
    if weights:
        print(f"  weights: genre={weights['genre']} | mood={weights['mood']} | energy=proximity")
    print(f"{'=' * 55}")

    if weights:
        results = _recommend_with_weights(user_prefs, songs, weights, k)
    else:
        results = recommend_songs(user_prefs, songs, k)

    for rank, (song, score, explanation) in enumerate(results, start=1):
        print(f"  {rank}. {song['title']} by {song['artist']}")
        print(f"     Score : {score:.2f}")
        print(f"     Why   : {explanation}")
        print()


def _recommend_with_weights(user_prefs, songs, weights, k=5):
    """Score songs using custom weights for genre and mood matches."""
    scored = []
    for song in songs:
        score = 0.0
        reasons = []

        if song["genre"] == user_prefs["genre"]:
            score += weights["genre"]
            reasons.append(f"genre match (+{weights['genre']})")

        if song["mood"] == user_prefs["mood"]:
            score += weights["mood"]
            reasons.append(f"mood match (+{weights['mood']})")

        energy_score = round(1.0 - abs(song["energy"] - user_prefs["energy"]), 2)
        score += energy_score
        reasons.append(f"energy score (+{energy_score:.2f})")

        scored.append((song, round(score, 2), ", ".join(reasons)))

    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs.")

    # --- Standard profiles ---
    profiles = [
        ("Happy Pop",       {"genre": "pop",     "mood": "happy",     "energy": 0.8}),
        ("Chill Lofi",      {"genre": "lofi",    "mood": "chill",     "energy": 0.35}),
        ("Deep Rock",       {"genre": "rock",    "mood": "intense",   "energy": 0.9}),
        # Adversarial: high energy but peaceful mood — conflicting signals
        ("Adversarial EDM", {"genre": "edm",     "mood": "peaceful",  "energy": 0.95}),
    ]

    for label, prefs in profiles:
        print_recommendations(songs, prefs, label)

    # --- Experiment: weight shift ---
    # Default: genre=2.0, mood=1.0
    # Experiment: genre=1.0, mood=2.0  (double mood, halve genre)
    print(f"\n{'#' * 55}")
    print("  EXPERIMENT: Swap genre/mood weights")
    print("  Default  → genre +2.0, mood +1.0")
    print("  Modified → genre +1.0, mood +2.0")
    print(f"{'#' * 55}")

    exp_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    print_recommendations(songs, exp_prefs, "Happy Pop (default weights)")
    print_recommendations(
        songs, exp_prefs, "Happy Pop (mood-first weights)",
        weights={"genre": 1.0, "mood": 2.0}
    )


if __name__ == "__main__":
    main()
