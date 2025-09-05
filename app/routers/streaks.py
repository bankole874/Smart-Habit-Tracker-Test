# app/routers/streaks.py
from typing import List
from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.schemas.streak import StreakResponse
from app.services.streak_service import StreakService
from app.utils.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/habits", tags=["Streaks"])

@router.get("/{habit_id}/streaks", response_model=List[StreakResponse])
async def get_habit_streaks(
    habit_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get all streaks for a habit"""
    return StreakService.get_habit_streaks(db, habit_id, current_user)

@router.get("/{habit_id}/streaks/current")
async def get_current_streak(
    habit_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get current streak length"""
    streak_length = StreakService.calculate_current_streak(db, habit_id, current_user)
    return {"habit_id": habit_id, "current_streak": streak_length}

@router.get("/{habit_id}/streaks/longest")
async def get_longest_streak(
    habit_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """Get longest streak length"""
    streak_length = StreakService.calculate_longest_streak(db, habit_id, current_user)
    return {"habit_id": habit_id, "longest_streak": streak_length}
