# app/routers/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from app.database import get_session
from app.schemas.auth import UserRegister, Token
from app.schemas.user import UserResponse, UserUpdate
from app.services.auth_service import AuthService
from app.utils.dependencies import get_current_user
from app.models.user import User
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
async def register(user_data: UserRegister, db: Session = Depends(get_session)):
    """Register new user"""
    return AuthService.create_user(db, user_data)

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    """Login user"""
    from app.schemas.auth import UserLogin
    login_data = UserLogin(username=form_data.username, password=form_data.password)
    access_token = AuthService.authenticate_user(db, login_data)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile"""
    return current_user

@router.put("/me", response_model=UserResponse)
async def update_profile(
    user_data: UserUpdate, 
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Update user profile"""
    update_data = user_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(current_user, key, value)
    
    current_user.updated_at = datetime.utcnow()
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/me")
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Delete user account"""
    db.delete(current_user)
    db.commit()
    return {"message": "Account deleted successfully"}

# app/routers/habits.py
from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.schemas.habit import HabitCreate, HabitUpdate, HabitResponse
from app.services.habit_service import HabitService
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/habits", tags=["Habits"])

@router.post("/", response_model=HabitResponse)
async def create_habit(
    habit_data: HabitCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Create new habit"""
    return HabitService.create_habit(db, habit_data, current_user)

@router.get("/", response_model=List[HabitResponse])
async def get_habits(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get all user habits"""
    return HabitService.get_user_habits(db, current_user)

@router.get("/{habit_id}", response_model=HabitResponse)
async def get_habit(
    habit_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get habit by ID"""
    return HabitService.get_habit_by_id(db, habit_id, current_user)

@router.put("/{habit_id}", response_model=HabitResponse)
async def update_habit(
    habit_id: int,
    habit_data: HabitUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Update habit"""
    return HabitService.update_habit(db, habit_id, habit_data, current_user)

@router.delete("/{habit_id}")
async def delete_habit(
    habit_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Delete habit"""
    HabitService.delete_habit(db, habit_id, current_user)
    return {"message": "Habit deleted successfully"}

@router.patch("/{habit_id}/archive", response_model=HabitResponse)
async def archive_habit(
    habit_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Archive habit (soft delete)"""
    return HabitService.archive_habit(db, habit_id, current_user)
