from fastapi import FastAPI, HTTPException
from models import PromtIn, PromtOut

app = FastAPI()

promts = dict()
next_id = {"next_id": 1}

@app.post("/promts", status_code=201)
def add_promt(promt: PromtIn):
    data = promt.model_dump()
    promt_id = next_id["next_id"]
    promts[promt_id] = data
    result = PromtOut(promt_id, promts[promt_id]["text"], promts[promt_id]["model"], promts[promt_id]["tags"])
    next_id["next_id"] += 1
    return result

@app.get("/promts")
def get_promt(tag: str = None):
    result = list()
    for k, v in promts.items():
        if k == "next_id":
            continue

        if tag is None or tag in v["tags"]:
            result.append(PromtOut(k, v["text"], v["model"], v["tags"]))
    return result

@app.get("/promts/{p_id}")
def get_promt_by_id(p_id: int):
    promt = promts.get(p_id)
    if promt is None:
        raise HTTPException(404, f"Object with id: {p_id} not found")
    result = PromtOut(p_id, promt["text"], promt["model"], promt["tags"])
    return result

@app.delete("/promts/{p_id}", status_code=200)
def delete_promt(p_id: int):
    promt = promts.get(p_id)
    if promt is None:
        raise HTTPException(404, f"Object with id: {p_id} not found")
    result = PromtOut(p_id, promt["text"], promt["model"], promt["tags"])
    del promts[p_id]
    return result