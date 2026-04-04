# Reflection: Music Recommender Simulation

## Profile-Pair Comparisons

### EDM Gym Warrior vs. Intense Rock Lover

Both profiles target high energy (0.95 and 0.9) and share "intense" as their preferred mood. The key differentiator is genre. The EDM profile gets Bass Cathedral (edm, intense, energy 0.95) and Club Mirage (edm, happy, energy 0.88) at the top — both electronic, beat-driven tracks. The Rock profile gets Storm Runner (rock, intense, energy 0.91) and Neon Alley (rock, moody, energy 0.80) — guitar-driven, raw production. Even though both users want intensity, the genre weight (2.0 points) cleanly separates their recommendations into different sonic worlds. This makes sense: "intense EDM" and "intense rock" are fundamentally different listening experiences, and the system captures that.

### Chill Lofi Listener vs. Mellow Acoustic Soul

Both are low-energy listeners (0.4 and 0.35), but genre and the `likes_acoustic` flag split them apart. The Lofi listener gets Midnight Coding and Library Rain — electronic lo-fi beats with that signature tape-hiss texture. The Acoustic listener gets Rainy Window and Sunday Morning — stripped-down guitar and piano tracks. The `likes_acoustic` boolean adds 0.5 points for songs with acousticness > 0.7, which pushes genuinely acoustic tracks up for that profile. Without it, both profiles would converge on the same low-energy tracks regardless of production style. This shows that a single boolean preference can meaningfully change recommendations when the catalog has enough variety.

### Happy Pop Fan vs. EDM Gym Warrior

The Pop Fan (energy 0.8) and EDM Warrior (energy 0.95) both lean toward upbeat, high-energy music, but their top results barely overlap. Pop Fan gets Sunrise City (pop, happy) first, while EDM Warrior gets Bass Cathedral (edm, intense) first. The interesting overlap is in the middle of each list: Club Mirage (edm, happy) shows up at #3 for Pop Fan and #2 for EDM Warrior. This makes sense — Club Mirage is a happy EDM track that bridges both profiles. It scores well for Pop Fan because of mood match ("happy"), and for EDM Warrior because of genre match ("edm"). This is exactly the kind of crossover a real recommender should surface.

### Intense Rock Lover vs. Mellow Acoustic Soul

These are near-opposites: energy 0.9 vs. 0.35, genre rock vs. acoustic, likes_acoustic false vs. true. Their top-5 lists have zero overlap. Rock Lover gets Storm Runner, Neon Alley, Gym Hero, Bass Cathedral, Iron Crown — all high-energy, non-acoustic tracks. Acoustic Soul gets Rainy Window, Sunday Morning, Coffee Shop Stories, Desert Highway, Golden Hour — all low-energy, organic-sounding tracks. The complete separation validates that the scoring system can differentiate between fundamentally different taste profiles. The combination of genre weight, energy proximity, and acoustic preference creates enough distance to prevent any bleed between these two listener types.

### Happy Pop Fan vs. Chill Lofi Listener

Pop Fan wants energy 0.8, happy mood, non-acoustic. Lofi Listener wants energy 0.4, chill mood, acoustic. Their lists are entirely different. Pop Fan's top pick (Sunrise City, score 5.50) would score poorly for the Lofi Listener because of genre mismatch, mood mismatch, and a 0.42 energy gap. Meanwhile, Lofi Listener's top pick (Midnight Coding, score 5.59) would tank for Pop Fan due to the same misalignments in reverse. The energy gap alone (0.8 vs. 0.4) creates a 0.4-point swing in energy proximity scoring — but the genre and mood mismatches (3.5 combined points) are what really drive the separation.
