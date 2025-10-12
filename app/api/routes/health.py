from fastapi import APIRouter

from app.utils import get_version

router = APIRouter(tags=["health"])


@router.get("/")
async def hello():
    return {"message": "Hello World"}


@router.get("/health", status_code=200)
async def health_check():
    return {"message": "OK"}


@router.get("/version")
async def version():
    return {"release_version": get_version()}

