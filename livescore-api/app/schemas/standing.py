from pydantic import BaseModel

class StandingResponse(BaseModel):
    id: int
    competition_id: int
    team_name: str
    rank: int
    points: int
    matches_played: int
    wins: int
    draws: int
    losses: int
    goals_for: int
    goals_against: int
    
    class Config:
        from_attributes = True