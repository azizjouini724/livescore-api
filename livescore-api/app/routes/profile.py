from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.utils.security import decode_token
from app.schemas.user import UserProfile

router = APIRouter(prefix="/profile", tags=["profile"])

def get_current_user_from_header(authorization: str = Header(None), db: Session = Depends(get_db)) -> User:
    """Extract & validate JWT from Authorization header"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="No token provided")
    
    token = authorization.split(" ")[1]
    try:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@router.get("/me", response_model=UserProfile)
def get_profile(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_from_header)
):
    """Get current user profile"""
    return user

@router.put("/me")
def update_profile(
    username: str = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_from_header)
):
    """Update user profile"""
    if username:
        existing = db.query(User).filter(
            (User.username == username) & (User.id != user.id)
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already taken")
        user.username = username
    
    db.commit()
    db.refresh(user)
    return {"status": "updated", "user": user}