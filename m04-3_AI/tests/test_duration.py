import pytest
from main import parse_brief

def test_duration_minute_instead_second():
    text = "видео в 1 минуту"
    assert parse_brief(text)["duration"] == 60

def test_duration_words_instead_num():
    text = "видео в десять секунд"
    assert parse_brief(text)["duration"] == 10

def test_empty_text():
    text = ""
    assert parse_brief(text)["duration"] is None and parse_brief(text)["aspect_ratio"] is None and parse_brief(text)["keywords"] is None

def test_two_duration():
    text = "мне нужно видео на 10 секунд. Мы создаем рекламный ролик и он должен быть на 15 секунд."
    assert parse_brief(text)["duration"] == 10

def test_duration_with_c():
    text = "Продолжительность видео 15 с"
    assert parse_brief(text)["duration"] == 15