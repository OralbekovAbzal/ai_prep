import httpx
import time

with httpx.Client() as client:
    for _ in range(20):
        resp = client.get("https://jsonplaceholder.typicode.com/posts/1")
        print(resp.json())