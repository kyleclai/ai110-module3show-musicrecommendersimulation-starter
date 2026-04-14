# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder 1.0 suggests songs from a small catalog based on a user's preferred genre, mood, and energy level. It is designed for classroom exploration of how content-based recommendation systems work — not for use in a real product.

The system assumes the user can describe their taste with a single genre, a single mood label, and a target energy level between 0.0 and 1.0. It does not learn from listening history, does not adapt over time, and does not account for the fact that real musical taste is more complex than three attributes. It should not be used to make recommendations for real users or to draw conclusions about what music people "should" hear.

---

## 3. How the Model Works

Imagine you hand a friend a list of your three favorite things about music: your favorite genre (like pop or jazz), the mood you want (like happy or chill), and how energetic you want it to feel on a scale from calm to intense. Your friend then goes through every song in a catalog and gives each one a score based on how well it matches your preferences.

That is exactly what VibeFinder does. For each song, it checks whether the genre matches your favorite (worth 2 points), whether the mood matches (worth 1 point), and how close the song's energy level is to your target (worth up to 1 point — the closer, the more points). The maximum possible score is 4.0. After every song is scored, the list is sorted from highest to lowest, and the top results are returned along with an explanation of why each song ranked where it did.

The "energy score" is the most interesting part: instead of simply rewarding high-energy or low-energy songs, it rewards songs that are *close* to whatever energy level you asked for. A calm user gets credit for calm songs; a high-energy user gets credit for intense ones.

---

## 4. Data

The catalog contains 20 songs stored in `data/songs.csv`. The original starter file had 10 songs; 10 more were added to expand genre and mood coverage.

Genres represented: pop, lofi, rock, ambient, jazz, synthwave, indie pop, hip-hop, edm, country, classical, r&b, folk, metal, blues, reggae, electronic (17 total).

Moods represented: happy, chill, intense, relaxed, moody, focused, confident, energetic, nostalgic, melancholic, romantic, peaceful, aggressive, soulful, uplifting, dreamy (16 total).

Each song includes numeric features for energy (0.0–1.0), tempo in BPM, valence (musical positivity), danceability, and acousticness — though VibeFinder 1.0 only uses energy in its scoring. The other features exist in the data but are not currently factored into recommendations.

The dataset was constructed manually for classroom purposes. It does not reflect real streaming data, real listener behavior, or any demographic. Genres like lofi and pop have 3 songs each while most other genres have only 1, which creates an uneven distribution.

---

## 5. Strengths

VibeFinder works best when the user's preferred genre has multiple songs in the catalog. For the "Chill Lofi" profile (genre=lofi, mood=chill, energy=0.35), the top result scored a perfect 4.00 out of 4.00, and the top three results were all genuinely chill lofi tracks — the results matched musical intuition exactly.

The system is fully transparent. Every recommendation comes with a plain-language explanation of exactly which signals contributed to its score, which makes it easy to understand why a song was suggested and to spot when the logic is wrong. Unlike a neural network, there is no hidden behavior — you can trace every point back to a specific rule.

The scoring is also symmetric: it does not inherently favor high-energy or low-energy songs. A user who wants very quiet music (energy=0.2) and a user who wants very loud music (energy=0.95) both get the same quality of energy-based scoring, because the formula measures distance from the target rather than rewarding a particular direction.

---

## 6. Limitations and Bias

The genre weight (+2.0) is double the mood weight (+1.0), which means a genre match dominates the score even when the mood is completely wrong. A user who asks for "peaceful EDM" will receive an energetic EDM track at #1 simply because genre alignment outweighs the mood mismatch. This is a built-in structural bias toward genre over feel.

The catalog only has one rock song, one metal song, and one country song. Users with those genre preferences will see that single song at #1 and then get unrelated songs at #2–5 sorted purely by energy — the recommender cannot provide meaningful variety for underrepresented genres. This creates an unequal experience depending on which genre a user prefers.

The system has no memory and no personalization. Every run with the same profile produces the same result regardless of what the user has already heard. Real users eventually dislike repetition, but this system will keep recommending the same top songs indefinitely.

The energy score never goes negative — even a song with completely wrong energy gets a small positive score — which means every song contributes some noise to the ranking even when it should be excluded entirely.

---

## 7. Evaluation

Four user profiles were tested against the 20-song catalog:

- **Happy Pop** (genre=pop, mood=happy, energy=0.8) — top result was nearly perfect (3.98/4.00). Results matched musical intuition well.
- **Chill Lofi** (genre=lofi, mood=chill, energy=0.35) — produced a perfect 4.00/4.00 top result. The three lofi songs swept the top 3.
- **Deep Rock** (genre=rock, mood=intense, energy=0.9) — only one rock song exists, so positions #2–5 were filled by unrelated genres ranked purely by energy.
- **Adversarial EDM** (genre=edm, mood=peaceful, energy=0.95) — conflicting signals. The system surfaced an energetic EDM track at #1 (genre won) and a quiet folk song at #2 (the only peaceful track), with a score gap of 1.65 points between them. The system had no way to represent the contradiction.

One logic experiment was run: swapping genre weight (2.0→1.0) and mood weight (1.0→2.0) for the Happy Pop profile. The #2 and #3 results swapped — Rooftop Lights (indie pop/happy) rose above Gym Hero (pop/intense) because mood alignment became worth more than genre alignment. The #1 result was unchanged since it matched both signals regardless of weighting.

The two automated tests in `tests/test_recommender.py` both pass, confirming that the `Recommender` class correctly ranks a pop/happy song above a lofi/chill song for a pop/happy user profile, and that `explain_recommendation` returns a non-empty string.

---

## 8. Future Work

**Add a diversity penalty.** Right now the same artist or genre can appear multiple times in the top results. A simple rule — reduce the score of any song whose genre already appears in the top results — would force more variety into the recommendations and reduce the "filter bubble" effect.

**Use more song features in scoring.** The catalog already has valence, danceability, and acousticness for every song, but VibeFinder 1.0 ignores them. Adding a user preference for acousticness (does the user want live/acoustic or produced/electronic?) and incorporating it into the score would make recommendations much more nuanced, especially for profiles where energy alone is not enough to differentiate songs.

**Expand the catalog and balance genres.** Most genres in the current dataset have only one song. A real content-based recommender needs at least 5–10 songs per genre to provide meaningful variety. Doubling the catalog size and ensuring each genre has at least 3 songs would make the recommender significantly more useful across all profile types.

---

## 9. Personal Reflection

The most surprising thing about building this was how quickly a very simple set of rules starts to feel like a real recommendation. Three numbers — genre match, mood match, energy distance — are enough to produce results that often match your gut feeling about what you'd want to hear. It made me realize that "AI recommendation" doesn't always mean something mysterious or complex. A lot of what Spotify or YouTube does at its core is this same loop: score every candidate, sort by score, return the top results. The intelligence is mostly in the quality of the features and the size of the catalog, not in the math itself.

What changed how I think about real recommendation apps is the adversarial profile test. When I gave the system a contradictory preference — high energy AND peaceful mood — it had no way to handle it and just picked a winner (genre) and ignored the loser (mood). Real platforms face this constantly: a user who listens to both aggressive metal and quiet classical is genuinely hard to serve. The difference is that Spotify has thousands of features per song and millions of users to learn from, so it can find patterns that a three-rule system never could. Building this made the gap between "simple scoring" and "real personalization" feel very concrete.
