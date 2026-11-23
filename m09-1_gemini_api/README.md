# m09-1 · Первый вызов LLM и лог в Postgres

Скрипт отправляет текст в Gemini API и записывает каждый вызов в таблицу `llm_calls`: модель, вопрос, токены входа и выхода, время ответа и сам ответ. Задача — с первого вызова привыкнуть считать токены, а значит, и деньги.

На этих логах сравнивается, сколько токенов стоит один и тот же вопрос на английском, русском и казахском.

## Как устроено

1. `ask_gemini(text)` вызывает модель `gemini-3.5-flash-lite` через Interactions API.
2. Время ответа замеряется вокруг вызова через `time.perf_counter()` и записывается в миллисекундах.
3. Токены берутся из `interaction.usage`: `total_input_tokens` и `total_output_tokens`.
4. Строка лога пишется в Postgres через psycopg.

## Таблица `llm_calls`

```sql
create table llm_calls (
    id bigserial primary key,
    model text not null,
    input_text text not null,
    input_tokens int not null,
    output_tokens int,
    response_time_ms int not null,
    response_text text,
    error_text text,
    created_at timestamptz default now()
);
```

`output_tokens`, `response_text` и `error_text` могут быть пустыми: они предназначены для вызовов, которые завершились ошибкой.

## Как запустить

Нужны Python и Postgres. Я использую Postgres в Docker, с отдельной базой `api_requests`.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install google-genai "psycopg[binary]" python-dotenv
```

Файл `.env`:

```
GEMINI_API_KEY=ключ из Google AI Studio
DATABASE_URL=postgresql://postgres:пароль@localhost:5432/api_requests
```

Создать таблицу (SQL выше) и запустить:

```bash
python main.py
```

Посмотреть лог:

```sql
select id, model, left(input_text, 20) as input, input_tokens, output_tokens, response_time_ms
from llm_calls;
```

## Сравнение токенов по языкам

Один и тот же вопрос клиента банка на трёх языках, модель `gemini-3.5-flash-lite`, по одному прогону на язык.

| Язык | Входные токены | × к англ. | Выходные токены | × к англ. | Время, мс |
|---|---|---|---|---|---|
| Английский | 35 | 1,00 | 125 | 1,00 | 2647 |
| Русский | 44 | 1,26 | 195 | 1,56 | 2541 |
| Казахский | 76 | 2,17 | 297 | 2,38 | 4083 |

| Наблюдение | Почему |
|---|---|
| Казахский вход дороже английского в 2,2 раза | Токенизатор обучен в основном на английских текстах. Частые английские слова — один токен, а казахские слова режутся на куски по 2–4 токена |
| Для казахоязычного клиента тот же сервис стоит примерно вдвое дороже | Цена API считается по токенам |
| Чистое сравнение — только по входу | Вопрос одинаковый. Выход зависит ещё и от длины ответа, а ответы разные по содержанию, поэтому 2,38 по выходу — смесь эффекта языка и длины ответа |
| Время растёт вместе с выходными токенами | Модель генерирует ответ по одному токену |
| Вывод предварительный | Один прогон на язык. Для надёжного результата нужно 3–5 прогонов и среднее |

## Структура

```
m09-1_gemini_api/
├── main.py     # вызов Gemini, замер времени, запись в llm_calls
├── config.py   # ключ API и адрес базы из .env
└── .env        # не коммитится
```
