"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}\n")

    # Taste profile: high-energy pop listener who loves happy, danceable tracks.
    user_prefs = {
        "favorite_genre":       "pop",    # preferred genre
        "favorite_mood":        "happy",  # preferred mood
        "target_energy":        0.85,     # high energy — upbeat and driving
        "target_valence":       0.80,     # very positive, feel-good
        "target_danceability":  0.82,     # strongly prefers danceable tracks
        "target_acousticness":  0.15,     # produced/electronic sound preferred
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("=" * 50)
    print("  TOP RECOMMENDATIONS")
    print("=" * 50)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']}  —  {song['artist']}")
        print(f"    Score : {score:.2f} / 10.0")
        print(f"    Why   : {explanation}")


if __name__ == "__main__":
    main()
