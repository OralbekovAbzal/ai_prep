def by_model(items: list, model: str) -> list:
    selected = []
    for i in items:
        if i["model"] == model:
            selected.append(i)
    return selected

def longer_than(items: list, sec: int) -> list:
    selected = []
    for i in items:
        if i["duration_sec"] > sec:
            selected.append(i)
    return selected

def all_tags(items: list) -> set:
    tags = set()
    for i in items:
        tags.update(i["tags"])
    return tags

def add_tag(tag: str,tags: list = None) -> list:
    tags = []
    tags.append(tag)
    return tags

videos = [
    {"title": "Кроссовки в ночном городе", "model": "kling", "duration_sec": 15, "tags": ["реклама", "ночь", "город"]},
    {"title": "Кофе в замедленной съёмке", "model": "veo", "duration_sec": 8, "tags": ["еда", "slow-motion"]},
    {"title": "Дрон над степью", "model": "sora", "duration_sec": 20, "tags": ["природа", "дрон"]},
    {"title": "Неоновая вывеска под дождём", "model": "kling", "duration_sec": 10, "tags": ["ночь", "город", "дождь"]},
    {"title": "Чай с пиалой на дастархане", "model": "veo", "duration_sec": 8, "tags": ["еда", "традиции"]},
    {"title": "Горы на закате", "model": "seedance", "duration_sec": 30, "tags": ["природа", "закат"]},
    {"title": "Смартфон вращается в студии", "model": "kling", "duration_sec": 5, "tags": ["реклама", "студия"]},
    {"title": "Байга в замедлении", "model": "sora", "duration_sec": 12, "tags": ["спорт", "slow-motion", "традиции"]},
    {"title": "Анимация логотипа", "model": "seedance", "duration_sec": 5, "tags": ["реклама", "анимация"]},
    {"title": "Вечерняя Астана с высоты", "model": "veo", "duration_sec": 20, "tags": ["город", "ночь", "дрон"]},
]

sorted_videos = sorted(videos, key=lambda x:(x["duration_sec"],x["title"]))

a = [1,2]
b = a
a.append(3) #Цифра 3 добавилась в оба списка так как b = a не копирует значения переменной а самму ссылку где храняться данные
print(id(a) == id(b))

assert len(by_model(videos, "kling")) == 3
assert len(longer_than(videos,10)) == 5
assert len(all_tags(videos)) == 13
assert sorted_videos[0]["title"] == "Анимация логотипа"
assert sorted_videos[1]["title"] == "Смартфон вращается в студии"