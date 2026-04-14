# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
