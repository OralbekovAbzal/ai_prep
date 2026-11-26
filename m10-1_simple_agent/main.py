from google import genai
from dotenv import load_dotenv
import os
import psycopg
import sys
import json


load_dotenv()

class ToolError(Exception):
    pass

def price_credits(user_id: int, model: str, seconds: int) -> int:
    if model == "pro":
        data = {
            "cost": seconds * 5
        }
        return data
    if model == "fast":
        data = {
            "cost": seconds * 2
        }
        return data
    raise ToolError(f"Invalid model: {model}. Correct models are fast and pro.")

def search_prompts(user_id: int, query: str) -> tuple:
    with psycopg.connect(os.getenv("DATABASE_URL")) as conn:
        with conn.cursor() as cur:
            cur.execute("select prompt, model, status, cost, created_at from jobs where prompt like %s and user_id = %s;",("%" + query + "%", user_id))
            rows = cur.fetchall()
            data = list()
            for prompt, model, status, cost, created_at in rows:
                data.append({
                    "prompt": prompt,
                    "model": model,
                    "status": status,
                    "cost": cost,
                    "created_at": created_at.isoformat()
                })
            return data

def check_balance(user_id: int) -> int:
    with psycopg.connect(os.getenv("DATABASE_URL")) as conn:
        with conn.cursor() as cur:
            cur.execute("select balance from wallets where user_id = %s",(user_id,))
            row = cur.fetchone()
            if row is None:
                raise ToolError("Неизвестный пользователь")
            data = {
                "balance": row[0]
            }
            return data

def ask_permision(model: str, cost: int, seconds: int) -> bool:
    text = f"Сгенерировать видео на {seconds}с используя модель {model} за {cost} кредитов? [y/n]\n"
    decision = input(text)
    yes = ["y", "yes", "ok", "go"]
    no = ["n", "no", "not", "stop"]
    if decision.lower() in yes:
        return True
    elif decision.lower() in no:
        return False
    else:
        raise ToolError("Пользователь не дал конкретного ответа")

def start_generation(user_id: int, prompt: str, model: str, seconds: int) -> dict:
    if seconds <= 0:
        raise ToolError(f"Длительность видео не может быть отрицательным: {seconds}")
    
    with psycopg.connect(os.getenv("DATABASE_URL")) as conn:
        with conn.cursor() as cur:
            data = price_credits(user_id, model, seconds)
            cost = data["cost"]

            query = "select balance from wallets where user_id = %s"
            cur.execute(query, (user_id,))
            row = cur.fetchone()

            if row is None:
                raise ToolError("Неизвестный пользователь")
            balance = row[0]
            if balance < cost:
                raise ToolError("Недостаточно средств")

            try:
                decision = ask_permision(model, cost, seconds)
                if not decision:
                    return {"result": "Permision denied"}
            except ToolError as e:
                return {"result": f"Permision error: {e}"}

            query = "select balance from wallets where user_id=%s for update"
            cur.execute(query, (user_id,))
            row = cur.fetchone()

            if row is None:
                raise ToolError("Неизвестный пользователь")
            balance = row[0]
            if balance < cost:
                raise ToolError("Недостаточно средств")

            query = "insert into jobs (user_id, prompt, model, status, cost) values (%s, %s, %s, 'queued', %s)"
            cur.execute(query, (user_id, prompt, model, cost))
            if cur.rowcount == 0:
                raise ToolError("Ошибка при создании работы")

            query = "update wallets set balance = balance - %s where user_id = %s"
            cur.execute(query,(cost, user_id))
            return {"result": "success"}

price_credits_tool = {
    "type": "function",
    "name": "price_credits",
    "description": (
        "Calculate the cost in credits of generating one video. "
        "Use it whenever the user asks about price or whether they can afford videos. "
        "For several videos, call it once and multiply the result yourself."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "model": {
                "type": "string",
                "enum": ["fast", "pro"],
                "description": "Generation model: fast (cheaper) or pro (higher quality).",
            },
            "seconds": {
                "type": "integer",
                "description": "Length of one video in seconds, a positive whole number.",
            },
        },
        "required": ["model", "seconds"],
    },
}

