import os
import pytest
from src.recommender import (
    Song, UserProfile, Recommender,
    load_songs, score_song, recommend_songs,
)

# ── Fixtures ─────────────────────────────────────────────────

@pytest.fixture
def sample_songs():
    return [
        Song(1, "Test Pop Track", "Artist A", "pop", "happy", 0.8, 120, 0.9, 0.8, 0.2),
        Song(2, "Chill Lofi Loop", "Artist B", "lofi", "chill", 0.4, 80, 0.6, 0.5, 0.9),
        Song(3, "Hard Rock Hit", "Artist C", "rock", "intense", 0.92, 150, 0.45, 0.65, 0.1),
        Song(4, "Ambient Drift", "Artist D", "ambient", "chill", 0.25, 60, 0.6, 0.4, 0.95),
        Song(5, "EDM Banger", "Artist E", "edm", "intense", 0.95, 140, 0.7, 0.9, 0.05),
    ]

@pytest.fixture
def pop_user():
    return UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.8, likes_acoustic=False)

@pytest.fixture
def lofi_user():
    return UserProfile(favorite_genre="lofi", favorite_mood="chill", target_energy=0.4, likes_acoustic=True)

@pytest.fixture
def rock_user():
    return UserProfile(favorite_genre="rock", favorite_mood="intense", target_energy=0.9, likes_acoustic=False)

def make_small_recommender():
    songs = [
        Song(1, "Test Pop Track", "Test Artist", "pop", "happy", 0.8, 120, 0.9, 0.8, 0.2),
        Song(2, "Chill Lofi Loop", "Test Artist", "lofi", "chill", 0.4, 80, 0.6, 0.5, 0.9),
    ]
    return Recommender(songs)


# ── OOP Recommender Tests ────────────────────────────────────

class TestRecommenderOOP:
    def test_recommend_returns_correct_count(self, sample_songs, pop_user):
        rec = Recommender(sample_songs)
        results = rec.recommend(pop_user, k=3)
        assert len(results) == 3

    def test_recommend_returns_songs_sorted_by_score(self):
        user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.8, likes_acoustic=False)
        rec = make_small_recommender()
        results = rec.recommend(user, k=2)
        assert len(results) == 2
        assert results[0].genre == "pop"
        assert results[0].mood == "happy"

    def test_pop_user_gets_pop_first(self, sample_songs, pop_user):
        rec = Recommender(sample_songs)
        results = rec.recommend(pop_user, k=1)
        assert results[0].genre == "pop"

    def test_lofi_user_gets_lofi_first(self, sample_songs, lofi_user):
        rec = Recommender(sample_songs)
        results = rec.recommend(lofi_user, k=1)
        assert results[0].genre == "lofi"

    def test_rock_user_gets_rock_first(self, sample_songs, rock_user):
        rec = Recommender(sample_songs)
        results = rec.recommend(rock_user, k=1)
        assert results[0].genre == "rock"

    def test_explain_recommendation_returns_non_empty_string(self):
        user = UserProfile(favorite_genre="pop", favorite_mood="happy", target_energy=0.8, likes_acoustic=False)
        rec = make_small_recommender()
        explanation = rec.explain_recommendation(user, rec.songs[0])
        assert isinstance(explanation, str)
        assert explanation.strip() != ""

    def test_explanation_mentions_genre_match(self, sample_songs, pop_user):
        rec = Recommender(sample_songs)
        explanation = rec.explain_recommendation(pop_user, sample_songs[0])
        assert "genre match" in explanation

    def test_score_song_returns_tuple(self, sample_songs, pop_user):
        rec = Recommender(sample_songs)
        result = rec.score_song(pop_user, sample_songs[0])
        assert isinstance(result, tuple)
        assert isinstance(result[0], float)
        assert isinstance(result[1], list)

    def test_acoustic_user_prefers_acoustic(self, sample_songs, lofi_user):
        rec = Recommender(sample_songs)
        # Ambient Drift has acousticness=0.95
        _, reasons_ambient = rec.score_song(lofi_user, sample_songs[3])
        assert any("acoustic match" in r for r in reasons_ambient)

    def test_recommend_with_scores_returns_reasons(self, sample_songs, pop_user):
        rec = Recommender(sample_songs)
        results = rec.recommend_with_scores(pop_user, k=2)
        assert len(results) == 2
        song, score, reasons = results[0]
        assert score > 0
        assert len(reasons) > 0


# ── Functional API Tests ─────────────────────────────────────

class TestFunctionalAPI:
    def test_load_songs_returns_list(self):
        csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")
        songs = load_songs(csv_path)
        assert isinstance(songs, list)
        assert len(songs) == 20

    def test_load_songs_converts_numeric_types(self):
        csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")
        songs = load_songs(csv_path)
        first = songs[0]
        assert isinstance(first["energy"], float)
        assert isinstance(first["tempo_bpm"], float)
        assert isinstance(first["id"], int)

    def test_score_song_returns_score_and_explanation(self):
        song = {"genre": "pop", "mood": "happy", "energy": 0.8, "valence": 0.9, "danceability": 0.8, "acousticness": 0.2}
        prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
        score, explanation = score_song(prefs, song)
        assert score > 0
        assert "genre match" in explanation

    def test_genre_match_adds_two_points(self):
        song = {"genre": "pop", "mood": "sad", "energy": 0.5, "valence": 0.5, "danceability": 0.5, "acousticness": 0.5}
        prefs_match = {"genre": "pop", "mood": "angry", "energy": 0.5}
        prefs_no_match = {"genre": "rock", "mood": "angry", "energy": 0.5}
        score_match, _ = score_song(prefs_match, song)
        score_no_match, _ = score_song(prefs_no_match, song)
        assert score_match - score_no_match == pytest.approx(2.0, abs=0.01)

    def test_mood_match_adds_points(self):
        song = {"genre": "jazz", "mood": "chill", "energy": 0.5, "valence": 0.5, "danceability": 0.5, "acousticness": 0.5}
        prefs_match = {"genre": "rock", "mood": "chill", "energy": 0.5}
        prefs_no_match = {"genre": "rock", "mood": "intense", "energy": 0.5}
        score_match, _ = score_song(prefs_match, song)
        score_no_match, _ = score_song(prefs_no_match, song)
        assert score_match - score_no_match == pytest.approx(1.5, abs=0.01)

    def test_recommend_songs_returns_sorted(self):
        csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")
        songs = load_songs(csv_path)
        prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
        results = recommend_songs(prefs, songs, k=5)
        scores = [score for _, score, _ in results]
        assert scores == sorted(scores, reverse=True)

    def test_recommend_songs_respects_k(self):
        csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "songs.csv")
        songs = load_songs(csv_path)
        prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
        results = recommend_songs(prefs, songs, k=3)
        assert len(results) == 3

    def test_energy_proximity_rewards_closeness(self):
        song_close = {"genre": "jazz", "mood": "sad", "energy": 0.81, "valence": 0.5, "danceability": 0.5, "acousticness": 0.5}
        song_far = {"genre": "jazz", "mood": "sad", "energy": 0.2, "valence": 0.5, "danceability": 0.5, "acousticness": 0.5}
        prefs = {"genre": "rock", "mood": "angry", "energy": 0.8}
        score_close, _ = score_song(prefs, song_close)
        score_far, _ = score_song(prefs, song_far)
        assert score_close > score_far

    def test_empty_catalog(self):
        prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
        results = recommend_songs(prefs, [], k=5)
        assert results == []
