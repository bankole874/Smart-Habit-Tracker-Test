# app/utils/dependencies.py
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from app.database import get_session
from app.models.user import User
from app.utils.security import oauth2_scheme, verify_token

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_session)):
    """Get current authenticated user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token_data = verify_token(token, credentials_exception)
    
    statement = select(User).where(User.username == token_data.username)
    user = db.exec(statement).first()
    
    if user is None:
        raise credentials_exception
    return user