search_prompts_tool = {
    "type": "function",
    "name": "search_prompts",
    "description": (
        "Search the current user's past generation jobs by words in the prompt. "
        "Returns matching jobs with prompt, model, status, cost and date. "
        "Use it when the user asks about videos they made before or what similar videos cost."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "One or two key words to search for in prompts, e.g. 'горы' or 'кофейня'. Use the language of the stored prompts (Russian).",
            },
        },
        "required": ["query"],
    },
}

check_balance_tool = {
    "type": "function",
    "name": "check_balance",
    "description": (
        "Get the current user's credit balance. "
        "Use it before answering whether the user can afford something. "
        "It always returns the balance of the current user only."
    ),
    "parameters": {
        "type": "object",
        "properties": {},
    },
}

start_generation_tool = {
    "type": "function",
    "name": "start_generation",
    "description": (
        "Start generating one video and charge its cost in credits from the current user's balance. "
        "Call it only when the user clearly asks to generate a video, not when they only ask about price or balance. "
        "The user is asked to confirm the price automatically before any credits are charged, "
        "so do not ask for confirmation yourself. "
        "If the result says the user declined, do not call it again for the same video."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "prompt": {
                "type": "string",
                "description": "Description of the video to generate, in the user's words or slightly improved.",
            },
            "model": {
                "type": "string",
                "enum": ["fast", "pro"],
                "description": "Generation model: fast (cheaper) or pro (higher quality).",
            },
            "seconds": {
                "type": "integer",
                "description": "Length of the video in seconds, a positive whole number.",
            },
        },
        "required": ["prompt", "model", "seconds"],
    },
}

tools = {
    "check_balance": check_balance,
    "search_prompts": search_prompts,
    "price_credits": price_credits,
    "start_generation": start_generation
}

tool_list = [price_credits_tool, search_prompts_tool, check_balance_tool, start_generation_tool]

def agent(user_id: int, prompt: str) -> str:
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    prev_id = None
    interaction = client.interactions.create(
            model="gemini-3.5-flash",
            input=prompt,
            tools=tool_list,
            previous_interaction_id=prev_id
        )
    for _ in range(5):
        prompt = ""
        data = list()
        for step in interaction.steps:
            prev_id = interaction.id
            if step.type == "function_call":
                if step.name not in tools:
                    data.append({
                        "type": "function_result",
                        "name": step.name,
                        "call_id": step.id,
                        "result": [{"type":"text", "text":f"Неизвестный инстремент {step.name}. Список актуальных инструментов {tool_list}"}]
                    })
                    continue
                try:
                    result = tools[step.name](user_id, **step.arguments)
                    data.append({
                        "type": "function_result",
                        "name": step.name,
                        "call_id": step.id,
                        "result": [{"type":"text", "text":json.dumps(result, ensure_ascii=False)}]
                    })
                    sys.stderr.write(f"Агент использовал функцияю {step.name} с аргументами {step.arguments}\n")
                except Exception as e:
                    data.append({
                        "type": "function_result",
                        "name": step.name,
                        "call_id": step.id,
                        "result": [{"type":"text", "text":f"Ошибка при вызове функции: {step.name}. Ошибка: {e}"}]
                    })
                    sys.stderr.write(f"Ошибка при вызове функции: {step.name}. Ошибка: {e}\n")

        if data:
            interaction = client.interactions.create(
                model="gemini-3.5-flash",
                input=data,
                tools=tool_list,
                previous_interaction_id=prev_id
            )
        else:
            return interaction.output_text
    return "Превышено количество запросов"

print(agent(2, "запусти генерацию видео на 15 сек с промтом 'Ночные улицы Астаны'. Используй модель pro"))