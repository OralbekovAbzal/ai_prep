import pytest
from main import parse_brief

def test_correct_aspect_ratio():
    text = "Видео в формате 9:16"
    assert parse_brief(text)["aspect_ratio"] == "9:16"

def test_words_instead_numbers():
    text = "Вертикальное видео"
    assert parse_brief(text)["aspect_ratio"] == "9:16"

def test_two_formats():
    text = "Нужно вертикальное видео про семью. Формат видео 16:9"
    assert parse_brief(text)["aspect_ratio"] == "9:16"

def test_wrone_format():
    text = "Видео должно быть в формате 4:3"
    assert parse_brief(text)["aspect_ratio"] is None

