from fastapi import APIRouter, Query

from app.services.traffic_simulator import simulate_traffic

router = APIRouter(prefix="/simulate", tags=["simulation"])


@router.get("/")
async def simulate(
    time_to_run: int = Query(gt=0, le=30),
    interval: int = Query(gt=0, le=30)
):
    request_sent = await simulate_traffic(time_to_run, interval)
    return {"status": "done", "requests_sent": request_sent}

