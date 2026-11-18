from db import conn
from models import UserNotFound, NotEnoughCredits
from fastapi import HTTPException

def create_job(user_id: int, prompt: str, model: str, cost: int) -> int:
    with conn.transaction():
        with conn.cursor() as cur:
            cur.execute("select balance from wallets where user_id = %s for update;", (user_id,))
            row = cur.fetchone()
            if row is None:
                raise UserNotFound(404, "Пользователь не найден")
            if row[0] >= cost:
                cur.execute("update wallets set balance = balance - %s where user_id = %s and balance >= %s;", (cost, user_id, cost))
                cur.execute("insert into jobs (user_id, prompt, model, status, cost) values (%s, %s, %s, 'queued', %s) returning id;", (user_id, prompt, model, cost))
                row = cur.fetchone()
                if row is None:
                    raise HTTPException(500, "Не удалось создать задачу")
                return row[0]
            raise NotEnoughCredits(402, "Недостаточно кредитов")
