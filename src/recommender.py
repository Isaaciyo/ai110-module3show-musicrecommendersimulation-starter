from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read a songs CSV and return a list of dicts with typed numeric fields."""
    import csv
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user preferences; return (score_out_of_10, reasons_list)."""
    score = 0.0
    reasons = []

    # --- Tier 1: numeric proximity scores (max points shown per feature) ---
    numeric_features = [
        ("energy",        "target_energy",        2.5),
        ("valence",       "target_valence",        2.0),
        ("danceability",  "target_danceability",   2.0),
        ("acousticness",  "target_acousticness",   1.5),
    ]

    for song_key, pref_key, max_points in numeric_features:
        if pref_key in user_prefs:
            proximity = 1.0 - abs(song[song_key] - user_prefs[pref_key])
            points = max_points * proximity
            score += points
            reasons.append(f"{song_key} fit (+{points:.2f}/{max_points})")

    # --- Tier 2: categorical match scores ---
    if song["genre"] == user_prefs.get("favorite_genre"):
        score += 1.0
        reasons.append("genre match (+1.0)")

    if song["mood"] == user_prefs.get("favorite_mood"):
        score += 1.0
        reasons.append("mood match (+1.0)")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score every song and return the top-k as (song, score, explanation) tuples."""
    scored = [
        (song, score, ", ".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
