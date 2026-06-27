from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, Favorite
from app.utils.security import decode_token
from typing import Optional

router = APIRouter(prefix="/favorites", tags=["favorites"])

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

@router.post("/")
def add_favorite(
    team_id: Optional[int] = None,
    player_id: Optional[int] = None,
    match_id: Optional[int] = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_from_header)
):
    """Add favorite (team, player, or match)"""
    if not any([team_id, player_id, match_id]):
        raise HTTPException(status_code=400, detail="At least one ID must be provided")
    
    existing = db.query(Favorite).filter(
        (Favorite.user_id == user.id) &
        ((Favorite.team_id == team_id) if team_id else True) &
        ((Favorite.player_id == player_id) if player_id else True) &
        ((Favorite.match_id == match_id) if match_id else True)
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already favorited")
    
    favorite = Favorite(user_id=user.id, team_id=team_id, player_id=player_id, match_id=match_id)
    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return {"id": favorite.id, "status": "added"}

@router.get("/")
def get_favorites(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_from_header)
):
    """Get user favorites"""
    favorites = db.query(Favorite).filter(Favorite.user_id == user.id).all()
    return {"user_id": user.id, "total": len(favorites), "favorites": favorites}

@router.delete("/{favorite_id}")
def delete_favorite(
    favorite_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user_from_header)
):
    """Delete favorite"""
    favorite = db.query(Favorite).filter(
        (Favorite.id == favorite_id) & (Favorite.user_id == user.id)
    ).first()
    
    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")
    
    db.delete(favorite)
    db.commit()
    return {"status": "deleted"}