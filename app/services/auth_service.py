# app/services/auth_service.py
from sqlmodel import Session, select
from fastapi import HTTPException, status
from datetime import timedelta
from app.models.user import User
from app.schemas.user import UserCreate
from app.schemas.auth import UserLogin
from app.utils.security import verify_password, get_password_hash, create_access_token
from app.config import settings

class AuthService:
    @staticmethod
    def create_user(db: Session, user_data: UserCreate) -> User:
        """Create new user"""
        # Check if user exists
        statement = select(User).where(
            (User.username == user_data.username) | (User.email == user_data.email)
        )
        existing_user = db.exec(statement).first()
        
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username or email already registered"
            )
        
        # Create user
        hashed_password = get_password_hash(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed_password
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def authenticate_user(db: Session, login_data: UserLogin) -> str:
        """Authenticate user and return JWT token"""
        statement = select(User).where(User.username == login_data.username)
        user = db.exec(statement).first()
        
        if not user or not verify_password(login_data.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
        access_token = create_access_token(
            data={"sub": user.username}, 
            expires_delta=access_token_expires
        )
        return access_token
