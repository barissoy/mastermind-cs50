from project import generate_code, check_guess, format_feedback, COLORS, CODE_LENGTH

def test_generate_code_length():
    code = generate_code()
    assert len(code) == CODE_LENGTH

def test_generate_code_valid_colors():
    code = generate_code()
    for c in code:
        assert c in COLORS

def test_check_guess_all_correct():
    secret = ["A", "B", "C", "D"]
    guess =  ["A", "B", "C", "D"]
    black, white = check_guess(secret, guess)
    assert black == 4
    assert white == 0

def test_check_guess_mixed():
    secret = ["A", "B", "C", "D"]
    guess =  ["A", "C", "B", "X"]
    black, white = check_guess(secret, guess)
    assert black == 1
    assert white == 2

def test_format_feedback():
    fb = format_feedback(2, 1, length=4)
    assert fb == ["black", "black", "white", "empty"]
