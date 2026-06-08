# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [x] **Game's purpose.** A single-player number-guessing game built with Streamlit. The app picks a secret number within a range that depends on the chosen difficulty (Easy 1–20, Normal 1–100, Hard 1–50), and the player has a limited number of attempts to find it. After each guess the game gives a "higher/lower" hint, validates the input, and updates a running score until the player wins or runs out of attempts.

- [x] **Bugs I found.**
  - **Bug 1 — Reversed hints.** `check_guess` had the high/low messages swapped, so a guess *above* the secret told you to "Go HIGHER" and a guess *below* told you to "Go LOWER" — steering you the wrong way every time.
  - **Bug 2 — Out-of-range guesses accepted.** `parse_guess` only checked "is this a number?" and never compared the value against the allowed range, so numbers like `200` or `-1` were treated as valid guesses and got a normal direction hint instead of a warning.

- [x] **Fixes I applied.**
  - Refactored the core logic (`check_guess`, `parse_guess`, `update_score`, `get_range_for_difficulty`) out of `app.py` into `logic_utils.py` so it can be unit-tested without launching Streamlit.
  - Fixed Bug 1 by swapping the hint logic so a guess above the secret returns `"Too High"` (Go LOWER) and below returns `"Too Low"` (Go HIGHER). `check_guess` now returns just the outcome string; the UI hint text lives in `HINT_MESSAGES` in `app.py`.
  - Fixed Bug 2 by threading the active difficulty's `low`/`high` into `parse_guess(raw, low, high)` and rejecting anything outside the band — instead of hardcoding `1–100`, which would have wrongly accepted `50` on Easy (1–20).
  - Added regression tests in `tests/test_game_logic.py` for both bugs and confirmed the full suite passes (6 tests).

## 📸 Demo Walkthrough

A text-based playthrough of the **fixed** game so a reader can follow the end-to-end behavior without running it. Sample game: **Normal** difficulty (range **1–100**), secret number **63**, starting score **0**.

1. The player starts a Normal game. The app shows the range (1–100) and the attempts allowed, and the score begins at 0.
2. **Guess `75`** → 75 is above the secret (63), so the game correctly returns **"Too High" → 📉 Go LOWER!** (Bug 1 fixed — the hint points the right way). Score updates to **5**.
3. **Guess `60`** → 60 is below the secret, so the game returns **"Too Low" → 📈 Go HIGHER!**. Score updates to **0**.
4. **Guess `150`** → out of range, so the game rejects it with **"Out of range. Pick a number between 1 and 100."** instead of giving a direction hint (Bug 2 fixed). The score is unchanged.
5. **Guess `63`** → matches the secret, so the game returns **"🎉 Correct!"**, awards the win points (final score **40**), shows the balloons, and ends the round with a "You won! The secret was 63" message.
6. Switching to **Easy** difficulty (range 1–20) and entering `50` is now also rejected as out of range — confirming the fix respects each difficulty's band, not a hardcoded 1–100.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# ========================= X passed in 0.XXs =========================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
