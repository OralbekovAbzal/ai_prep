import psycopg
from config import get_db

def execute_query(sql, *params) -> list:
    with psycopg.connect(get_db()) as conn:
        with conn.cursor() as cur:
            res = cur.execute(sql, (*params,))
            return res.fetchall()

conn = psycopg.connect(get_db())