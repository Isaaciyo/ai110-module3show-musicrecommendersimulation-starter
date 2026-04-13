"""
Command line runner for the Music Recommender Simulation.

Runs six user profiles through the recommender — three standard taste profiles
and three adversarial / edge-case profiles — and prints the top-5 results for
each so you can inspect whether the scoring logic behaves as expected.
"""

try:
    from .recommender import load_songs, recommend_songs
except ImportError:
    from recommender import load_songs, recommend_songs


# ---------------------------------------------------------------------------
# User profiles
# ---------------------------------------------------------------------------

PROFILES = [
    # ── Standard profiles ──────────────────────────────────────────────────

    {
        "name": "High-Energy Pop",
        "description": "Upbeat, danceable pop lover — always happy and moving.",
        "prefs": {
            "favorite_genre":      "pop",
            "favorite_mood":       "happy",
            "target_energy":       0.85,
            "target_valence":      0.80,
            "target_danceability": 0.82,
            "target_acousticness": 0.15,
        },
    },

    {
        "name": "Chill Lofi",
        "description": "Late-night study session vibes — low energy, warm acoustics.",
        "prefs": {
            "favorite_genre":      "lofi",
            "favorite_mood":       "chill",
            "target_energy":       0.38,
            "target_valence":      0.58,
            "target_danceability": 0.60,
            "target_acousticness": 0.75,
        },
    },

    {
        "name": "Deep Intense Rock",
        "description": "Heavy, driving rock — raw energy, low valence, electric sound.",
        "prefs": {
            "favorite_genre":      "rock",
            "favorite_mood":       "intense",
            "target_energy":       0.92,
            "target_valence":      0.35,
            "target_danceability": 0.60,
            "target_acousticness": 0.08,
        },
    },

    # ── Adversarial / edge-case profiles ───────────────────────────────────

    {
        "name": "ADVERSARIAL — Conflicting Energy + Mood",
        "description": (
            "energy: 0.9 (very high) but mood: melancholic. "
            "Does the scorer reward energy-matched loud tracks "
            "even though the desired mood is sad/quiet?"
        ),
        "prefs": {
            "favorite_genre":      "rock",
            "favorite_mood":       "melancholic",   # only 'Autumn Sonata No. 3' matches
            "target_energy":       0.90,            # pulls toward metal/edm
            "target_valence":      0.30,            # low — sad songs
            "target_danceability": 0.85,            # high — contradicts melancholic mood
            "target_acousticness": 0.10,
        },
    },

    {
        "name": "ADVERSARIAL — Acoustic yet Max Energy",
        "description": (
            "acousticness: 1.0 AND energy: 1.0. "
            "These features are strongly anti-correlated in the dataset — "
            "no song can score well on both simultaneously."
        ),
        "prefs": {
            "favorite_genre":      "folk",
            "favorite_mood":       "romantic",
            "target_energy":       1.00,   # maximum — pulls toward metal/edm
            "target_valence":      0.75,
            "target_danceability": 0.50,
            "target_acousticness": 1.00,   # maximum — pulls toward classical/lofi
        },
    },

    {
        "name": "ADVERSARIAL — Ghost Genre (not in dataset)",
        "description": (
            "favorite_genre: 'bossa nova' — a genre that does not appear in songs.csv. "
            "The genre-match bonus will never fire; scoring falls back entirely "
            "to numeric proximity. Does the ranker still surface sensible songs?"
        ),
        "prefs": {
            "favorite_genre":      "bossa nova",   # no songs have this genre
            "favorite_mood":       "relaxed",       # only 'Coffee Shop Stories' matches
            "target_energy":       0.45,
            "target_valence":      0.70,
            "target_danceability": 0.55,
            "target_acousticness": 0.80,
        },
    },
]


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_profile(profile: dict, songs: list) -> None:
    print("\n" + "=" * 60)
    print(f"  {profile['name']}")
    print(f"  {profile['description']}")
    print("=" * 60)

    recommendations = recommend_songs(profile["prefs"], songs, k=5)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Genre/Mood : {song['genre']} / {song['mood']}")
        print(f"       Score      : {score:.2f} / 10.0")
        print(f"       Why        : {explanation}")


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs from data/songs.csv")

    for profile in PROFILES:
        run_profile(profile, songs)

    print("\n" + "=" * 60)
    print("  All profiles complete.")
    print("=" * 60)


if __name__ == "__main__":
    main()
