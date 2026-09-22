from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.auth.dependencies import require_admin
from app.match.schemas import MatchCreate, MatchResponse, BallUpdate, LiveMatchState
from app.match.service import create_match, process_ball_update, get_live_state
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

@router.get("/history", response_model=list[MatchResponse])
def list_match_history(db: Session = Depends(get_db)):
    return db.query(Match).filter(Match.status == "COMPLETED").order_by(Match.created_at.desc()).all()

@router.get("/{match_id}/live", response_model=LiveMatchState)
def get_match_live_state(match_id: str):
    try:
        return get_live_state(match_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@router.post("/{match_id}/complete", response_model=MatchResponse, dependencies=[Depends(require_admin)])
def complete_match(match_id: str, db: Session = Depends(get_db)):
    match = db.query(Match).filter(Match.id == match_id).first()
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    match.status = "COMPLETED"
    db.commit()
    db.refresh(match)
    return match

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
