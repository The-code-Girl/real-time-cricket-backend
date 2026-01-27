from pydantic import BaseModel
from uuid import UUID

class MatchCreate(BaseModel):
    team_a: str
    team_b: str
    venue: str

class MatchResponse(BaseModel):
    id: UUID
    team_a: str
    team_b: str
    venue: str
    status: str

class BallUpdate(BaseModel):
    over: str
    runs: int
    wicket: bool = False
    commentary: str
