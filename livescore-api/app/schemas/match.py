from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MatchDetail(BaseModel):
    id: int
    api_id: int
    home_team_name: str
    away_team_name: str
    home_goals: Optional[int]
    away_goals: Optional[int]
    status: str
    competition_name: str
    match_date: datetime
    
    class Config:
        from_attributes = True

class MatchResponse(BaseModel):
    id: int
    home_team_name: str
    away_team_name: str
    home_goals: Optional[int]
    away_goals: Optional[int]
    status: str
    match_date: datetime
    
    class Config:
        from_attributes = True