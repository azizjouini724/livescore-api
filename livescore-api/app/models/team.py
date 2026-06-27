from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.database import Base

class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    api_id = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False, index=True)
    code = Column(String(10), nullable=True)
    country = Column(String(100), nullable=True)
    founded = Column(Integer, nullable=True)
    national = Column(Integer, default=0)
    logo = Column(String(500), nullable=True)
    venue_name = Column(String(200), nullable=True)  # 255 → 200
    venue_city = Column(String(100), nullable=True)
    venue_capacity = Column(Integer, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)