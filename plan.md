# Music Recommender Simulation — Project Plan

**Estimated total time:** ~4 hours  
**Goal:** Build a weighted-score, content-based music recommender in Python, evaluate its behavior, and document it with a Model Card.

---

## Phase 1: Understanding the Problem (~25 min) ✅

**Goal:** Learn how real recommenders work and decide what your system will do.

### Tasks

- [x] Fork and clone the repo, open in VS Code.
- [x] Research the difference between:
  - **Collaborative filtering** — uses other users' behavior (e.g., "people like you also liked…")
  - **Content-based filtering** — uses song attributes (e.g., genre, mood, energy) — this is what we're building
- [x] Review `data/songs.csv` to understand available features:
  - `genre`, `mood`, `energy` (0.0–1.0), `tempo_bpm`, `valence`, `danceability`, `acousticness`
- [x] Decide your "Algorithm Recipe" — the scoring rules your system will use:
  - `+2.0` for genre match, `+1.0` for mood match, `1.0 - abs(song_energy - target_energy)` for energy proximity
- [x] Update `README.md` → **How The System Works** with plain-language explanation, feature table, and scoring pseudocode

**Checkpoint:** ✅ Written concept sketch complete — data flow, scoring logic, and bias noted.

---

## Phase 2: Designing the Simulation (~45 min) ✅

**Goal:** Expand the dataset, define a user profile, and lock in your scoring logic before writing code.

### Tasks

- [x] Expanded `data/songs.csv` from 10 to 20 songs with diverse genres/moods:
  - Added: hip-hop, edm, country, classical, r&b, folk, metal, blues, reggae, electronic
  - Added moods: confident, energetic, nostalgic, melancholic, romantic, peaceful, aggressive, soulful, uplifting, dreamy
- [x] Defined starter user profile dictionary in `src/main.py`:
  ```python
  user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}
  ```
- [x] Finalized scoring weights:

  | Signal | Points |
  |---|---|
  | Genre match | +2.0 |
  | Mood match | +1.0 |
  | Energy proximity | `1.0 - abs(song_energy - target_energy)` |

- [x] Added Mermaid.js flowchart to `README.md` showing: `User Prefs + songs.csv → score each song → sort → Top K`
- [x] Documented finalized recipe and expected bias in `README.md` → **How The System Works**

**Checkpoint:** ✅ 20-song CSV, defined user profile, locked-in scoring rules.

---

## Phase 3: Implementation (~90 min) ✅

**Goal:** Make `src/recommender.py` fully functional — load songs, score them, rank them, explain results.

### Key files
- `src/recommender.py` — core logic (`load_songs`, `score_song`, `recommend_songs`, `Recommender` class)
- `src/main.py` — runner that calls `load_songs` and `recommend_songs`
- `tests/test_recommender.py` — existing tests for `Song`, `UserProfile`, `Recommender`

### Tasks

- [x] **Implemented `load_songs(csv_path)`** in `src/recommender.py`
  - Uses Python's `csv` module; casts all numeric fields to `float`/`int`
  - Returns `List[Dict]`

- [x] **Added `score_song(user_prefs, song, weights=None)`** returning `(float, str)`:
  - Awards points per recipe; builds human-readable reasons string
  - Accepts optional `weights` dict for mode switching (added in optional extensions)

- [x] **Implemented `recommend_songs(user_prefs, songs, k, mode)`**
  - Uses `sorted()` (non-mutating); returns top `k` as `List[Tuple[Dict, float, str]]`

- [x] **Implemented `Recommender.recommend` and `Recommender.explain_recommendation`** (OOP wrappers for tests)

- [x] **Formatted terminal output in `src/main.py`**
  - Prints rank, title, artist, score out of max possible, and reasons for each result

- [x] `pytest` — 2/2 tests pass
- [ ] Take a screenshot of terminal output and add to `README.md` *(manual step)*
- [x] 1-line docstrings added to all functions
- [ ] Commit and push *(manual step)*

**Checkpoint:** ✅ `python -m src.main` prints ranked recommendations with scores and reasons. `pytest` passes.

---

## Phase 4: Evaluate and Explain (~45 min) ✅

**Goal:** Test your system with diverse profiles, run an experiment, find a bias, document it.

### Tasks

- [x] Defined 4 user profiles in `src/main.py` and ran each:
  - "Happy Pop": `{"genre": "pop", "mood": "happy", "energy": 0.8}`
  - "Chill Lofi": `{"genre": "lofi", "mood": "chill", "energy": 0.35}`
  - "Deep Rock": `{"genre": "rock", "mood": "intense", "energy": 0.9}`
  - "Adversarial EDM": `{"genre": "edm", "mood": "peaceful", "energy": 0.95}` *(conflicting signals)*

