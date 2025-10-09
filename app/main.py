from fastapi import FastAPI, Query

from app.utils import (
    get_container_cpu,
    get_container_memory,
    get_version,
    simulate_traffic
)

app = FastAPI()

@app.get("/")
async def hello():
    return {"message": "Hello World"}

@app.get("/health", status_code=200)
async def health_check():
    return {"message": "OK"}

@app.get("/version")
async def version():
    return {"release_version": get_version()}

@app.get("/memory")
async def container_memory():
    return {"memory_usage": get_container_memory()}

@app.get("/cpu")
async def container_cpu():
    return {"cpu_usage": get_container_cpu()}

@app.get("/simulate")
async def simulate(
    time_to_run: int = Query(gt=0, le=30),
    interval: int = Query(gt=0, le=30)
):
    request_sent = await simulate_traffic(time_to_run, interval)
    return {"status": "done", "requests_sent": request_sent}
