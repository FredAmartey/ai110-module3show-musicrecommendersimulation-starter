import csv
from typing import List, Dict, Tuple, Optional
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

class Recommender:
    """OOP implementation of the recommendation logic."""
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def score_song(self, user: UserProfile, song: Song) -> Tuple[float, List[str]]:
        """Score a single song against a user profile, returning score and reasons."""
        score = 0.0
        reasons = []

        # Genre match: +2.0
        if song.genre.lower() == user.favorite_genre.lower():
            score += 2.0
            reasons.append(f"genre match: {song.genre} (+2.0)")

        # Mood match: +1.5
        if song.mood.lower() == user.favorite_mood.lower():
            score += 1.5
            reasons.append(f"mood match: {song.mood} (+1.5)")

        # Energy proximity: up to +1.0 (closer = higher)
        energy_gap = abs(song.energy - user.target_energy)
        energy_score = round(1.0 - energy_gap, 2)
        score += energy_score
        reasons.append(f"energy proximity: {energy_score:.2f} (gap {energy_gap:.2f})")

        # Valence proximity to energy target: up to +0.5
        valence_score = round(0.5 * (1.0 - abs(song.valence - user.target_energy)), 2)
        score += valence_score
        reasons.append(f"valence fit: +{valence_score:.2f}")

        # Danceability bonus: up to +0.3
        dance_score = round(0.3 * song.danceability, 2)
        score += dance_score
        reasons.append(f"danceability: +{dance_score:.2f}")

        # Acoustic preference: +0.5 if user likes acoustic and song is acoustic
        if user.likes_acoustic and song.acousticness > 0.7:
            score += 0.5
            reasons.append("acoustic match (+0.5)")
        elif not user.likes_acoustic and song.acousticness < 0.3:
            score += 0.3
            reasons.append("non-acoustic fit (+0.3)")

        return round(score, 2), reasons

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return top-k songs ranked by score for this user."""
        scored = [(song, self.score_song(user, song)) for song in self.songs]
        scored.sort(key=lambda x: x[1][0], reverse=True)
        return [song for song, _ in scored[:k]]

    def recommend_with_scores(self, user: UserProfile, k: int = 5) -> List[Tuple[Song, float, List[str]]]:
        """Return top-k songs with scores and reasons."""
        scored = []
        for song in self.songs:
            song_score, reasons = self.score_song(user, song)
            scored.append((song, song_score, reasons))
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Generate a human-readable explanation for why a song was recommended."""
        _, reasons = self.score_song(user, song)
        return "; ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dictionaries."""
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
    """Score a single song against user preferences, returning score and explanation."""
    score = 0.0
    reasons = []

    # Genre match: +2.0
    if song.get("genre", "").lower() == user_prefs.get("genre", "").lower():
        score += 2.0
        reasons.append(f"genre match: {song['genre']} (+2.0)")

    # Mood match: +1.5
    if song.get("mood", "").lower() == user_prefs.get("mood", "").lower():
        score += 1.5
        reasons.append(f"mood match: {song['mood']} (+1.5)")

    # Energy proximity: up to +1.0
    if "energy" in user_prefs and "energy" in song:
        energy_gap = abs(float(song["energy"]) - float(user_prefs["energy"]))
        energy_score = round(1.0 - energy_gap, 2)
        score += energy_score
        reasons.append(f"energy proximity: {energy_score:.2f} (gap {energy_gap:.2f})")

    # Valence proximity: up to +0.5
    if "energy" in user_prefs and "valence" in song:
        valence_score = round(0.5 * (1.0 - abs(float(song["valence"]) - float(user_prefs["energy"]))), 2)
        score += valence_score
        reasons.append(f"valence fit: +{valence_score:.2f}")

    # Danceability bonus: up to +0.3
    if "danceability" in song:
        dance_score = round(0.3 * float(song["danceability"]), 2)
        score += dance_score
        reasons.append(f"danceability: +{dance_score:.2f}")

    # Acoustic preference
    if user_prefs.get("likes_acoustic") and float(song.get("acousticness", 0)) > 0.7:
        score += 0.5
        reasons.append("acoustic match (+0.5)")
    elif not user_prefs.get("likes_acoustic") and float(song.get("acousticness", 0)) < 0.3:
        score += 0.3
        reasons.append("non-acoustic fit (+0.3)")

    return round(score, 2), "; ".join(reasons)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Rank all songs by score and return the top k recommendations."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