- [ ] Take terminal screenshots for each profile and add to `README.md` *(manual step)*

- [x] Compared Happy Pop results to musical intuition — Sunrise City at #1 (3.98/4.0) felt correct

- [x] Ran logic experiment: swapped genre/mood weights (genre 2.0→1.0, mood 1.0→2.0)
  - Gym Hero and Rooftop Lights swapped positions at #2/#3
  - Documented in `README.md` → **Experiments You Tried** with before/after table

- [x] Identified bias risks: genre dominance, sparse genre catalog, no memory, non-negative energy scoring

- [x] Filled in `model_card.md` → **Section 6: Limitations and Bias** (4 specific weaknesses)

- [x] Updated `model_card.md` → **Section 7: Evaluation** with all 4 profiles + experiment results

- [x] Added profile comparison notes in `README.md` → **Experiments You Tried**

**Checkpoint:** ✅ 4 profiles tested, 1 experiment run, bias documented in `model_card.md`.

---

## Phase 5: Reflection and Model Card (~25 min) ✅

**Goal:** Complete the Model Card and write a personal reflection.

### Tasks

- [x] Completed all sections of `model_card.md`:

  | Section | Status |
  |---|---|
  | 1. Model Name | ✅ VibeFinder 1.0 |
  | 2. Intended Use | ✅ Done |
  | 3. How It Works | ✅ Done (updated for modes + new features) |
  | 4. Data | ✅ Done (updated for 12 columns) |
  | 5. Strengths | ✅ Done (updated for modes) |
  | 6. Limitations and Bias | ✅ Done |
  | 7. Evaluation | ✅ Done |
  | 8. Future Work | ✅ Done (updated to reflect what's been implemented) |
  | 9. Personal Reflection | ✅ Done |

- [x] Wrote personal reflection in `README.md` → **Reflection** (2 paragraphs)

- [ ] Final commit and push *(manual step)*

**Checkpoint:** ✅ `model_card.md` fully filled out, reflection written.

---

## Optional Extensions (~30 min each)

- [x] **Challenge 1 — Advanced features:** Added `popularity` (0–100) and `release_decade` to `songs.csv` and scoring logic as optional bonus signals (+0.5 each, max +1.0 total)
- [x] **Challenge 2 — Multiple scoring modes:** Built `SCORING_MODES` dict with `balanced`, `genre-first`, `mood-first`, `energy-focused` — switchable via `mode=` parameter in `recommend_songs` and `Recommender`
- [ ] **Challenge 3 — Diversity penalty:** Penalize songs if same genre/artist already appears in top results
- [ ] **Challenge 4 — Visual summary table:** Use `tabulate` or ASCII formatting for terminal output

---

## File Reference

| File | Purpose |
|---|---|
| `data/songs.csv` | Song catalog — 20 songs, 12 columns including popularity and release_decade |
| `src/recommender.py` | Core logic: `SCORING_MODES`, `load_songs`, `score_song`, `recommend_songs`, `Recommender` |
| `src/main.py` | Runner — demonstrates advanced features and all 4 scoring modes |
| `tests/test_recommender.py` | Starter tests for `Song`, `UserProfile`, `Recommender` — all passing |
| `model_card.md` | AI documentation artifact — all 9 sections complete |
| `README.md` | Project explanation, algorithm recipe, experiments, reflection |

---

## Scoring Logic Summary (current implementation)

```python
# Weights come from the chosen SCORING_MODES entry (default: "balanced")
# genre=2.0, mood=1.0, energy=×1.0  →  max base score 4.0
# Optional: +0.5 popularity proximity, +0.5 decade match  →  max 5.0

score = 0.0
reasons = []

if song["genre"] == user_prefs["genre"]:
    score += weights["genre"]
    reasons.append(f"genre match (+{weights['genre']})")

if song["mood"] == user_prefs["mood"]:
    score += weights["mood"]
    reasons.append(f"mood match (+{weights['mood']})")

energy_score = round((1.0 - abs(song["energy"] - user_prefs["energy"])) * weights["energy"], 2)
score += energy_score
reasons.append(f"energy score (+{energy_score:.2f})")

# Optional bonus signals
if "target_popularity" in user_prefs:
    pop_score = round((1.0 - abs(song["popularity"] - user_prefs["target_popularity"]) / 100) * 0.5, 2)
    score += pop_score
    reasons.append(f"popularity score (+{pop_score:.2f})")

if "target_decade" in user_prefs and song["release_decade"] == user_prefs["target_decade"]:
    score += 0.5
    reasons.append("decade match (+0.5)")

return round(score, 2), ", ".join(reasons)
```
