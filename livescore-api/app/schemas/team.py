from pydantic import BaseModel
from typing import Optional

class TeamResponse(BaseModel):
    id: int
    api_id: int
    name: str
    country: Optional[str]
    logo: Optional[str]
    
    class Config:
        from_attributes = True