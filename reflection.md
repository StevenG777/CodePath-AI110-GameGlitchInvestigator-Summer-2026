# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game, it looked like a normal number-guessing app — a title, a guess box, a Submit button, and an "Attempts left" counter — but the feedback it gave me was wrong almost every time I played. The hints pointed me in the wrong direction, it never stopped me from typing impossible numbers, and the attempts counter didn't match how many guesses I actually had.

The three concrete bugs I noticed at the start were:

- **Bug 1 — Hints are backwards.** No matter what number I guessed (anything other than the secret), the game kept telling me to "Go LOWER." I expected a guess below the secret to say "Go HIGHER" and a guess above it to say "Go LOWER," but the directions were reversed.
- **Bug 2 — Out-of-range numbers are accepted.** The game says to guess between 1 and 100, but it happily accepts numbers like 200 or -1. I expected a warning that the number was out of range, but instead it gave me a normal high/low hint as if the guess were valid.
- **Bug 3 — Attempts counter is off.** The "Attempts left" counter doesn't count correctly. It gave me one more (or one fewer) attempt than I should have, so the number on screen didn't match how many guesses I really got.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| 200 | Warning that the number is out of the 1–100 range | Treated as a valid guess and gave a direction hint | "📉 Go LOWER!" (no error) |
| -1 | Warning that the number is out of the 1–100 range | Treated as a valid guess and gave a direction hint | "📉 Go LOWER!" (no error) |
| 59 (secret = 60) | Hint to "Go HIGHER" | Hint to "Go LOWER" | "📉 Go LOWER!" (no error) |

---

## 2. How did you use AI as a teammate?

I used Claude Code (agent mode) and worked through it with a fixed, systematic
sequence rather than just asking it to "fix the bug." For each bug I (1) told it
where I *thought* the error was and asked it to confirm or correct my location,
(2) asked it to explain the underlying mechanism that produced the faulty output,
(3) asked it to propose a fix, and only then (4) gave it permission to apply the
change and document our collaboration as a comment right next to the affected code.
Keeping the diagnosis and the permission-to-edit as separate steps meant I
understood every change before it landed.

**Correct suggestion.** For Bug 2 (out-of-range numbers accepted), I guessed the
problem lived in `parse_guess()` and left a `FIXME`. The AI confirmed my location
was right and explained the mechanism: `parse_guess()` only answered "is this a
number?" and never compared the value against the allowed range, so `200` and `-1`
returned `(True, value, None)` and flowed straight into `check_guess()`, which gave
a normal high/low hint. It proposed threading the difficulty range into the
function as `parse_guess(raw, low, high)` and returning `False` with an
out-of-range message that reuses the existing error path at line 152. I verified
this by entering `200` and `-1` after the fix and seeing the "Out of range" warning
instead of a direction hint, and confirmed valid in-range guesses still worked.

**Incorrect / misleading suggestion.** A tempting shortcut that came up was to
hardcode the check as `if value < 1 or value > 100`, matching the on-screen
"between 1 and 100" text. That suggestion was misleading: the range actually
depends on difficulty (`get_range_for_difficulty()` returns 1–20 for Easy and 1–50
for Hard). I verified it was wrong by switching to **Easy** difficulty and guessing
`50` — a hardcoded 1–100 check would happily accept it even though the real range
is 1–20. So I rejected the hardcoded version and used the `low`/`high` parameters
threaded from the active difficulty instead.

---

## 3. Debugging and testing your fixes

I decided a bug was really fixed only when I could see it pass in two places: an
automated test that pinned the exact behavior, and the live app behaving correctly
when I reproduced the original failing input by hand. Before refactoring I moved the
game logic (`check_guess`, `parse_guess`, `update_score`,
`get_range_for_difficulty`) out of `app.py` into `logic_utils.py` so it could be
tested without launching Streamlit, then ran the suite with
`.venv/bin/python -m pytest tests/ -v` and confirmed all 6 tests passed (3 starter
tests plus 3 I added).

The most useful test I ran was `test_parse_guess_rejects_out_of_range_easy`, which
calls `parse_guess("50", 1, 20)` and asserts it returns `ok is False` with an error
message containing "between 1 and 20." This directly targeted Bug 2 and showed me
why the hardcoded `1–100` shortcut would have been wrong: on Easy the valid range is
1–20, so the test would have failed if I'd hardcoded the bounds instead of threading
in `low`/`high`. I also added `test_high_low_hints_not_reversed` for Bug 1 (a guess
of 99 against 50 must be "Too High," and 1 against 50 must be "Too Low"), then
confirmed it live with `streamlit run app.py` by guessing above the secret and seeing
"📉 Go LOWER!" and entering `50` on Easy and seeing the out-of-range warning.

AI helped me design the tests by keeping them small and behavior-focused: rather than
testing implementation details, each test reproduces a specific bug's input and
asserts the corrected outcome, so the test name itself documents which glitch it
guards against. It also caught a signature mismatch I'd have missed — the starter
tests expected `check_guess` to return a plain outcome string (e.g. `"Win"`), but the
original code returned a `(outcome, message)` tuple. That pushed me to keep the logic
layer returning just the outcome and move the hint text into the UI, which made the
code cleaner and the tests pass at the same time.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
