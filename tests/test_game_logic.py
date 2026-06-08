from logic_utils import check_guess, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- Regression tests for the bugs fixed in Step 2 ---

def test_high_low_hints_not_reversed():
    # Bug 1: the high/low hints were swapped. A guess ABOVE the secret must
    # report "Too High", and a guess BELOW must report "Too Low".
    assert check_guess(99, 50) == "Too High"
    assert check_guess(1, 50) == "Too Low"

def test_parse_guess_rejects_out_of_range_easy():
    # Bug 2: parse_guess never checked the range, so 50 was wrongly accepted
    # on Easy (1-20). It should now be rejected.
    ok, value, err = parse_guess("50", 1, 20)
    assert ok is False
    assert value is None
    assert "between 1 and 20" in err

def test_parse_guess_accepts_in_range():
    # A valid guess inside the band still parses correctly.
    ok, value, err = parse_guess("15", 1, 20)
    assert ok is True
    assert value == 15
    assert err is None
