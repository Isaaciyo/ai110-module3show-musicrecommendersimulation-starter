# Model Card: Music Recommender Simulation

---

## 1. Model Name

**VibeMatch 1.0**

A score-based music recommender that matches songs to a listener's taste profile.

---

## 2. Goal / Task

VibeMatch suggests songs that fit how you want to feel and what kind of music you like.

You tell it your favorite genre, your favorite mood, and how energetic, positive, danceable, or acoustic you want a song to be. It scores every song in the catalog against those preferences and returns the top 5.

This is a classroom simulation. It is not connected to any real streaming service.

---

## 3. Data Used

The catalog has **18 songs** stored in a CSV file.

Each song has these fields:
- **Title and artist** — who made it
- **Genre** — for example: pop, lofi, rock, jazz, metal, edm
- **Mood** — for example: happy, chill, intense, melancholic, romantic
- **Energy** — a number from 0 to 1 (0 = very calm, 1 = very intense)
- **Valence** — a number from 0 to 1 (0 = sad or dark, 1 = happy and bright)
- **Danceability** — a number from 0 to 1 (how easy it is to dance to)
- **Acousticness** — a number from 0 to 1 (0 = electronic/produced, 1 = acoustic/natural)
- **Tempo** — beats per minute

**Limits of the data:**
- 18 songs is tiny. A real recommender uses millions.
- 15 out of 15 unique genres appear only once or twice. Lofi has 3 songs; most genres have 1.
- Some musical styles are missing entirely — no classical-crossover, no R&B subgenres, no K-pop, no Latin.
- All data was hand-crafted for this simulation, so the numbers are approximate, not measured from real audio.

---

## 4. Algorithm Summary

VibeMatch uses a **point-based scoring system**. Every song gets a score out of 12 points.

Here is how the points are calculated:

**Numeric features** — the system measures how close each song is to your target on a 0–1 scale. The closer the song is to your preference, the more points it gets.

| Feature | Max points |
|---|---|
| Energy match | 5.0 |
| Valence (positivity) match | 2.0 |
| Danceability match | 2.0 |
| Acousticness match | 1.5 |

**Categorical bonuses** — these fire only if the song is an exact match.

| Feature | Bonus points |
|---|---|
| Genre matches your favorite | +0.5 |
| Mood matches your favorite | +1.0 |

The song with the highest total score is recommended first.

No machine learning is used. The weights were set by hand and adjusted during experiments.

---

## 5. Strengths

The system works well when your preferences point clearly in one direction.

**High-energy pop listeners** get great results. Songs like *Sunrise City* (pop/happy) score near-perfect because every number lines up and the genre and mood bonuses both fire.

**Lofi and chill listeners** also do well. The catalog has three lofi songs, so the system has real options to choose from.

**The scoring explanation is readable.** For every recommendation, the system tells you exactly which features contributed and how many points each one added. That makes it easy to understand *why* a song ranked where it did.

**Graceful fallback.** When a genre doesn't exist in the catalog at all, the system doesn't crash — it falls back to numeric similarity and still surfaces reasonable songs.

---

## 6. Limitations and Bias

**Energy dominates everything.**

Energy is worth 5 out of 12 points — about 42% of the total score. That means a song can outscore a better match just by having the right energy level. During testing, a metal song ranked above a folk song for a user who explicitly asked for acoustic, romantic music — because the metal song's energy was closer to the target.

**Some genres are almost invisible.**

13 out of 15 genres appear in only one song. A lofi listener can receive the genre bonus up to 3 times across 18 songs. A jazz or reggae listener can only receive it once. This means the system quietly rewards popular genres and ignores niche ones.

**Mood can get overruled by numbers.**

If your favorite mood only appears in one song and that song's other numbers don't match your preferences, the mood bonus isn't enough to push it into your top 5. A user who asked for melancholic songs never saw the only melancholic song in their results, because it was too calm for their high-energy target.

**Conflicting preferences confuse the scorer.**

The system adds up points independently. It has no way to detect when two preferences contradict each other. Asking for "maximum energy AND maximum acousticness" produces low scores across the board because no song can satisfy both at once — but the system doesn't warn you about this.

**The scoring scale is no longer 0–10.**

After the weight-shift experiment, the maximum possible score is 12.0. Many songs score above 10. The "out of 10" framing in the output is now misleading.

---

## 7. Evaluation Process

Six user profiles were tested against all 18 songs.

