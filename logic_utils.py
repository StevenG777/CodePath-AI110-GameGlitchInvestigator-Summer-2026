def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str, low: int, high: int):
    """
    Parse user input into an int guess and validate it against the range.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    # FIX (Bug 2): I asked the agent whether this FIXME spot was the real source
    # of the out-of-range bug. It confirmed parse_guess only checked "is it a
    # number?" and never compared against the range — and that hardcoding 1-100
    # would still break Easy/Hard. So we thread low/high in from the difficulty
    # and reject anything outside the band; the error flows back to the caller.
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    if value < low or value > high:
        return False, None, f"Out of range. Pick a number between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome.

    outcome: "Win", "Too High", or "Too Low"
    """
    if guess == secret:
        return "Win"

    # FIX (Bug 1 & 2): I spotted the reversed hints; agent confirmed the messages
    # were swapped and that the str(secret) path made the except branch compare
    # strings. Swapped the messages and removed the dead try/except together.
    if guess > secret:
        # guess is larger than the secret → player must go lower
        return "Too High"
    else:
        # guess is smaller than the secret → player must go higher
        return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score
