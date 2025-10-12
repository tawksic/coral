from fastapi import APIRouter

from app.services.container_metrics import get_container_cpu, get_container_memory

router = APIRouter(prefix="/container", tags=["container"])


@router.get("/cpu")
async def container_cpu():
    return {"cpu_usage": get_container_cpu()}


@router.get("/memory")
async def container_memory():
    return {"memory_usage": get_container_memory()}

