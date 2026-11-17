from models import Job
import asyncio

async def create_job(jobs: dict, id: int) -> Job:
    jobs[id]["progress"] = 15
    await asyncio.sleep(2)
    jobs[id]["status"] = "running"
    jobs[id]["progress"] = 25
    await asyncio.sleep(1)
    jobs[id]["progress"] = 30
    await asyncio.sleep(2)
    jobs[id]["progress"] = 53
    await asyncio.sleep(3)
    jobs[id]["progress"] = 86
    await asyncio.sleep(3)
    jobs[id]["progress"] = 100
    jobs[id]["status"] = "done"