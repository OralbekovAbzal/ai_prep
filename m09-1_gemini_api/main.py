import psycopg
from google import genai
from config import get_gemini_api_key, get_db_url
import time

def ask_gemini(input_text: str):
    client = genai.Client(api_key=get_gemini_api_key())

    start = time.perf_counter()

    interaction = client.interactions.create(
        model="gemini-3.5-flash-lite",
        input=input_text,
    )

    time_ms = (time.perf_counter() - start) * 1000

    with psycopg.connect(get_db_url()) as conn:
        with conn.cursor() as cur:
            cur.execute("insert into llm_calls (model, input_text, input_tokens, output_tokens, response_time_ms, response_text) values (%s, %s, %s, %s, %s, %s)", (interaction.model, input_text, interaction.usage.total_input_tokens, interaction.usage.total_output_tokens, time_ms, interaction.output_text))

texts = {
    "eng": "Hello! I want to check my card balance and see how much I spent on food delivery last month. Can you also tell me when my next loan payment is due?",
    "rus": "Здравствуйте! Я хочу проверить баланс своей карты и узнать, сколько я потратил на доставку еды в прошлом месяце. Можете также подсказать, когда мой следующий платёж по кредиту?",
    "kaz": "Сәлеметсіз бе! Мен картамның балансын тексеріп, өткен айда тамақ жеткізуге қанша жұмсағанымды білгім келеді. Сондай-ақ келесі несие төлемім қашан екенін айта аласыз ба?"
}

for k, v in texts.items():
    ask_gemini(v)