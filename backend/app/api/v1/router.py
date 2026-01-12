from fastapi import APIRouter
from app.api.v1.health import router as health_router

router = APIRouter(prefix="/api/v1")

router.include_router(health_router)


@router.get("/ping")
async def ping():
    return {
        "message": "pong"
    }