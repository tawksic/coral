from fastapi import FastAPI
from utils import get_version, get_container_memory_stats, get_container_cpu_stats

app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello World"}

@app.get("/health", status_code=200)
def health_check():
    return {"message": "OK"}

@app.get("/version")
def version():
    return {"release_version": get_version()}

@app.get("/container-memory")
def container_memory():
    return {"memory_usage": get_container_memory_stats()}

@app.get("/container-cpu")
def container_cpu():
    return {"cpu_usage": get_container_cpu_stats()}

