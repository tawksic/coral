import asyncio
from time import time

import httpx

async def simulate_traffic(time_to_run: int, interval: int):
    start_time = time()
    count = 0
    async with httpx.AsyncClient() as client:
        while time() - start_time < time_to_run:
            resp = await client.get("http://localhost/health")
            count += 1
            await asyncio.sleep(interval)
    return count

