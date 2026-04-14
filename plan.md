# Music Recommender Simulation — Project Plan

**Estimated total time:** ~4 hours  
**Goal:** Build a weighted-score, content-based music recommender in Python, evaluate its behavior, and document it with a Model Card.

---

## Phase 1: Understanding the Problem (~25 min)

**Goal:** Learn how real recommenders work and decide what your system will do.

### Tasks

- [ ] Fork and clone the repo, open in VS Code.
- [ ] Use Copilot Chat to research the difference between:
  - **Collaborative filtering** — uses other users' behavior (e.g., "people like you also liked…")
  - **Content-based filtering** — uses song attributes (e.g., genre, mood, energy) — this is what we're building
- [ ] Review `data/songs.csv` to understand available features:
  - `genre`, `mood`, `energy` (0.0–1.0), `tempo_bpm`, `valence`, `danceability`, `acousticness`
- [ ] Decide your "Algorithm Recipe" — the scoring rules your system will use:
  - Example starting point: `+2.0` for genre match, `+1.0` for mood match, proximity score for energy
  - Decide what "closer to target energy" means mathematically (e.g., `1.0 - abs(song_energy - target_energy)`)
- [ ] Update `README.md` → **How The System Works** section with:
  - A plain-language explanation of how real recommenders work
  - The features your `Song` and `UserProfile` will use

**Checkpoint:** You have a written concept sketch — what data flows in, how scoring works, what comes out.

---

## Phase 2: Designing the Simulation (~45 min)

**Goal:** Expand the dataset, define a user profile, and lock in your scoring logic before writing code.

### Tasks

- [ ] Open `data/songs.csv` (currently 10 songs) and add 5–10 more with diverse genres/moods using Copilot Chat.
  - Maintain the same headers: `id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness`
  - Consider adding genres not yet present: e.g., `edm`, `classical`, `hip-hop`, `country`
- [ ] Define your starter user profile dictionary (used in `src/main.py`):
  ```python
  user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
  ```
  - Use Copilot Inline Chat to critique whether your profile can distinguish between "intense rock" and "chill lofi"
- [ ] Finalize scoring weights:

  | Signal | Points |
  |---|---|
  | Genre match | +2.0 |
  | Mood match | +1.0 |
  | Energy proximity | `1.0 - abs(song_energy - target_energy)` |

- [ ] Ask Copilot to generate a Mermaid.js flowchart of: `User Prefs → Score Each Song → Sort → Top K Results`
- [ ] Document your finalized recipe in `README.md` → **How The System Works**, including any expected biases (e.g., "Genre weight may dominate small catalogs")

**Checkpoint:** Expanded CSV, defined user profile, and locked-in scoring rules — ready to implement.

---

## Phase 3: Implementation (~90 min)

**Goal:** Make `src/recommender.py` fully functional — load songs, score them, rank them, explain results.

### Key files
- `src/recommender.py` — core logic (stubs already exist for `load_songs`, `recommend_songs`, `Recommender.recommend`, `Recommender.explain_recommendation`)
- `src/main.py` — runner that calls `load_songs` and `recommend_songs`
- `tests/test_recommender.py` — existing tests that use the `Song`, `UserProfile`, and `Recommender` classes

### Tasks

- [ ] **Implement `load_songs(csv_path)`** in `src/recommender.py`
  - Use Python's `csv` module (no pandas needed)
  - Cast numeric fields to `float`: `energy`, `tempo_bpm`, `valence`, `danceability`, `acousticness`
  - Cast `id` to `int`
  - Return a `List[Dict]`
  - Verify: `python -m src.main` should print the song count

- [ ] **Add a `score_song(user_prefs, song)` function** that returns `(float, str)`:
  - Award points per your Phase 2 recipe
  - Build a human-readable reasons string, e.g. `"genre match (+2.0), mood match (+1.0), energy score (+0.82)"`
  - Return `(total_score, reasons_string)`

- [ ] **Implement `recommend_songs(user_prefs, songs, k)`** in `src/recommender.py`
  - Loop through all songs, call `score_song` on each
  - Sort by score descending using `sorted()` (not `.sort()` — avoids mutating the original list)
  - Return top `k` as `List[Tuple[Dict, float, str]]`

- [ ] **Implement `Recommender.recommend` and `Recommender.explain_recommendation`** (OOP wrappers used by tests)
  - These can delegate to `score_song` and `recommend_songs` internally

- [ ] **Format terminal output in `src/main.py`**
  - Print title, score, and reasons for each result
  - Example:
    ```
    1. Sunrise City — Score: 3.84
       Because: genre match (+2.0), mood match (+1.0), energy score (+0.84)
    ```

- [ ] Run `pytest` — all starter tests should pass
- [ ] Take a screenshot of working terminal output and add it to `README.md`
- [ ] Add 1-line docstrings to new functions
- [ ] Commit: `git commit -m "implement load_songs, score_song, recommend_songs — working CLI recommender"`
- [ ] `git push origin main`

