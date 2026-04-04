# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder suggests 5 songs from a small catalog based on a user's preferred genre, mood, energy level, and acoustic preference. It's a classroom simulation for exploring how content-based recommendation works — not intended for real users or production deployment. It assumes the user has a single fixed taste profile and works best for exploring how weighted scoring turns preferences into ranked results.

### Non-Intended Use

- **Not for production music streaming** — the 20-song catalog is too small for real discovery, and the scoring weights haven't been validated against actual user behavior.
- **Not for mental health or therapeutic playlists** — the system has no understanding of emotional context or wellbeing. Recommending "sad" music to someone who is sad could be harmful.
- **Not for commercial playlist curation** — no licensing, rights management, or artist compensation is considered.
- **Not for evaluating musical quality** — the score measures "fit to preferences," not whether a song is good. A perfect-scoring song could still be terrible.

---

## 3. How the Model Works

The system looks at each song in the catalog and asks: "How well does this song match what the user wants?" It checks six things:

1. **Genre** — Does the song's genre match the user's favorite? This is the biggest factor, worth 2 points.
2. **Mood** — Does the mood match? Worth 1.5 points.
3. **Energy** — How close is the song's energy level to what the user wants? A perfect match gets 1 point, and the score drops as the gap widens.
4. **Valence** — How close is the song's musical positivity to the user's energy target? Worth up to 0.5 points.
5. **Danceability** — Higher danceability gives a small bonus, up to 0.3 points.
6. **Acoustic preference** — If the user likes acoustic music and the song is acoustic, bonus 0.5 points. If they prefer electronic and the song is non-acoustic, bonus 0.3 points.

After scoring every song, the system sorts them from highest to lowest and returns the top 5. Each recommendation comes with an explanation showing exactly which features contributed to the score and by how much.

---

## 4. Data

The catalog contains **20 songs** in `data/songs.csv`. The starter had 10; I added 10 more to cover genres and moods that were missing.

**Genres represented**: pop, lofi, rock, ambient, jazz, synthwave, indie pop, edm, r&b, country, acoustic, metal

**Moods represented**: happy, chill, intense, relaxed, moody, focused, romantic, sad

The dataset is intentionally small. It reflects a narrow slice of musical taste — mostly Western genres, no hip-hop or Latin music, no non-English tracks. The numerical features (energy, valence, etc.) are invented values, not pulled from a real API like Spotify's audio features.

---

## 5. Strengths

- **Transparency**: Every recommendation comes with a breakdown of exactly why it scored the way it did. No black box.
- **Profile accuracy for clear preferences**: When a user has a strong, unambiguous taste (like "chill lofi"), the top results feel right — Midnight Coding and Library Rain consistently rank first for lofi listeners.
- **Simplicity**: The scoring logic is easy to understand, modify, and debug. You can trace any score back to specific feature matches.
- **Handles edge cases gracefully**: Contradictory profiles (high energy + sad mood) don't crash — the system just leans on the strongest available signal.

---

## 6. Limitations and Bias

- **Genre dominance**: At 2.0 points, genre is the single strongest signal. A mediocre pop song will outscore a perfect mood+energy match from a different genre. This creates filter bubbles by design.
- **Small catalog bias**: With only 20 songs, some genres have 1-2 representatives. If you prefer metal, you're getting Iron Crown every time regardless of other preferences.
- **No temporal context**: The system doesn't know if you're at the gym, studying, or driving. A real recommender would adjust based on context.
- **Western-centric data**: No hip-hop, reggaeton, K-pop, Afrobeats, or classical. Users with those preferences get nothing relevant.
- **Static taste model**: The UserProfile is a single snapshot. Real taste is multi-dimensional and shifts constantly.
- **Energy-valence coupling**: I use the user's target energy as the valence reference too, which assumes energetic users want positive music. That's not always true — high-energy angry music exists.

---

## 7. Evaluation

I tested with five user profiles:

