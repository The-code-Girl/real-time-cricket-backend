from fastapi import APIRouter, Depends
from app.auth.dependencies import require_admin

router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)

@router.post("/health-check")
def admin_health_check(
    admin=Depends(require_admin)
):
    return {
        "message": "Admin authorized",
        "admin_id": str(admin.id)
    }