**Checkpoint:** `python -m src.main` prints ranked recommendations with scores and reasons. `pytest` passes.

---

## Phase 4: Evaluate and Explain (~45 min)

**Goal:** Test your system with diverse profiles, run an experiment, find a bias, document it.

### Tasks

- [ ] Define at least **3 distinct user profiles** in `src/main.py` and run each:
  - "High-Energy Pop": `{"genre": "pop", "mood": "intense", "energy": 0.9}`
  - "Chill Lofi": `{"genre": "lofi", "mood": "chill", "energy": 0.35}`
  - "Deep Rock": `{"genre": "rock", "mood": "intense", "energy": 0.85}`
  - Optional adversarial: `{"genre": "pop", "mood": "sad", "energy": 0.9}` (conflicting signals)

- [ ] Take a terminal screenshot for each profile's top-5 results and add to `README.md`

- [ ] Compare at least one profile's results to your own musical intuition — does it "feel" right?

- [ ] Run **one logic experiment** (choose one):
  - **Weight shift:** Double energy weight, halve genre weight — re-run and compare rankings
  - **Feature removal:** Comment out the mood check — observe how rankings shift
  - Document what changed and why in `README.md` → **Experiments You Tried**

- [ ] Use Copilot Chat with `#file:recommender.py` and `#file:songs.csv` to identify filter bubble / bias risks

- [ ] Fill in `model_card.md` → **Section 6: Limitations and Bias** with 3–5 sentences describing one real weakness found (e.g., "60% of the catalog is pop/lofi, so other genres rarely appear in top results regardless of user profile")

- [ ] Update `model_card.md` → **Section 7: Evaluation** with which profiles you tested and what surprised you

- [ ] Add comparison comments to `reflection.md` (or the README reflection section) — for each pair of profiles, note what changed in the output and why it makes sense

**Checkpoint:** 3+ profiles tested, 1 experiment run, bias documented in `model_card.md`.

---

## Phase 5: Reflection and Model Card (~25 min)

**Goal:** Complete the Model Card and write a personal reflection.

### Tasks

- [ ] Complete all sections of `model_card.md`:

  | Section | What to write |
  |---|---|
  | 1. Model Name | Something fun, e.g. "VibeFinder 1.0" |
  | 2. Intended Use | What it recommends, who it's for, what it shouldn't be used for |
  | 3. How It Works | Plain-language scoring explanation — no code |
  | 4. Data | Song count, genres/moods covered, what's missing |
  | 5. Strengths | Which user types it serves well |
  | 6. Limitations and Bias | At least one real bias found in Phase 4 |
  | 7. Evaluation | Profiles tested, experiment results, surprises |
  | 8. Future Work | 2–3 concrete improvements |
  | 9. Personal Reflection | Biggest learning moment, how AI helped/needed checking, what's next |

- [ ] Write your personal reflection in `README.md` → **Reflection** section (1–2 paragraphs):
  - How does a simple numeric score turn into a "recommendation"?
  - Where could bias or unfairness enter a system like this at scale?

- [ ] Final commit and push

**Checkpoint:** `model_card.md` fully filled out, reflection written, repo pushed.

---

## Optional Extensions (~30 min each)

Pick any that interest you — none are required.

| Challenge | What it involves |
|---|---|
| **Advanced features** | Add `popularity`, `release_decade`, or detailed mood tags to CSV and scoring logic |
| **Multiple scoring modes** | Build "Genre-First" vs "Mood-First" modes switchable from `main.py` |
| **Diversity penalty** | Penalize songs if the same artist already appears in the top results |
| **Visual summary table** | Use `tabulate` or ASCII formatting to display results as a table with reasons |

---

## File Reference

| File | Purpose |
|---|---|
| `data/songs.csv` | Song catalog — expand to 15–20 songs |
| `src/recommender.py` | Core logic: `load_songs`, `score_song`, `recommend_songs`, `Recommender` class |
| `src/main.py` | Runner — defines user profiles and prints results |
| `tests/test_recommender.py` | Starter tests for `Song`, `UserProfile`, `Recommender` |
| `model_card.md` | AI documentation artifact — fill out all 9 sections |
| `README.md` | Project explanation, screenshots, experiments, reflection |

---

## Scoring Logic Summary

```
score = 0.0
reasons = []

if song["genre"] == user_prefs["genre"]:
    score += 2.0
    reasons.append("genre match (+2.0)")

if song["mood"] == user_prefs["mood"]:
    score += 1.0
    reasons.append("mood match (+1.0)")

energy_score = 1.0 - abs(song["energy"] - user_prefs["energy"])
score += energy_score
reasons.append(f"energy score (+{energy_score:.2f})")

return score, ", ".join(reasons)
```

Adjust weights based on your Phase 2 decisions and Phase 4 experiments.