| Profile | Top Result | Felt Right? |
|---------|-----------|-------------|
| Happy Pop Fan (energy 0.8) | Sunrise City (pop, happy) | Yes — exact genre+mood match |
| Chill Lofi Listener (energy 0.4) | Midnight Coding (lofi, chill) | Yes — classic lofi pick |
| Intense Rock Lover (energy 0.9) | Storm Runner (rock, intense) | Yes — nailed it |
| EDM Gym Warrior (energy 0.95) | Bass Cathedral (edm, intense) | Yes — high energy EDM |
| Mellow Acoustic Soul (energy 0.35) | Rainy Window (acoustic, sad) | Mostly — got acoustic right, but "sad" wasn't what I wanted for "relaxed" |

**EDM vs. Rock comparison**: Both profiles prefer "intense" mood, but genre separates them cleanly. The EDM profile gets Bass Cathedral and Club Mirage; the Rock profile gets Storm Runner and Neon Alley. This shows genre weight is doing its job for differentiation.

**Chill Lofi vs. Mellow Acoustic comparison**: Both are low-energy listeners, but the genre and acoustic preference splits them apart. The lofi user gets electronic lo-fi beats while the acoustic user gets guitar-driven tracks. The `likes_acoustic` boolean adds meaningful separation here.

**Surprise**: The "Mellow Acoustic Soul" profile ranked Rainy Window (mood: sad) above Sunday Morning (mood: happy) because Rainy Window had closer energy proximity (0.30 vs 0.45 target of 0.35) and higher acousticness (0.95 vs 0.93). The mood mismatch (sad vs relaxed) cost Sunday Morning the top spot. This shows that when mood doesn't match for either song, small numerical differences in energy and acousticness break the tie.

**Experiment — doubled energy weight**: Made recommendations too energy-focused. The Pop Fan started getting EDM tracks because they had similar energy. Genre identity matters more than the numbers suggest.

---

## 8. Future Work

- **Feedback loop**: Let users thumbs-up/down recommendations and adjust weights dynamically. Right now the weights are static.
- **Diversity injection**: Force variety in the top-k results — if the top 3 are all the same genre, swap one out for the next-highest different genre.
- **Context-aware profiles**: Support multiple taste modes per user (workout, study, commute) instead of a single flat profile.
- **Larger catalog**: 20 songs isn't enough. With 200+ songs and real Spotify audio features, the scoring would produce much more meaningful differentiation.
- **Tempo matching**: tempo_bpm is in the data but unused in scoring. Adding it would help differentiate within genres (fast rock vs. slow rock).

---

## 9. Personal Reflection

The most surprising thing was how much the weight tuning matters. The algorithm itself is trivially simple — add up points, sort, done. But changing genre from 2.0 to 1.0 completely changed the character of every recommendation. That made me realize that "the algorithm" in real recommenders isn't just the math — it's the policy decisions baked into the weights. When Spotify decides how much to weight popularity vs. relevance, they're making an editorial choice disguised as a technical one.

Building this also changed how I think about filter bubbles. My system literally cannot recommend outside your stated genre preference unless there's nothing else to show. That's by design, but it means a pop listener in this system would never discover that they might love jazz. Real recommenders face this same tension between giving users what they want and expanding their horizons.

Where human judgment still matters: the system can tell you that a song scored 5.4, but it can't tell you whether that song will make you feel something. The numbers capture similarity, not quality or emotional resonance. A human curator would know that "Rainy Window" on a sad day hits different than the math suggests.

**How AI tools shaped my process**: Copilot was genuinely helpful for two things: expanding the CSV dataset (it generated diverse songs in valid format much faster than manual entry) and suggesting the energy proximity formula. I originally planned to just check "high/medium/low" energy buckets, but Copilot suggested the continuous 1.0 - abs(gap) approach which produces much smoother scoring. Where I had to push back: Copilot suggested using cosine similarity across all numerical features, which would've been elegant but would've hidden the individual feature contributions. I kept the explicit per-feature scoring because the "reasons" output is what makes the system explainable — and explainability was the whole point.

**What I'd try next**: First, I'd connect to Spotify's audio features API so the numerical values are real instead of invented. Second, I'd add a diversity constraint — if the top 3 results are all the same genre, force the third slot to be a different genre. Third, I'd build a simple feedback loop where thumbs-up/down adjusts the weights over time, turning this from a static recommender into something that actually learns.
