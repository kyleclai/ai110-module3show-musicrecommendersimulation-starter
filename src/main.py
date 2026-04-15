"""
Command line runner for the Music Recommender Simulation.

Run from the project root:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs, max_possible_score, SCORING_MODES


def print_recommendations(songs, user_prefs, label, mode="balanced", k=5):
    """Print top-k recommendations for a profile under a given scoring mode."""
    max_pts = max_possible_score(mode, user_prefs)
    print(f"\n{'=' * 60}")
    print(f"  {label}  [{mode}]")
    print(f"  genre={user_prefs['genre']} | mood={user_prefs['mood']} | energy={user_prefs['energy']}", end="")
    if "target_popularity" in user_prefs:
        print(f" | popularity≈{user_prefs['target_popularity']}", end="")
    if "target_decade" in user_prefs:
        print(f" | decade={user_prefs['target_decade']}", end="")
    print(f"\n  max possible score: {max_pts:.1f}")
    print(f"{'=' * 60}")

    results = recommend_songs(user_prefs, songs, k=k, mode=mode)
    for rank, (song, score, explanation) in enumerate(results, start=1):
        print(f"  {rank}. {song['title']} by {song['artist']}")
        print(f"     Score : {score:.2f} / {max_pts:.1f}")
        print(f"     Why   : {explanation}")
        print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs.\n")

    # -----------------------------------------------------------------------
    # Section 1: Challenge 1 — Advanced features (popularity + decade)
    # Compare the same profile with and without the new signals
    # -----------------------------------------------------------------------
    print("=" * 60)
    print("  CHALLENGE 1: Advanced Song Features")
    print("  popularity (0-100 proximity) and decade match now score")
    print("=" * 60)

    base_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
    advanced_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "target_popularity": 80,   # prefer mainstream/popular songs
        "target_decade": 2020,     # prefer recent releases
    }

    print_recommendations(songs, base_prefs,     "Happy Pop (no bonus features)", mode="balanced")
    print_recommendations(songs, advanced_prefs, "Happy Pop (popularity + decade)", mode="balanced")

    # -----------------------------------------------------------------------
    # Section 2: Challenge 2 — Scoring Modes
    # Same profile, all four modes side-by-side to show weight impact
    # -----------------------------------------------------------------------
    print("\n" + "#" * 60)
    print("  CHALLENGE 2: Scoring Modes")
    print("  Available modes:", ", ".join(SCORING_MODES.keys()))
    print("#" * 60)

    mode_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "target_popularity": 80,
        "target_decade": 2020,
    }

    for mode in SCORING_MODES:
        print_recommendations(songs, mode_prefs, "Happy Pop", mode=mode, k=3)


if __name__ == "__main__":
    main()
