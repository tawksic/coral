from fastapi import APIRouter, Query

from app.services.traffic_simulator import simulate_traffic

router = APIRouter(tags=["simulation"])


@router.get("/simulate")
async def simulate(
    duration: int = Query(gt=0, le=30),
    delay: int = Query(gt=0, le=30)
):
    request_sent = await simulate_traffic(duration, delay)
    return {"status": "done", "requests_sent": request_sent}

