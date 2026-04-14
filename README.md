# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommenders like Spotify and TikTok use a mix of two main approaches. **Collaborative filtering** finds users with similar listening histories and assumes you'll like what they liked — it requires a large crowd of users to work well. **Content-based filtering** looks only at the attributes of the songs themselves (genre, mood, energy) and matches them to a user's stated taste profile — it works with a single user and no history. This simulation uses content-based filtering because it is transparent, explainable, and well-suited to a small catalog.

### Song Features

Each `Song` object uses these attributes from `data/songs.csv`:

| Feature | Description |
|---|---|
| `genre` | Categorical label (e.g., pop, lofi, rock, jazz) |
| `mood` | Categorical label (e.g., happy, chill, intense, moody) |
| `energy` | Float 0.0–1.0 — how energetic/loud the track feels |
| `tempo_bpm` | Beats per minute |
| `valence` | Float 0.0–1.0 — musical positivity |
| `danceability` | Float 0.0–1.0 — how suited to dancing |
| `acousticness` | Float 0.0–1.0 — how acoustic (vs. produced) it sounds |

### User Profile

A `UserProfile` stores:
- `favorite_genre` — the genre the user wants to match
- `favorite_mood` — the mood the user wants to match
- `target_energy` — a float 0.0–1.0 representing how intense they want the music

### Algorithm Recipe (Scoring Rule)

For each song in the catalog, the recommender calculates a score:

```
score = 0.0

if song.genre == user.favorite_genre  →  +2.0 pts
if song.mood  == user.favorite_mood   →  +1.0 pts
energy_score  = 1.0 - |song.energy - user.target_energy|  →  +0.0 to +1.0 pts

Total possible: 4.0 pts
```

Genre is weighted highest because it is the strongest coarse filter — a jazz fan will rarely enjoy metal regardless of mood. Energy uses a proximity formula so songs *close* to the target still earn partial credit.

### Ranking Rule

After scoring every song, the system sorts all results from highest to lowest score and returns the top K results. This two-step process (score first, rank second) is necessary because a score for one song means nothing without comparing it to all other scores.

### Potential Bias

This system may over-prioritize genre matches in a small catalog. If most songs share the same genre as the user's preference, variety in the results will be low regardless of mood or energy differences.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this


---

## 7. `model_card_template.md`

Combines reflection and model card framing from the Module 3 guidance. :contentReference[oaicite:2]{index=2}  

```markdown
# 🎧 Model Card - Music Recommender Simulation

## 1. Model Name

Give your recommender a name, for example:

> VibeFinder 1.0

---

## 2. Intended Use

- What is this system trying to do
- Who is it for

Example:

> This model suggests 3 to 5 songs from a small catalog based on a user's preferred genre, mood, and energy level. It is for classroom exploration only, not for real users.

---

## 3. How It Works (Short Explanation)

Describe your scoring logic in plain language.

- What features of each song does it consider
- What information about the user does it use
- How does it turn those into a number

Try to avoid code in this section, treat it like an explanation to a non programmer.

---

## 4. Data

Describe your dataset.

- How many songs are in `data/songs.csv`
- Did you add or remove any songs
- What kinds of genres or moods are represented
- Whose taste does this data mostly reflect

---

## 5. Strengths

Where does your recommender work well

You can think about:
- Situations where the top results "felt right"
- Particular user profiles it served well
- Simplicity or transparency benefits

---

## 6. Limitations and Bias

Where does your recommender struggle

Some prompts:
- Does it ignore some genres or moods
- Does it treat all users as if they have the same taste shape
- Is it biased toward high energy or one genre by default
- How could this be unfair if used in a real product

---

## 7. Evaluation

How did you check your system

Examples:
- You tried multiple user profiles and wrote down whether the results matched your expectations
- You compared your simulation to what a real app like Spotify or YouTube tends to recommend
- You wrote tests for your scoring logic

You do not need a numeric metric, but if you used one, explain what it measures.

---

## 8. Future Work

If you had more time, how would you improve this recommender

Examples:

- Add support for multiple users and "group vibe" recommendations
- Balance diversity of songs instead of always picking the closest match
- Use more features, like tempo ranges or lyric themes

---

## 9. Personal Reflection

A few sentences about what you learned:

- What surprised you about how your system behaved
- How did building this change how you think about real music recommenders
- Where do you think human judgment still matters, even if the model seems "smart"

