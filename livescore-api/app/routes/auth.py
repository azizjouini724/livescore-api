from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import (
    UserRegister, UserLogin, TokenResponse,
    UserProfile, RefreshTokenRequest
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=TokenResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    try:
        AuthService.register_user(db, user_data.email, user_data.username, user_data.password)
        return AuthService.login_user(db, user_data.email, user_data.password)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    try:
        result = AuthService.login_user(db, credentials.email, credentials.password)
        return result
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.post("/refresh")
def refresh(request: RefreshTokenRequest):
    try:
        new_access_token = AuthService.refresh_access_token(request.refresh_token)
        return {
            "access_token": new_access_token,
            "token_type": "bearer"
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/me", response_model=UserProfile)
def get_profile(db: Session = Depends(get_db), token: str = None):
    if not token:
        raise HTTPException(status_code=401, detail="No token provided")
    
    try:
        user = AuthService.get_current_user(db, token)
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))