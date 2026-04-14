"""
Command line runner for the Music Recommender Simulation.

Run from the project root:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs.\n")

    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    print(f"User profile: genre={user_prefs['genre']} | mood={user_prefs['mood']} | energy={user_prefs['energy']}")
    print("-" * 55)
    print("Top 5 recommendations:\n")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"  {rank}. {song['title']} by {song['artist']}")
        print(f"     Score : {score:.2f} / 4.00")
        print(f"     Why   : {explanation}")
        print()


if __name__ == "__main__":
    main()
