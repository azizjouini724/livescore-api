from sqlalchemy import Column, Integer, String, DateTime, Float, Text
from datetime import datetime
from app.database import Base

class Match(Base):
    __tablename__ = "matches"
    
    id = Column(Integer, primary_key=True, index=True)
    api_id = Column(Integer, unique=True, index=True, nullable=False)
    
    # Teams
    home_team_id = Column(Integer, nullable=False, index=True)
    away_team_id = Column(Integer, nullable=False, index=True)
    home_team_name = Column(String(100), nullable=False)
    away_team_name = Column(String(100), nullable=False)
    
    # Scores
    home_goals = Column(Integer, nullable=True)
    away_goals = Column(Integer, nullable=True)
    home_expected_goals = Column(Float, nullable=True)
    away_expected_goals = Column(Float, nullable=True)
    
    # Match info
    status = Column(String(50), nullable=False)  # live, finished, not_started
    competition_id = Column(Integer, nullable=False, index=True)
    competition_name = Column(String(100), nullable=False)
    season = Column(Integer, nullable=False)
    round = Column(String(50), nullable=True)
    venue = Column(String(255), nullable=True)
    referee = Column(String(100), nullable=True)
    
    # Timing
    match_date = Column(DateTime, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    class Config:
        from_attributes = True