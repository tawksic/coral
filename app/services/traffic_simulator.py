import asyncio
from time import time

import httpx

async def simulate_traffic(duration: int, delay: int):
    start_time = time()
    count = 0
    async with httpx.AsyncClient() as client:
        while time() - start_time < duration:
            await client.get("http://localhost/health")
            count += 1
            await asyncio.sleep(delay)
    return count

