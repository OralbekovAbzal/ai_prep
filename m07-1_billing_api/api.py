from main import create_job
from fastapi import FastAPI, Depends
from config import check_key
from models import Job
from db import execute_query

app = FastAPI()

@app.post("/jobs", dependencies=[Depends(check_key)])
def new_job(job: Job):
    data = job.model_dump()
    res = create_job(data["user_id"], data["prompt"], data["model"], data["cost"])
    return {"job_id": res}

@app.get("/jobs/{id}")
def get_job(id: int):
    query = "select id, user_id, prompt, model, status, cost, created_at from jobs where id = %s"
    row = execute_query(query, id)
    if row == []:
        return None
    res = row[0]
    job = {
        "id": res[0],
        "user_id": res[1],
        "model": res[2],
        "status": res[3],
        "cost": res[4],
        "created_at": res[5]
    }
    return job

@app.get("/wallets/{user_id}")
def get_job(user_id: int):
    query = "select id, user_id, balance from wallets where user_id = %s"
    row = execute_query(query, user_id)
    if row == []:
        return None
    res = row[0]
    wallet = {
        "id": res[0],
        "user_id": res[1],
        "balance": res[2]
    }
    return wallet