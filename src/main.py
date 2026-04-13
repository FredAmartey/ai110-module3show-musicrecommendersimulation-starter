"""
Command line runner for the Music Recommender Simulation.

Runs multiple user profiles through the recommender and prints
ranked results with scores and explanations.
"""

import os
from recommender import load_songs, recommend_songs


# ── User Profiles ────────────────────────────────────────────

PROFILES = {
    "Happy Pop Fan": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    },
    "Chill Lofi Listener": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.4,
        "likes_acoustic": True,
    },
    "Intense Rock Lover": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9,
        "likes_acoustic": False,
    },
    "EDM Gym Warrior": {
        "genre": "edm",
        "mood": "intense",
        "energy": 0.95,
        "likes_acoustic": False,
    },
    "Mellow Acoustic Soul": {
        "genre": "acoustic",
        "mood": "relaxed",
        "energy": 0.35,
        "likes_acoustic": True,
    },
    "Contradiction Test": {
        "genre": "pop",
        "mood": "sad",
        "energy": 0.95,
        "likes_acoustic": True,
    },
}


# ── Experiment toggle ────────────────────────────────────────
# Flip this to True to run the weight-shift experiment
RUN_EXPERIMENT = False


def print_recommendations(profile_name, user_prefs, songs, k=5):
    """Print formatted recommendations for a single profile."""
    print(f"\n{'='*60}")
    print(f"  Profile: {profile_name}")
    print(f"  Prefs: genre={user_prefs['genre']}, mood={user_prefs['mood']}, "
          f"energy={user_prefs['energy']}, acoustic={user_prefs.get('likes_acoustic', False)}")
    print(f"{'='*60}")

    results = recommend_songs(user_prefs, songs, k=k)

    for rank, (song, score, explanation) in enumerate(results, 1):
        print(f"\n  #{rank}  {song['title']} by {song['artist']}")
        print(f"       Genre: {song['genre']} | Mood: {song['mood']} | "
              f"Energy: {song['energy']}")
        print(f"       Score: {score:.2f}")
        print(f"       Why:   {explanation}")

    print()


def main():
    csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")
    songs = load_songs(csv_path)
    print(f"Loaded {len(songs)} songs from catalog.\n")

    for name, prefs in PROFILES.items():
        print_recommendations(name, prefs, songs)

    if RUN_EXPERIMENT:
        print("\n" + "#"*60)
        print("  EXPERIMENT: doubled energy weight, halved genre weight")
        print("#"*60)
        # The experiment modifies weights inside score_song — see Phase 4
        # For now we just re-run to show side-by-side comparison
        for name, prefs in PROFILES.items():
            print_recommendations(name, prefs, songs)


if __name__ == "__main__":
    main()
