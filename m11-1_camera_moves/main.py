import os
from dotenv import load_dotenv
import psycopg
from google import genai
from google.genai import types

load_dotenv()

TEST_QUERIES = [
    ("камера кружится вокруг здания", "orbit"),
    ("снимаем сверху тарелку с едой на столе", "top_down"),
    ("Все замирает но капли воды медленно движутся", "slow_motion"),
    ("камера приближается к лицу, но фон не смещается", "zoom_in"),
    ("камера движется вместе с машиной", "truck"),
    ("в начале виден один дом затем камера поднимается вверх и виден весь город", "drone_reveal"),
    ("изображение слегка трясётся, как будто снимают на телефон в толпе", "handheld"),
    ("сначала фокус на чашке а затем фокус переходить на человека на фоне", "rack_focus"),
    ("герой кажется огромным и сильным, смотрим на него снизу", "low_angle"),
    ("небо над городом быстро меняется от дня к ночи за пару секунд", "time_lapse"),
]

def embedding(text: str):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    result = client.models.embed_content(
        model="gemini-embedding-2",
        contents=text,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY", output_dimensionality=768)
    )
    return result.embeddings[0].values

def search(query: str):
    with psycopg.connect(os.getenv("DATABASE_URL")) as conn:
        with conn.cursor() as cur:
            embed = embedding(query)
            db_query = "select name from camera_moves order by embedding <=> %s::vector limit 3"
            cur.execute(db_query, (embed,))
            results = cur.fetchall()
            data = []
            for r in results:
                data.append(r[0])
            return data

def test(test_queries: list):
    top = []
    for q in test_queries:
        result = search(q[0])
        try:
            top.append(result.index(q[1]) + 1)
        except ValueError:
            top.append(None)
        print(f"Text: {q[0]}, Correct: {q[1]}, Result of search: {result}")

    top_1 = top.count(1) / len(test_queries)
    top_3 = (top.count(1) + top.count(2) + top.count(3)) / len(test_queries)
    mrr = (top.count(1) + 1/3) / len(test_queries)
    print(f"@1: {top_1}, @3: {top_3}, mrr: {mrr}")
test(TEST_QUERIES)