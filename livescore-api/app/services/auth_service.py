from sqlalchemy.orm import Session
from app.models.user import User
from app.utils.security import (
    hash_password, verify_password,
    create_access_token, create_refresh_token,
    decode_token
)

class AuthService:
    
    @staticmethod
    def register_user(db: Session, email: str, username: str, password: str) -> User:
        # Check if user exists
        existing = db.query(User).filter(
            (User.email == email) | (User.username == username)
        ).first()
        
        if existing:
            raise Exception("Email or username already exists")
        
        # Create new user
        user = User(
            email=email,
            username=username,
            hashed_password=hash_password(password)
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def login_user(db: Session, email: str, password: str) -> dict:
        # Find user
        user = db.query(User).filter(User.email == email).first()
        
        if not user or not verify_password(password, user.hashed_password):
            raise Exception("Invalid credentials")
        
        if not user.is_active:
            raise Exception("User is inactive")
        
        # Create tokens
        access_token = create_access_token({"sub": str(user.id), "email": user.email})
        refresh_token = create_refresh_token({"sub": str(user.id)})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_id": user.id,
            "email": user.email,
            "username": user.username
        }
    
    @staticmethod
    def refresh_access_token(refresh_token: str) -> str:
        payload = decode_token(refresh_token)
        
        if payload.get("type") != "refresh":
            raise Exception("Invalid token type")
        
        user_id = payload.get("sub")
        access_token = create_access_token({"sub": user_id})
        
        return access_token
    
    @staticmethod
    def get_current_user(db: Session, token: str) -> User:
        payload = decode_token(token)
        user_id = int(payload.get("sub"))
        
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user or not user.is_active:
            raise Exception("User not found or inactive")
        
        return user