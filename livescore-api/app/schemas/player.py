from pydantic import BaseModel
from typing import Optional

class PlayerResponse(BaseModel):
    id: int
    api_id: int
    name: str
    age: Optional[int]
    nationality: Optional[str]
    photo: Optional[str]
    
    class Config:
        from_attributes = True