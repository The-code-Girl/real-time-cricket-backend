from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.router import router as api_v1_router
from app.auth.router import router as auth_router
from app.admin.router import router as admin_router
from app.websocket.router import router as ws_router
from app.match.router import router as match_router


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "ok",
        "service": settings.APP_NAME
    }

app.include_router(api_v1_router)
app.include_router(auth_router)
app.include_router(admin_router)
app.include_router(ws_router)
app.include_router(match_router)


