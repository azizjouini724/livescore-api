from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Standing(Base):
    __tablename__ = "standings"
    
    id = Column(Integer, primary_key=True, index=True)
    competition_id = Column(Integer, nullable=False, index=True)
    season = Column(Integer, nullable=False, index=True)
    team_id = Column(Integer, nullable=False, index=True)
    team_name = Column(String(100), nullable=False)
    rank = Column(Integer, nullable=False)
    points = Column(Integer, nullable=False)
    matches_played = Column(Integer, nullable=False)
    wins = Column(Integer, nullable=False)
    draws = Column(Integer, nullable=False)
    losses = Column(Integer, nullable=False)
    goals_for = Column(Integer, nullable=False)
    goals_against = Column(Integer, nullable=False)
    goal_difference = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    class Config:
        from_attributes = True