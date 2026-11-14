import re

# ---------- Числа словами ----------
_NUM_WORDS = {
    "ноль": 0, "один": 1, "одна": 1, "одну": 1, "одной": 1,
    "два": 2, "две": 2, "три": 3, "четыре": 4, "пять": 5,
    "шесть": 6, "семь": 7, "восемь": 8, "девять": 9, "десять": 10,
    "одиннадцать": 11, "двенадцать": 12, "тринадцать": 13,
    "четырнадцать": 14, "пятнадцать": 15, "шестнадцать": 16,
    "семнадцать": 17, "восемнадцать": 18, "девятнадцать": 19,
    "двадцать": 20, "тридцать": 30, "сорок": 40, "пятьдесят": 50,
    "шестьдесят": 60, "семьдесят": 70, "восемьдесят": 80,
    "девяносто": 90, "сто": 100,
    "полтора": 1.5, "полторы": 1.5,
}
_NUM_WORD = "|".join(sorted(_NUM_WORDS, key=len, reverse=True))
_NUM_WORDS_RE = rf"(?:(?:{_NUM_WORD})\b)(?:\s+(?:(?:{_NUM_WORD})\b))*"

_UNIT = (
    r"секунд\w*|сек\b\.?|seconds?\b|secs?\b"
    r"|минут\w*|мин\b\.?|minutes?\b|mins?\b"
    r"|час(?:а|ов)?\b|hours?\b|hrs?\b"
)

_DURATION_RE = re.compile(
    r"(?<!\w)(?:"
    r"пол\s*-?\s*(?P<half_unit>минут\w*|час\w*)"
    rf"|(?P<num>\d+(?:[.,]\d+)?|{_NUM_WORDS_RE})\s*-?\s*(?P<unit>{_UNIT})"
    r"|(?P<snum>\d+(?:[.,]\d+)?)(?P<short>с|s|м|m|ч|h)\b"
    r"|(?P<bare>минут[уакн]\w*|час\b|часов(?:ое|ой|ая|ого)\b)"
    r")",
    re.IGNORECASE,
)

# ---------- Формат кадра ----------
_KNOWN_RATIOS = {"9:16", "16:9", "1:1", "4:5", "5:4", "4:3", "3:4",
                 "21:9", "9:21", "2:3", "3:2"}

_RATIO_RE = re.compile(
    r"(?<![\d.,])(\d{1,2})\s*(?::|/|x|х|×|\bна\b)\s*(\d{1,2})(?!\d)",
    re.IGNORECASE,
)

_RATIO_WORDS = [
    (r"вертикальн\w*|портретн\w*|vertical\w*|portrait\w*"
     r"|сторис|stories|reels|рилс\w*|тик-?ток\w*|tik-?tok|shorts|шортс\w*", "9:16"),
    (r"горизонтальн\w*|альбомн\w*|широкоформатн\w*"
     r"|horizontal\w*|landscape\w*|widescreen", "16:9"),
    (r"квадрат\w*|square\w*", "1:1"),
]
_RATIO_WORDS_RE = [(re.compile(rf"(?<!\w)(?:{p})", re.IGNORECASE), v)
                   for p, v in _RATIO_WORDS]

# ---------- Стоп-слова ----------
_STOPWORDS = set("""
пожалуйста плиз сделай сделайте сделать создай создайте создать сгенерируй
сгенерируйте сгенерировать нарисуй снять сними нужно надо нужен нужна нужны
хочу хотел хотела хотелось бы можно можешь мне нам меня мой моя мое моё мои
давай давайте видео видеоролик видос ролик ролика клип формат формате формата
длительность длительностью продолжительность продолжительностью длиной длинной
примерно около где-то приблизительно
в во на с со к ко по о об про для из от до за под над при без через у
и а но или что чтобы как это этот эта эти тот та те так такой же ли не ни то
был была было быть очень просто еще ещё где когда который которая которое
которые его ее её их он она они оно я ты мы вы там тут здесь будет есть
please make create generate need want video clip format the a an of for with
in on and to about my me i it is be some
""".split())

_TOKEN_RE = re.compile(r"[a-zа-яё0-9]+(?:-[a-zа-яё0-9]+)*", re.IGNORECASE)


def _num_value(raw):
    raw = raw.strip().lower()
    if re.fullmatch(r"\d+(?:[.,]\d+)?", raw):
        return float(raw.replace(",", "."))
    return sum(_NUM_WORDS[w] for w in raw.split())


def _unit_factor(unit):
    u = unit.lower()
    if u[0] in "сs":
        return 1
    if u[0] in "мm":
        return 60
    return 3600


def _match_seconds(m):
    if m.group("half_unit"):
        return 0.5 * _unit_factor(m.group("half_unit"))
    if m.group("num"):
        return _num_value(m.group("num")) * _unit_factor(m.group("unit"))
    if m.group("snum"):
        return _num_value(m.group("snum")) * _unit_factor(m.group("short"))
    return 1 * _unit_factor(m.group("bare"))


def _find_duration(text):
    matches = list(_DURATION_RE.finditer(text))
    spans = [m.span() for m in matches]
    if not matches:
        return None, spans

    total = _match_seconds(matches[0])
    prev = matches[0]
    for m in matches[1:]:
        gap = text[prev.end():m.start()]
        if re.fullmatch(r"\s*(?:и\s*)?", gap, re.IGNORECASE):
            total += _match_seconds(m)
            prev = m
        else:
            break
    return int(round(total)), spans


def _find_aspect_ratio(text):
    found = []
    for m in _RATIO_RE.finditer(text):
        ratio = f"{int(m.group(1))}:{int(m.group(2))}"
        if ratio in _KNOWN_RATIOS:
            found.append((m.start(), ratio, m.span()))
    for regex, value in _RATIO_WORDS_RE:
        for m in regex.finditer(text):
            found.append((m.start(), value, m.span()))

    if not found:
        return None, []
    found.sort(key=lambda x: x[0])
    return found[0][1], [f[2] for f in found]


def _extract_keywords(text, spans):
    chars = list(text)
    for start, end in spans:
        for i in range(start, end):
            chars[i] = " "
    cleaned = "".join(chars).lower()

    keywords, seen = [], set()
    for token in _TOKEN_RE.findall(cleaned):
        if token in _STOPWORDS or token.isdigit() or len(token) < 2:
            continue
        if token not in seen:
            seen.add(token)
            keywords.append(token)
    return keywords or None


def parse_brief(prompt: str) -> dict:
    result = {"duration": None, "aspect_ratio": None, "keywords": None}
    if not isinstance(prompt, str) or not prompt.strip():
        return result

    duration, dur_spans = _find_duration(prompt)
    aspect_ratio, ratio_spans = _find_aspect_ratio(prompt)

    result["duration"] = duration
    result["aspect_ratio"] = aspect_ratio
    result["keywords"] = _extract_keywords(prompt, dur_spans + ratio_spans)
    return result