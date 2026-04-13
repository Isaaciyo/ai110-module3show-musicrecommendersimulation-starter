# Reflection: Profile Pair Comparisons

Each section below compares two profiles head-to-head — what changed between their top-5 outputs and why the difference makes sense given what each profile is actually testing.

---

## Pair 1: High-Energy Pop vs. Chill Lofi

**High-Energy Pop** pulls toward *Sunrise City* (pop/happy, energy 0.82) and *Gym Hero* (pop/intense, energy 0.93). Every top-5 pick has energy above 0.75 and acousticness below 0.40.

**Chill Lofi** pulls toward *Midnight Coding* and *Library Rain* — both lofi/chill songs with energy below 0.45 and acousticness above 0.70. The entire top-5 flips to the opposite end of the energy spectrum.

**Why it makes sense:** Energy is the highest-weighted feature (5.0 pts). These two profiles sit at opposite ends of the energy scale (0.85 vs. 0.38), so their preferred songs share almost no overlap. The genre and mood bonuses reinforce the separation further — "pop/happy" and "lofi/chill" are categorical opposites in this dataset. This is the expected behavior: the scorer correctly separates two very different listener types.

---

## Pair 2: Chill Lofi vs. Deep Intense Rock

**Chill Lofi** top-5 is dominated by soft, high-acousticness tracks (lofi, ambient, jazz). No track exceeds energy 0.42.

**Deep Intense Rock** top-5 is the mirror image — *Storm Runner* (rock/intense, energy 0.91) at #1, followed by *Iron Cathedral* (metal, energy 0.97) and *Gym Hero* (pop/intense, energy 0.93). Every pick has energy above 0.75 and acousticness below 0.12.

**Why it makes sense:** Both profiles have strong, internally consistent preferences. The rock profile's low target valence (0.35) also filters toward darker songs, which is why metal outranks pop here even though pop is better represented in the dataset. The combination of high energy + low valence is a narrow enough target that only rock and metal satisfy it simultaneously.

---

## Pair 3: High-Energy Pop vs. Deep Intense Rock

These two profiles share high energy targets (0.85 and 0.92) but diverge on valence (0.80 vs. 0.35) and mood (happy vs. intense).

**High-Energy Pop** top-5 includes *Sunrise City*, *Rooftop Lights*, and *Gym Hero* — all bright, positive-sounding tracks with valence above 0.75.

**Deep Intense Rock** top-5 includes *Storm Runner*, *Iron Cathedral*, and *Night Drive Loop* — darker songs with valence ranging from 0.31 to 0.49. *Sunrise City* doesn't appear anywhere in the rock top-5 despite being the pop profile's #1 pick.

**Why it makes sense:** With energy roughly equal between the two profiles, valence becomes the deciding factor in ranking. This is a good sign: it shows the scorer doesn't simply return "the loudest songs" when two profiles share high energy — the secondary features (valence, mood, genre) still differentiate the outputs meaningfully.

---

## Pair 4: High-Energy Pop vs. Conflicting Energy + Mood (adversarial)

**High-Energy Pop** scores *Sunrise City* at 11.66 — a near-perfect match on every dimension.

**Conflicting Energy + Mood** asks for energy 0.9 AND mood: melancholic. Its #1 result is *Storm Runner* (rock/intense) — a song the user's mood preference should disqualify.

**Why it makes sense (as a failure):** The scorer has no concept of "this preference contradicts that one." It adds up points independently. The melancholic mood bonus (+1.0) could only fire for *Autumn Sonata No. 3*, but that song's energy (0.24) is so far from the target (0.9) that it loses 3.8 energy points — far more than the mood bonus can recover. The system gets "tricked" because there is no song in the dataset that is simultaneously high-energy and melancholic. A real system would either warn the user about conflicting preferences or use a non-additive scoring model.

---

## Pair 5: Chill Lofi vs. Ghost Genre (adversarial)

**Chill Lofi** scores its #1 (*Midnight Coding*) at 11.66, with genre and mood bonuses both firing cleanly.

**Ghost Genre** (bossa nova, not in dataset) scores its #1 (*Coffee Shop Stories*) at 10.93 — almost as high, but the genre bonus never fires for any song.

**Why it makes sense:** "Bossa nova" shares acoustic, mid-tempo, relaxed characteristics with jazz. Because the scoring falls back entirely to numeric proximity (energy, valence, danceability, acousticness), it accidentally surfaces *Coffee Shop Stories* — the closest numeric neighbor to bossa nova in the catalog. The mood match (+1.0 for "relaxed") also fires for that song, partially compensating for the missing genre bonus. This shows that numeric features carry enough signal to produce a reasonable fallback recommendation even when categorical features fail entirely.

---

## Pair 6: Acoustic yet Max Energy vs. Ghost Genre (both adversarial)

**Acoustic + Max Energy** produces an internally contradictory signal. Its #1 (*Wildflower Road*, folk/romantic) scores 9.27 — relatively low compared to the standard profiles' scores of ~11.5. Energy tops out at 2.40/5.0 for that song because its energy (0.48) is far from the target (1.0). The scorer cannot find a song that satisfies both constraints simultaneously.

**Ghost Genre** still reaches 10.93 for its top pick — significantly higher than the Acoustic + Max Energy profile — even though a whole feature category is missing.

**Why it makes sense:** This comparison reveals that a *missing* feature (ghost genre) is less damaging than a *contradictory* feature pair (acoustic + max energy). When a category simply doesn't match, the system loses at most 0.5 genre points. When two numeric features pull in opposite directions, the system loses points on both simultaneously, suppressing the entire top-5. Contradiction is a harder problem for additive scorers than absence.
