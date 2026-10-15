"""مسیر سالمت عملیاتی -- از روز اول، طبق سند Forge."""
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live")
async def live() -> dict:
    return {"status": "ok"}


@router.get("/ready")
async def ready() -> dict:
    return {"status": "ok"}
