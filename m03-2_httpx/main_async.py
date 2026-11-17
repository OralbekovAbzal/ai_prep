import httpx
import asyncio

URL = "https://jsonplaceholder.typicode.com/posts/{}"

async def fetch_one(client: httpx.AsyncClient, sem: asyncio.Semaphore, post_id: int):
    async with sem:
        resp = await client.get(URL.format(post_id))
        print(f"Успешно {post_id}")
        await asyncio.sleep(1)
        return resp.json()

async def main():
    sem = asyncio.Semaphore(5)
    async with httpx.AsyncClient(timeout=10) as client:
        tasks = [fetch_one(client, sem, i) for i in range(1,21)]
        results = await asyncio.gather(*tasks)
        print(len(results))

asyncio.run(main())