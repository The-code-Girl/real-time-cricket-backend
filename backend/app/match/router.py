from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.auth.dependencies import require_admin
from app.match.schemas import MatchCreate, BallUpdate
from app.match.service import create_match, process_ball_update

router = APIRouter(prefix="/matches", tags=["Matches"])

@router.post("/", dependencies=[Depends(require_admin)])
def create_match_api(
    data: MatchCreate,
    db: Session = Depends(get_db)
):
    return create_match(db, data)

@router.post("/{match_id}/ball", dependencies=[Depends(require_admin)])
def ball_update_api(
    match_id: str,
    ball: BallUpdate
):
    process_ball_update(match_id, ball)
    return {"status": "update published"}
