from typing import Literal

from pydantic import BaseModel, Field
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

    model_config = {"from_attributes": True}

class BallUpdate(BaseModel):
    delivery: Literal["legal", "wide", "no_ball", "bye", "leg_bye"] = "legal"
    over: str | None = None
    runs: int = Field(ge=0)
    wicket: bool = False
    commentary: str = Field(min_length=1, max_length=500)

class LiveMatchState(BaseModel):
    runs: int
    wickets: int
    overs: str
    last_event: str | None = None
