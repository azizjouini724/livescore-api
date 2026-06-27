from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base

class Competition(Base):
    __tablename__ = "competitions"
    
    id = Column(Integer, primary_key=True, index=True)
    api_id = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False, index=True)
    country = Column(String(100), nullable=True)
    logo = Column(String(500), nullable=True)
    type = Column(String(50), nullable=True)
    season = Column(Integer, nullable=False)
    current_season_start = Column(String(20), nullable=True)
    current_season_end = Column(String(20), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)