**Standard profiles** (designed to work well):
- **High-Energy Pop** — upbeat, danceable pop with happy mood
- **Chill Lofi** — low energy, acoustic, chill mood
- **Deep Intense Rock** — high energy, dark valence, intense mood

**Adversarial profiles** (designed to expose weaknesses):
- **Conflicting Energy + Mood** — energy 0.9 (loud) paired with mood: melancholic (quiet/sad)
- **Acoustic yet Max Energy** — acousticness 1.0 and energy 1.0 at the same time
- **Ghost Genre** — favorite genre set to "bossa nova," which has zero songs in the catalog

**What was checked:**
For standard profiles, the expected #1 song was known in advance. The test was whether the system ranked it first by a clear margin. For adversarial profiles, the goal was to see *how* it failed, not whether it failed.

**What was surprising:**
The melancholic profile never surfaced the only melancholic song in the top 5 — it was beaten by loud rock tracks because energy points outweighed the mood bonus. The ghost genre profile accidentally returned a very sensible jazz song as its #1 pick, even though the genre bonus never fired.

**Weight-shift experiment:**
Energy weight was doubled (2.5 → 5.0) and genre bonus was halved (1.0 → 0.5). Standard profile rankings barely changed. Adversarial profiles got worse — metal songs started appearing for users who wanted acoustic folk.

---

## 8. Intended Use and Non-Intended Use

**This system is intended for:**
- Classroom exploration of how recommender systems work
- Learning how scoring weights affect recommendation quality
- Experimenting with user profiles to understand bias and trade-offs

**This system is NOT intended for:**
- Real music discovery or deployment in a product
- Recommending music to actual users in a meaningful way
- Any situation where fairness, diversity, or personalization actually matter
- Replacing tools like Spotify, Apple Music, or any real recommendation engine

The catalog is too small and the scoring rules are too simple for real use. The weights were tuned by hand during experiments, not trained on real listener data.

---

## 9. Ideas for Improvement

**1. Normalize scores by genre availability.**
A genre that appears 3 times in the catalog should not have 3x the bonus opportunity of a genre that appears once. One fix: divide the genre bonus by the number of songs in that genre, so rare genres are not penalized.

**2. Let the user set their own weights.**
Right now, energy always counts more than mood. But some listeners care mostly about mood and barely care about energy. A better system would ask: "Which of these matters most to you?" and adjust the weights accordingly.

**3. Add a diversity rule.**
The top 5 results often come from 2–3 similar songs that cluster around the same genre. A simple fix would be to prevent any single genre from appearing more than twice in the top 5, so the recommendations feel less repetitive.

---

## 10. Personal Reflection

**Biggest learning moment**

My biggest learning moment was realizing that the weights matter more than the logic.

The scoring formula itself is simple — just measure how close each song is to what you asked for, add up the points. But when I doubled the energy weight, the whole system changed personality. Songs I never expected started showing up. Songs that felt right stopped appearing.

That one number change taught me more about recommender systems than reading about them ever did.

**How AI tools helped — and when I had to double-check**

AI tools helped me move fast. I used them to design adversarial profiles, apply weight changes to the code, and identify biases in the scoring logic. Things that would have taken me an hour to think through on my own got done in minutes.

But I had to double-check the math. When the agent said "the new max score is 12.0," I verified it by hand before trusting it. The calculation was right — but I wouldn't have caught an error if I hadn't checked. AI tools are great at suggesting. They still need a human to confirm.

**What surprised me about simple algorithms**

I was surprised that 30 lines of scoring logic could produce results that actually feel like recommendations.

When *Sunrise City* came back as #1 for the High-Energy Pop profile, it felt correct. It wasn't just a high score — it genuinely matched the vibe I had in mind. The system had no taste, no ears, and no idea what music is. It just added up proximity scores. And somehow it worked.

That moment made me understand why simple rule-based systems stuck around for so long before machine learning took over. If your features are good and your weights are reasonable, even a basic formula can feel surprisingly smart.

**What I'd try next**

First, I'd let users rank their own priorities. Not everyone cares about energy the most. Some people pick songs entirely by mood. The system should ask.

Second, I'd add a diversity rule. Right now the top 5 can be nearly identical songs. A real recommendation should surprise you at least once.

Third, I'd expand the catalog to a few hundred songs. Most of the bias problems I found came from having only 18 songs — one per genre is not enough data for any pattern to emerge fairly.
