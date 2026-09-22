from sqlalchemy.orm import Session
from app.match.models import Match
from app.services.match_cache import set_match_state
from app.services.match_pubsub import publish_match_event
from app.services.match_cache import get_match_state

def create_match(db: Session, data):
    match = Match(
        team_a=data.team_a,
        team_b=data.team_b,
        venue=data.venue
    )
    db.add(match)
    db.commit()
    db.refresh(match)

    # initialize live state in Redis
    set_match_state(
        str(match.id),
        {
            "runs": 0,
            "wickets": 0,
            "overs": "0.0"
        }
    )
    return match

def process_ball_update(match_id: str, ball):
    current_state = get_match_state(match_id)
    if not current_state:
        raise ValueError("Match does not exist or has no live state")

    current_runs = int(current_state.get("runs", 0))
    current_wickets = int(current_state.get("wickets", 0))
    wickets = current_wickets + int(ball.wicket)

    state = {
        "overs": ball.over,
        "runs": current_runs + ball.runs,
        "wickets": wickets,
        "last_event": ball.commentary
    }
    set_match_state(match_id, state)

    # Publish to WebSocket
    publish_match_event(
        match_id,
        {
            "type": "BALL",
            "over": ball.over,
            "runs": state["runs"],
            "wickets": wickets,
            "wicket": ball.wicket,
            "commentary": ball.commentary
        }
    )
