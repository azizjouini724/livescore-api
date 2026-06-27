from sqlalchemy import Column, Integer, String, DateTime, Float
from datetime import datetime
from app.database import Base

class Player(Base):
    __tablename__ = "players"
    
    id = Column(Integer, primary_key=True, index=True)
    api_id = Column(Integer, unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=False, index=True)
    firstname = Column(String(100), nullable=True)
    lastname = Column(String(100), nullable=True)
    age = Column(Integer, nullable=True)
    birth_date = Column(DateTime, nullable=True)
    nationality = Column(String(100), nullable=True)
    height = Column(String(20), nullable=True)
    weight = Column(String(20), nullable=True)
    injured = Column(Integer, default=0)
    photo = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)