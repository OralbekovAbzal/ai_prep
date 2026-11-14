import pytest
from main import parse_brief

def test_with_not_meaningful_words():
    text = "Короче, сделай мне ролик про кешбэк по карте пожалуйста"
    res = parse_brief(text)["keywords"]
    assert "пожалуйста" not in res and "сделай" not in res and "короче" not in res

def test_correct_words():
    text = "Пожалуйста, сделай мне ролик про кешбэк по карте"
    assert "кешбэк" in parse_brief(text)["keywords"]

def test_reapet_words():
    text = "Наше отделение работает с кешбэк картами, сделай мне ролик про кешбэк по карте"
    words = parse_brief(text)["keywords"]
    count = 0
    for kw in words:
        if kw == "кешбэк":
            count += 1
    assert count == 1
