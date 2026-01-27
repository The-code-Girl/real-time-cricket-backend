from sqlalchemy.orm import Session
from app.match.models import Match
from app.services.match_cache import set_match_state
from app.services.match_pubsub import publish_match_event

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
    # Update Redis state
    state = {
        "overs": ball.over,
        "runs": ball.runs,
        "last_event": ball.commentary
    }
    set_match_state(match_id, state)

    # Publish to WebSocket
    publish_match_event(
        match_id,
        {
            "type": "BALL",
            "over": ball.over,
            "runs": ball.runs,
            "wicket": ball.wicket,
            "commentary": ball.commentary
        }
    )
