from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.auth.dependencies import require_admin
from app.match.schemas import MatchCreate, MatchResponse, BallUpdate
from app.match.service import create_match, process_ball_update
from app.match.models import Match

router = APIRouter(prefix="/matches", tags=["Matches"])

@router.post("/", response_model=MatchResponse, dependencies=[Depends(require_admin)])
def create_match_api(
    data: MatchCreate,
    db: Session = Depends(get_db)
):
    return create_match(db, data)

@router.get("/live", response_model=list[MatchResponse])
def list_live_matches(db: Session = Depends(get_db)):
    return db.query(Match).filter(Match.status == "LIVE").all()

@router.post("/{match_id}/ball", dependencies=[Depends(require_admin)])
def ball_update_api(
    match_id: str,
    ball: BallUpdate
):
    try:
        process_ball_update(match_id, ball)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"status": "update published"}
