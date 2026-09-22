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
            "overs": "0.0",
            "legal_balls": 0,
            "last_event": "Match started"
        }
    )
    return match

def process_ball_update(match_id: str, ball):
    current_state = get_match_state(match_id)
    if not current_state:
        raise ValueError("Match does not exist or has no live state")

    current_runs = int(current_state.get("runs", 0))
    current_wickets = int(current_state.get("wickets", 0))
    legal_balls = int(current_state.get("legal_balls", 0))

    if ball.delivery == "wide":
        delivery_runs = max(1, ball.runs)
        counts_as_legal_ball = False
    elif ball.delivery == "no_ball":
        delivery_runs = 1 + ball.runs
        counts_as_legal_ball = False
    else:
        delivery_runs = ball.runs
        counts_as_legal_ball = True

    if counts_as_legal_ball:
        legal_balls += 1

    over = f"{legal_balls // 6}.{legal_balls % 6}"
    wickets = current_wickets + int(ball.wicket)

    state = {
        "overs": over,
        "runs": current_runs + delivery_runs,
        "wickets": wickets,
        "legal_balls": legal_balls,
        "last_event": ball.commentary
    }
    set_match_state(match_id, state)

    # Publish to WebSocket
    publish_match_event(
        match_id,
        {
            "type": "BALL",
            "over": over,
            "runs": state["runs"],
            "runs_this_ball": delivery_runs,
            "wickets": wickets,
            "wicket": ball.wicket,
            "delivery": ball.delivery,
            "legal_ball": counts_as_legal_ball,
            "commentary": ball.commentary
        }
    )

def get_live_state(match_id: str):
    state = get_match_state(match_id)
    if not state:
        raise ValueError("Match does not exist or has no live state")
    return {
        "runs": int(state.get("runs", 0)),
        "wickets": int(state.get("wickets", 0)),
        "overs": state.get("overs", "0.0"),
        "last_event": state.get("last_event")
    }
